# Copyright 2012 OpenStack Foundation.
# Copyright 2015 Hewlett-Packard Development Company, L.P.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import logging
import time

import requests
import six.moves.urllib.parse as urlparse

from neutronclient import client
from neutronclient.common import constants
from neutronclient.common import exceptions
from neutronclient.common import serializer
from neutronclient.common import utils

_logger = logging.getLogger(__name__)


def exception_handler_v20(status_code, error_content):
    """Exception handler for API v2.0 client.

    This routine generates the appropriate Neutron exception according to
    the contents of the response body.

    :param status_code: HTTP error status code
    :param error_content: deserialized body of error response
    """
    error_dict = None
    if isinstance(error_content, dict):
        error_dict = error_content.get('NeutronError')
    # Find real error type
    bad_neutron_error_flag = False
    if error_dict:
        # If Neutron key is found, it will definitely contain
        # a 'message' and 'type' keys?
        try:
            error_type = error_dict['type']
            error_message = error_dict['message']
            if error_dict['detail']:
                error_message += "\n" + error_dict['detail']
        except Exception as e:
            bad_neutron_error_flag = True
        if not bad_neutron_error_flag:
            # If corresponding exception is defined, use it.
            client_exc = getattr(exceptions, '%sClient' % error_type, None)
            # Otherwise look up per status-code client exception
            if not client_exc:
                client_exc = exceptions.HTTP_EXCEPTION_MAP.get(status_code)
            if client_exc:
                raise client_exc(message=error_message,
                                 status_code=status_code)
            else:
                raise exceptions.NeutronClientException(
                    status_code=status_code, message=error_message)
        else:
            raise exceptions.NeutronClientException(status_code=status_code,
                                                    message=error_dict)
    else:
        message = None
        if isinstance(error_content, dict):
            message = error_content.get('message')
        if message:
            raise exceptions.NeutronClientException(status_code=status_code,
                                                    message=message)

    # If we end up here the exception was not a neutron error
    msg = "%s-%s" % (status_code, error_content)
    raise exceptions.NeutronClientException(status_code=status_code,
                                            message=msg)


class APIParamsCall(object):
    """A Decorator to add support for format and tenant overriding and filters.
    """

    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        def with_params(*args, **kwargs):
            _format = instance.format
            if 'format' in kwargs:
                instance.format = kwargs['format']
            ret = self.function(instance, *args, **kwargs)
            instance.format = _format
            return ret

        return with_params


class ClientBase(object):
    """Client for the OpenStack Neutron v2.0 API.

    :param string username: Username for authentication. (optional)
    :param string user_id: User ID for authentication. (optional)
    :param string password: Password for authentication. (optional)
    :param string token: Token for authentication. (optional)
    :param string tenant_name: Tenant name. (optional)
    :param string tenant_id: Tenant id. (optional)
    :param string auth_strategy: 'keystone' by default, 'noauth' for no
                                 authentication against keystone. (optional)
    :param string auth_url: Keystone service endpoint for authorization.
    :param string service_type: Network service type to pull from the
                                keystone catalog (e.g. 'network') (optional)
    :param string endpoint_type: Network service endpoint type to pull from the
                                 keystone catalog (e.g. 'publicURL',
                                 'internalURL', or 'adminURL') (optional)
    :param string region_name: Name of a region to select when choosing an
                               endpoint from the service catalog.
    :param string endpoint_url: A user-supplied endpoint URL for the neutron
                            service.  Lazy-authentication is possible for API
                            service calls if endpoint is set at
                            instantiation.(optional)
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    :param bool insecure: SSL certificate validation. (optional)
    :param bool log_credentials: Allow for logging of passwords or not.
                                 Defaults to False. (optional)
    :param string ca_cert: SSL CA bundle file to use. (optional)
    :param integer retries: How many times idempotent (GET, PUT, DELETE)
                            requests to Neutron server should be retried if
                            they fail (default: 0).
    :param bool raise_errors: If True then exceptions caused by connection
                              failure are propagated to the caller.
                              (default: True)
    :param session: Keystone client auth session to use. (optional)
    :param auth: Keystone auth plugin to use. (optional)

    Example::

        from neutronclient.v2_0 import client
        neutron = client.Client(username=USER,
                                password=PASS,
                                tenant_name=TENANT_NAME,
                                auth_url=KEYSTONE_URL)

        nets = neutron.list_networks()
        ...

    """

    # API has no way to report plurals, so we have to hard code them
    # This variable should be overridden by a child class.
    EXTED_PLURALS = {}

    def __init__(self, **kwargs):
        """Initialize a new client for the Neutron v2.0 API."""
        super(ClientBase, self).__init__()
        self.retries = kwargs.pop('retries', 0)
        self.raise_errors = kwargs.pop('raise_errors', True)
        self.httpclient = client.construct_http_client(**kwargs)
        self.format = "json"
        self.action_prefix = kwargs.pop('action_prefix', '')  # e.g. 'v2.0/'
        self.retry_interval = 1

    def _handle_fault_response(self, status_code, response_body):
        # Create exception with HTTP status code and message
        _logger.debug("Error message: %s", response_body)
        # Add deserialized error message to exception arguments
        try:
            des_error_body = self.deserialize(response_body, status_code)
        except Exception:
            # If unable to deserialized body it is probably not a
            # Neutron error
            des_error_body = {'message': response_body}
        # Raise the appropriate exception
        exception_handler_v20(status_code, des_error_body)

    def do_request(self, method, action, body=None, headers=None, params=None):
        # Add format and tenant_id
        # action += "%s" % self.format
        action = self.action_prefix + action
        if type(params) is dict and params:
            params = utils.safe_encode_dict(params)
            action += '?' + urlparse.urlencode(params, doseq=1)

        if body:
            body = self.serialize(body)

        resp, replybody = self.httpclient.do_request(
            action, method, body=body,
            content_type=self.content_type())

        status_code = resp.status_code
        if status_code in (requests.codes.ok,
                           requests.codes.created,
                           requests.codes.accepted,
                           requests.codes.no_content):
            return self.deserialize(replybody, status_code)
        else:
            if not replybody:
                replybody = resp.reason
            self._handle_fault_response(status_code, replybody)

    def get_auth_info(self):
        return self.httpclient.get_auth_info()

    def serialize(self, data):
        """Serializes a dictionary into either XML or JSON.

        A dictionary with a single key can be passed and it can contain any
        structure.
        """
        if data is None:
            return None
        elif type(data) is dict:
            return serializer.Serializer(
                self.get_attr_metadata()).serialize(data, self.content_type())
        elif type(data) is list:
            return serializer.Serializer(
                self.get_attr_metadata()).serialize(data, self.content_type())
        else:
            raise Exception("Unable to serialize object of type = '%s'" %
                            type(data))

    def deserialize(self, data, status_code):
        """Deserializes an XML or JSON string into a dictionary."""
        if status_code == 204:
            return data
        return serializer.Serializer(self.get_attr_metadata()).deserialize(
            data)['body']

    def get_attr_metadata(self):
        if self.format == 'json':
            return {}
        old_request_format = self.format
        self.format = 'json'
        exts = self.list_extensions()['extensions']
        self.format = old_request_format
        ns = dict([(ext['alias'], ext['namespace']) for ext in exts])
        self.EXTED_PLURALS.update(constants.PLURALS)
        return {'plurals': self.EXTED_PLURALS,
                'xmlns': constants.XML_NS_V20,
                constants.EXT_NS: ns}

    def content_type(self, _format=None):
        """Returns the mime-type for either 'xml' or 'json'.

        Defaults to the currently set format.
        """
        _format = _format or self.format
        return "application/%s" % (_format)

    def retry_request(self, method, action, body=None,
                      headers=None, params=None):
        """Call do_request with the default retry configuration.

        Only idempotent requests should retry failed connection attempts.
        :raises: ConnectionFailed if the maximum # of retries is exceeded
        """
        max_attempts = self.retries + 1
        for i in range(max_attempts):
            try:
                return self.do_request(method, action, body=body,
                                       headers=headers, params=params)
            except exceptions.ConnectionFailed:
                # Exception has already been logged by do_request()
                if i < self.retries:
                    _logger.debug('Retrying connection to Neutron service')
                    time.sleep(self.retry_interval)
                elif self.raise_errors:
                    raise

        if self.retries:
            msg = ("Failed to connect to Neutron server after %d attempts"
                   % max_attempts)
        else:
            msg = "Failed to connect Neutron server"

        raise exceptions.ConnectionFailed(reason=msg)

    def delete(self, action, body=None, headers=None, params=None):
        return self.retry_request("DELETE", action, body=body,
                                  headers=headers, params=params)

    def get(self, action, body=None, headers=None, params=None):
        return self.retry_request("GET", action, body=body,
                                  headers=headers, params=params)

    def post(self, action, body=None, headers=None, params=None):
        # Do not retry POST requests to avoid the orphan objects problem.
        return self.do_request("POST", action, body=body,
                               headers=headers, params=params)

    def put(self, action, body=None, headers=None, params=None):
        return self.retry_request("PUT", action, body=body,
                                  headers=headers, params=params)

    def list(self, collection, path, retrieve_all=True, **params):
        if retrieve_all:
            res = []
            for r in self._pagination(collection, path, **params):
                res.extend(r[collection])
            return {collection: res}
        else:
            return self._pagination(collection, path, **params)

    def _pagination(self, collection, path, **params):
        if params.get('page_reverse', False):
            linkrel = 'previous'
        else:
            linkrel = 'next'
        next = True
        while next:
            res = self.get(path, params=params)
            yield res
            next = False
            try:
                for link in res['%s_links' % collection]:
                    if link['rel'] == linkrel:
                        query_str = urlparse.urlparse(link['href']).query
                        params = urlparse.parse_qs(query_str)
                        next = True
                        break
            except KeyError:
                break


class PlatformClient(ClientBase):
    def __init__(self, **kwargs):
        kwargs.setdefault('user_agent', 'python-isystemclient')
        kwargs.setdefault('service_type', 'platform')
        # kwargs.setdefault('interface', 'internal')
        super(PlatformClient, self).__init__(**kwargs)

    @APIParamsCall
    def list_ext(self, path, **_params):
        """Client extension hook for lists.
        """
        return self.get(path, params=_params)

    @APIParamsCall
    def show_ext(self, path, id, **_params):
        """Client extension hook for shows.
        """
        return self.get(path % id, params=_params)

    @APIParamsCall
    def create_ext(self, path, body=None):
        """Client extension hook for creates.
        """
        return self.post(path, body=body)

    @APIParamsCall
    def update_ext(self, path, id, body=None):
        """Client extension hook for updates.
        """
        return self.put(path % id, body=body)

    @APIParamsCall
    def delete_ext(self, path, id):
        """Client extension hook for deletes.
        """
        return self.delete(path % id)

    def get_isystem_id(self):
        isystems = self.get('/isystems')
        for l in isystems["isystems"]:
            if l["uuid"]:
                return l["uuid"]

    def patch_data(self, action, data):
        return self.retry_request("PATCH", action=action, body=data,
                                  headers=None, params=None)

    def modify_isystem_name(self, name):
        """
        :param name: the name want to be modified.
        :return: "ihosts" dict
        """
        id = self.get_isystem_id()
        action = '/isystems/%s' % id
        body = [{"path": "/name", "value": "%s" % name, "op": "replace"}]
        return self.patch_data(action, body)

    def list_hosts(self):
        """
        :return: ihosts list
        """
        ihosts = self.get('/ihosts')
        return ihosts["ihosts"]

    def get_host_id(self, name):
        ihosts_list = self.list_hosts()
        for h in ihosts_list:
            if h["hostname"] == name:
                return h["uuid"]

    def get_host_humanid(self, host_name):
        ihosts_list = self.list_hosts()
        for h in ihosts_list:
            if h["hostname"] == host_name:
                return h["id"]

    def list_disks(self, host_id):
        """
        :return: disks list
        """
        idisks = self.get('/ihosts/%s/idisks' % host_id)
        return idisks["idisks"]

    def get_disk_id_raw(self, disks_list, disk_name):
        '''
        get disk id from a raw list of disks
        :param disks_list: (list) a raw list of disks, (necessary)
        :param disk_name: (string) name of target disk, (necessary)
        :return: (string) disk id
        '''
        for d in disks_list:
            if d["device_node"] == disk_name:
                return d["uuid"]

    def get_disk_id(self, ihost_id, idisk_name):
        idisks_list = self.list_disks(ihost_id)
        return self.get_disk_id_raw(disks_list=idisks_list, disk_name=idisk_name)

    def get_disk_size_raw(self, disks_list, disk_name):
        '''
        get disk size from a raw list of disks
        :param disks_list: (list) a raw list of disks, (necessary)
        :param disk_name: (string) name of target disk, (necessary)
        :return: (integer) disk size in MB
        '''
        for d in disks_list:
            if d["device_node"] == disk_name:
                return d["size_mib"]

    def get_disk_size(self, host_id, disk_name):
        disks_list = self.list_disks(host_id)
        return self.get_disk_size_raw(disks_list=disks_list, disk_name=disk_name)

    def host_lvg_add(self, host_id):
        action = "/ilvgs"
        body = {"lvm_vg_name": "nova-local", "ihost_uuid": "%s" % host_id}
        return self.post(action=action, body=body)

    def host_lvg_modify(self, lvg_id, size):
        action = "/ilvgs/%s" % lvg_id
        body = [{"path": "/capabilities", "value": "{\"instances_lv_size_mib\": %s}" % size, "op": "replace"}]
        return self.patch_data(action, body)

    def get_lvg_id(self, host_id):
        action = "/ihosts/%s/ilvgs" % host_id
        lvg_list = self.get(action=action)
        for l in lvg_list["ilvgs"]:
            if l["lvm_vg_name"] == "nova-local":
                return l["uuid"]

    def host_pv_add(self, host_id, lvg_id, disk_id):
        action = "/ipvs"
        body = {"ihost_uuid": "%s" % host_id, "ilvg_uuid": "%s" % lvg_id, "idisk_uuid": "%s" % disk_id}
        return self.post(action=action, body=body)

    def get_interface_id(self, host_id, interface_name):
        action = "/ihosts/%s/iinterfaces" % host_id
        interfaces_list = self.get(action)
        for i in interfaces_list["iinterfaces"]:
            if i["ifname"] == interface_name:
                return i["uuid"]

    def _create_modify_param_dict(self, path, value):
        return {"path": "%s" % path, "value": "%s" % value, "op": "replace"}

    def host_if_modify(self, interface_id, **params):
        """
        Modify the host interface.
        :param interface_id: (string), interface id, (necessary)
        :param params: 'name'
                       'type'
                       'providenet'
                       'mtu'
        :return:
        """
        action = "/iinterfaces/%s" % interface_id
        name = params.get("name", None)
        type = params.get("type", None)
        providenet = params.get("providenet", None)
        mtu = params.get("mtu", None)
        body = []
        if name:
            body.append(self._create_modify_param_dict("/ifname", name))
        if type:
            body.append(self._create_modify_param_dict("/networktype", type))
        if providenet:
            body.append(self._create_modify_param_dict("/providernetworks", providenet))
        if mtu:
            body.append(self._create_modify_param_dict("/imtu", mtu))
        return self.patch_data(action=action, data=body)

    def unlock_host(self, host_name):
        host_id = self.get_host_humanid(host_name)
        data = [{"path": "/action", "value": "unlock", "op": "replace"}]
        return self.patch_data(action="/ihosts/%s" % host_id, data=data)

    def lock_host(self, host_name):
        host_id = self.get_host_humanid(host_name)
        data = [{"path": "/action", "value": "lock", "op": "replace"}]
        return self.patch_data(action="/ihosts/%s" % host_id, data=data)

    def swact_host(self, host_name):
        host_id = self.get_host_humanid(host_name)
        data = [{"path": "/action", "value": "swact", "op": "replace"}]
        return self.patch_data(action="/ihosts/%s" % host_id, data=data)

    def get_host(self, humanid=None, host_name=None):
        if humanid:
            return self.get(action="/ihosts/%s" % humanid)
        elif host_name:
            host_id = self.get_host_humanid(host_name)
            return self.get(action="/ihosts/%s" % host_id)
        else:
            print("Error: get_host() needs at least 1 param.")
            exit()

    def list_alarms(self):
        alarms = self.get("/ialarms")
        return alarms["ialarms"]

    def list_isystems(self):
        isystems = self.get('/isystems')
        return isystems["isystems"]

    def list_storconfig(self):
        storconfig = self.get("/istorconfig")
        return storconfig["istorconfigs"]


class NokiaCliClient(ClientBase):
    def __init__(self, **kwargs):
        kwargs.setdefault('user_agent', 'tersy-nokiacliclient')
        kwargs.setdefault('service_type', 'restfulapi')
        # kwargs.setdefault('interface', 'internal')
        super(NokiaCliClient, self).__init__(**kwargs)

    def alarm_list_active(self):
        alarms = self.get("alarm/v1/alarms")
        # change alarm to list
        alarm_list = []
        for k in alarms["data"]:
            # to align with the previous alarm data format, add/change some key/value.
            alarms["data"][k]["ReasonText"] = alarms["data"][k]["message"]
            alarms["data"][k]["Severity"] = alarms["data"][k]["severity"]
            alarm_list.append(alarms["data"][k])
        return alarm_list

    def swm_show_cluster(self):
        swm_cluster = self.get("swm/v1/cluster")
        return swm_cluster["data"]

    def get_nodes(self):
        """
        :return:
        {u'code': 0,
        u'data': {u'controller-3': {u'running-state': u'running', u'admin-state': u'unlocked', u'role': u'active'},
                  u'controller-2': {u'running-state': u'running', u'admin-state': u'unlocked', u'role': u'active'},
                  u'compute-10': {u'running-state': u'running', u'admin-state': u'unlocked', u'role': u'active'},
                  u'controller-1': {u'running-state': u'running', u'admin-state': u'unlocked', u'role': u'active'},
                  u'compute-8': {u'running-state': u'running', u'admin-state': u'unlocked', u'role': u'active'}},
        u'desc': u''}
        """
        nodes = self.get("has/v1/nodes")
        return nodes["data"]