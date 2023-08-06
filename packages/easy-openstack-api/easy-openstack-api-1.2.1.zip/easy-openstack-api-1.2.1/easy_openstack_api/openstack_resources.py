#! /usr/bin/python
from cinderclient.v2.client import Client as CinderClient
from glanceclient.v2.client import Client as GlanceClient
from heatclient.client import Client as HeatClient
from keystoneauth1 import exceptions as keystone_exceptions
from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from keystoneclient.v3.client import Client as KeystoneClient
from neutronclient.v2_0.client import Client as NeutronClient
from novaclient import exceptions as nova_exceptions
from novaclient.client import Client as NovaClient
from easy_openstack_api.SelfDefinedClient import NokiaCliClient
from time import sleep
import logging

LOG = logging.getLogger("easy-openstack-api")


class NoGetVIMMethod(Exception):
    pass


class NoQueryPatchMethod(Exception):
    pass


class OpenstackBase(object):
    def __init__(self, cred=None, logger=LOG, **kwargs):
        self.logger = logger
        self.logger.info('Initializing rest api')
        if (not cred) and (not kwargs.get("session")):
            raise Exception("init Openstack object fail, need cred or session info")
        self.cred = cred
        self.endpoint_type = 'publicURL'
        if kwargs.get("session"):
            self.sess = kwargs.pop("session")
        else:
            self.sess = self.get_session()
        self.project_id = self.sess.get_project_id()

    def get_session(self):
        if self.cred['auth_url'] is None:
            raise Exception('Auth url is not retrieved. Save the stack once')
        self.logger.info('%s Authenticating to openstack: %s' % (self.__class__.__name__, self.cred))
        auth = v3.Password(auth_url=self.cred['auth_url'],
                           username=self.cred['username'], password=self.cred['password'],
                           user_domain_id="default",
                           project_name=self.cred['tenant_name'],
                           project_domain_id="default")
        session = Session(auth=auth, verify=False)
        self.logger.debug(auth.get_access(session).service_catalog.get_endpoints(interface='public'))
        return session

    def delete(self, resource):
        '''Displays informational message about a resource deletion.'''
        self.logger.debug('Deleting %s.' % resource)


class NokiaCliObject(OpenstackBase):
    def __init__(self, cred=None, **kwargs):
        super(NokiaCliObject, self).__init__(cred, **kwargs)
        self.client = NokiaCliClient(session=self.sess, endpoint_type=self.endpoint_type)


class Alarm(NokiaCliObject):
    def list(self):
        return self.client.alarm_list_active()


class Swm(NokiaCliObject):
    @property
    def _get_sw_info(self):
        if hasattr(self, "_%s__sw_info" % self.__class__.__name__):
            return self.__sw_info
        else:
            self.__sw_info = self.client.swm_show_cluster()
            return self.__sw_info

    def get_VIM(self):
        try:
            return self._get_sw_info['SW Release']
        except:
            return self._get_sw_info[0]

    def get_patch(self):
        try:
            return self._get_sw_info['SW Build']
        except:
            return self._get_sw_info[1]


class KeystoneBase(OpenstackBase):
    def __init__(self, **kwargs):
        super(KeystoneBase, self).__init__(**kwargs)
        self.client = KeystoneClient(session=self.sess, interface='public')


class KeystoneUser(KeystoneBase):
    def get_user_object(self, user_name):
        users_list = self.client.users.list()
        for user in users_list:
            if user.name == user_name:
                return user
        raise Exception("user_name<%s> doesn't exist on cloud<%s>" % (user_name, self.cred.get("auth_url")))

    def enable(self, user_name):
        user = self.get_user_object(user_name)
        if user is None:
            return "Try to enable stack<%s>user<%s>, but user not exist." % (self.cred.get("auth_url"), user_name)
        self.client.users.update(user=user, enabled=True)

    def disable(self, user_name):
        user = self.get_user_object(user_name)
        if user is None:
            return "Try to enable stack<%s>user<%s>, but user not exist." % (
                    self.cred.get("auth_url"), self.cred.get("username"))
        self.client.users.update(user=user, enabled=False)


class KeystoneEndpoint(KeystoneBase):
    def get(self, service="keystone", interface="public"):
        _services = self.client.services.list(name=service)
        _endpoints = self.client.endpoints.list(service=_services[0], interface=interface)
        for endpoint in _endpoints:
            if endpoint.service_id == _services[0].id and endpoint.interface == interface:
                return endpoint.url


class HeatStacks(OpenstackBase):
    def __init__(self, cred=None, **kwargs):
        super(HeatStacks, self).__init__(cred, **kwargs)
        self.client = HeatClient(1, session=self.sess, endpoint_type=self.endpoint_type, service_type='orchestration')

    def list(self):
        all_stacks = self.client.stacks.list()
        stacks_list = []
        for stack in all_stacks:
            if stack.project == self.project_id:
                stacks_list.append(stack)
        return stacks_list

    def delete(self, stack):
        super(HeatStacks, self).delete(stack)
        self.client.stacks.delete(stack.id)
        # delete the stack for 2 minutes
        try_count = 10
        while try_count > 0:
            try:
                stack.get()
                if not stack or stack.stack_status in ['DELETE_COMPLETE']:
                    self.logger.info('Stack(ID: %s) has been deleted successfully!' % stack.id)
                    return True
                elif stack.stack_status in ['DELETE_IN_PROGRESS']:
                    sleep(15)
                else:
                    #failed or other invalid
                    sleep(15)
                    self.client.stacks.delete(stack.id)
            except Exception as e:
                if not stack or stack.stack_status in ['DELETE_COMPLETE']:
                    self.logger.info('Stack(ID:%s) has been deleted successfully!' % stack.id)
                    return True
                else:
                    self.logger.error('Error during deleting stack (ID:%s) in cloud<%s>_project<%s>' % (
                        stack.id, self.cred.get("auth_url"), self.cred.get("tenant_name")))
                sleep(15)
            try_count -= 1
        # If reach here, means the stack delete failed
        self.logger.error('Delete stack (ID:%s) in cloud<%s>_project<%s> fail, stack_status<%s>' % (
            stack.id, self.cred.get("auth_url"), self.cred.get("tenant_name"), stack.stack_status))
        return False

    def resource_str(self, stack):
        return "stack %s" % stack.id


class CinderBase(OpenstackBase):
    def __init__(self, cred=None, **kwargs):
        super(CinderBase, self).__init__(cred, **kwargs)
        self.client = CinderClient(session=self.sess, endpoint_type=self.endpoint_type)


class CinderSnapshots(CinderBase):
    def list(self):
        all_snapshots = self.client.volume_snapshots.list()
        snapshots_list = []
        for snapshot in all_snapshots:
            if snapshot.__getattr__("os-extended-snapshot-attributes:project_id") == self.project_id:
                snapshots_list.append(snapshot)
        return snapshots_list

    def delete(self, snap):
        super(CinderSnapshots, self).delete(snap)
        self.client.volume_snapshots.delete(snap)

    def resource_str(self, snap):
        return "snapshot %s (id %s)" % (snap.name, snap.id)


class CinderLimits(CinderBase):
    def get_cinder_used(self):
        limits = self.client.limits.get(tenant_id=self.project_id)
        for absolute_limit in limits.absolute:
            if absolute_limit.name == "totalGigabytesUsed":
                return absolute_limit.value


class CinderVolumes(CinderBase):
    def list(self):
        all_volumes = self.client.volumes.list()
        volumes_list = []
        for volume in all_volumes:
            if volume.__getattr__("os-vol-tenant-attr:tenant_id") == self.project_id:
                volumes_list.append(volume)
        return volumes_list

    def delete(self, vol):
        """Snapshots created from the volume must be deleted first."""
        super(CinderVolumes, self).delete(vol)
        self.client.volumes.delete(vol)

    def resource_str(self, vol):
        return "volume %s (id %s)".format(vol.name, vol.id)


class NovaBase(OpenstackBase):
    def __init__(self, cred=None, **kwargs):
        super(NovaBase, self).__init__(cred, **kwargs)
        self.client = NovaClient("2", session=self.sess, endpoint_type=self.endpoint_type)


class NovaServers(NovaBase):
    def list(self):
        # tenant_id
        all_servers = self.client.servers.list()
        servers_list = []
        for server in all_servers:
            if server.tenant_id == self.project_id:
                servers_list.append(server)
        return servers_list

    def delete(self, server):
        super(NovaServers, self).delete(server)
        self.client.servers.delete(server)

    def resource_str(self, server):
        return "server {} (id {})".format(server.name, server.id)


class NeutronBase(OpenstackBase):
    def __init__(self, cred=None, **kwargs):
        super(NeutronBase, self).__init__(cred, **kwargs)
        self.client = NeutronClient(session=self.sess, endpoint_type=self.endpoint_type)

    # This method is used for routers and interfaces removal
    def list_routers(self):
        return filter(
            self._owned_resource,
            self.client.list_routers(tenant_id=self.project_id)['routers'])

    def _owned_resource(self, res):
        # Only considering resources owned by project
        # We try to filter directly in the cinderclient.list() commands, but some 3rd
        # party Neutron plugins may ignore the "tenant_id=self.project_id"
        # keyword filtering parameter. An extra check does not cost much and
        # keeps us on the safe side.
        return res['tenant_id'] == self.project_id


class NeutronFloatingIps(NeutronBase):
    def list(self):
        return filter(self._owned_resource,
                      self.client.list_floatingips(
                          tenant_id=self.project_id)['floatingips'])

    def delete(self, floating_ip):
        super(NeutronFloatingIps, self).delete(floating_ip)
        self.client.delete_floatingip(floating_ip['id'])

    @staticmethod
    def resource_str(floating_ip):
        return "floating ip {} (id {})".format(
            floating_ip['floating_ip_address'], floating_ip['id'])


class NeutronInterfaces(NeutronBase):
    def list(self):
        # Only considering "router_interface" ports
        # (not gateways, neither unbound ports)
        all_ports = [
            port for port in self.client.list_ports(
                tenant_id=self.project_id)['ports']
            if port["device_owner"] == "network:router_interface"
        ]
        return filter(self._owned_resource, all_ports)

    def delete(self, interface):
        super(NeutronInterfaces, self).delete(interface)
        self.client.remove_interface_router(interface['device_id'],
                                            {'port_id': interface['id']})

    @staticmethod
    def resource_str(interface):
        return "interface {} (id {})".format(interface['name'],
                                             interface['id'])


class NeutronRouters(NeutronBase):
    def list(self):
        return self.list_routers()

    def delete(self, router):
        """Interfaces must be deleted first."""
        super(NeutronRouters, self).delete(router)
        # Remove router gateway prior to remove the router itself
        self.client.remove_gateway_router(router['id'])
        self.client.delete_router(router['id'])

    @staticmethod
    def resource_str(router):
        return "router %s (id %s)" % (router['name'], router['id'])


class NeutronPorts(NeutronBase):
    # When created, unbound ports' device_owner are "". device_owner
    # is of the form" compute:*" if it has been bound to some vm in
    # the past.
    def list(self):
        all_ports = [
            port for port in self.client.list_ports(
                tenant_id=self.project_id)['ports']
            if port["device_owner"] == ""
            or port["device_owner"].startswith("compute:")
        ]
        return filter(self._owned_resource, all_ports)

    def delete(self, port):
        super(NeutronPorts, self).delete(port)
        self.client.delete_port(port['id'])

    @staticmethod
    def resource_str(port):
        return "port {} (id {})".format(port['name'], port['id'])


class NeutronNetworks(NeutronBase):
    def list(self):
        return filter(self._owned_resource,
                      self.client.list_networks(
                          tenant_id=self.project_id)['networks'])

    def delete(self, net):
        """Delete a Neutron network

        Interfaces connected to the network must be deleted first.
        Implying there must not be any VM on the network.
        """
        super(NeutronNetworks, self).delete(net)
        self.client.delete_network(net['id'])

    @staticmethod
    def resource_str(net):
        return "network {} (id {})".format(net['name'], net['id'])


class NeutronSecgroups(NeutronBase):
    def list(self):
        # filtering out default security group (cannot be removed)
        def secgroup_filter(secgroup):
            if secgroup['name'] == 'default':
                return False
            return self._owned_resource(secgroup)

        try:
            sgs = self.client.list_security_groups(
                tenant_id=self.project_id)['security_groups']
            return filter(secgroup_filter, sgs)
        except NeutronClient.common.exceptions.NeutronClientException as err:
            if getattr(err, "status_code", None) == 404:
                raise Exception( 'Security Group is not enabled! {}.'.format(err) )
            raise Exception( 'Invalid Security Group! {}.'.format(err) )

    def delete(self, secgroup):
        """VMs using the security group should be deleted first."""
        super(NeutronSecgroups, self).delete(secgroup)
        self.client.delete_security_group(secgroup['id'])

    @staticmethod
    def resource_str(secgroup):
        return "security group {} (id {})".format(
            secgroup['name'], secgroup['id'])


class GlanceImages(OpenstackBase):
    def __init__(self, cred=None, **kwargs):
        super(GlanceImages, self).__init__(cred, **kwargs)
        self.client = GlanceClient(session=self.sess)

    def list(self):
        """
        :return: [<Image {u'status': u'active', u'virtual_size': None, u'name': u'test_image1', u'deleted': False,
        u'container_format': u'bare', u'created_at': u'2018-06-21T11:12:36.000000', u'disk_format': u'raw',
        u'updated_at': u'2018-06-21T11:12:45.000000', u'properties': {}, u'owner': u'd2d9df95ced1461f881a36a80657f5c5',
        u'protected': False, u'min_ram': 0, u'checksum': u'8a7ba34ef90e55e048f6535cb4941a44', u'min_disk': 0,
        u'is_public': False, u'deleted_at': None, u'id': u'5f395c6f-7729-4dc4-90c9-9eb6796639e1', u'size': 952041472}>]
        """
        # Glance.images.list() return a generator not a list, so need to create a list
        image_list = []
        for image in self.client.images.list():
            if image.get("owner") == self.project_id:
                image_list.append(image)
        return image_list

    def delete(self, image):
        super(GlanceImages, self).delete(image)
        try:
            self.client.images.delete(image.id)
        except Exception as e:
            image_id = image.get('id', None)
            if image_id is not None:
                self.client.images.delete(image_id)

    def resource_str(self, image):
        return "image {} (id {})".format(getattr(image, 'name', ''), image.id)

    def _owned_resource(self, res):
        # Only considering resources owned by project
        return res.get("owner") == self.project_id
