from easy_openstack_api.openstack_resources import *


class OpenstackClient(OpenstackBase):
    def __init__(self, cred, **kwargs):
        super(OpenstackClient, self).__init__(cred, **kwargs)
        self.kwargs = kwargs

    @property
    def resource_clients_list(self):
        if not hasattr(self, "_resource_clients_list"):
            self._resource_clients_list = [
                CinderSnapshots,
                NeutronFloatingIps,
                NovaServers,
                NeutronInterfaces,
                NeutronRouters,
                NeutronPorts,
                NeutronNetworks,
                CinderVolumes,
                GlanceImages,
                HeatStacks,
            ]
        return self._resource_clients_list

    @property
    def keystone_user(self):
        if not hasattr(self, "_keystone_user"):
            self._keystone_user = KeystoneUser
        return self._keystone_user

    @property
    def keystone_endpoint(self):
        if not hasattr(self, "_keystone_endpoint"):
            self._keystone_endpoint = KeystoneEndpoint
        return self._keystone_endpoint

    @property
    def glance_images(self):
        if not hasattr(self, "_glance_images"):
            self._glance_images = GlanceImages
        return self._glance_images

    @property
    def glance_client(self):
        if not hasattr(self, "_glance_client"):
            self._glance_client = GlanceClient(session=self.sess)
        return self._glance_client

    @property
    def nova_client(self):
        if not hasattr(self, "_nova_client"):
            self._nova_client = NovaClient("2", session=self.sess, endpoint_type=self.endpoint_type, **self.kwargs)
        return self._nova_client

    @property
    def keystone_client(self):
        if not hasattr(self, "_keystone_client"):
            self._keystone_client = KeystoneClient(session=self.sess, interface='public', **self.kwargs)
        return self._keystone_client

    @property
    def cinder_client(self):
        if not hasattr(self, "_cinder_client"):
            self._cinder_client = CinderClient(session=self.sess, endpoint_type=self.endpoint_type, **self.kwargs)
        return self._cinder_client

    @property
    def neutron_client(self):
        if not hasattr(self, "_neutron_client"):
            self._neutron_client = NeutronClient(session=self.sess, endpoint_type=self.endpoint_type, **self.kwargs)
        return self._neutron_client

    @property
    def heat_client(self):
        if not hasattr(self, "_heat_client"):
            self._heat_client = HeatClient(1, session=self.sess, endpoint_type=self.endpoint_type,
                                           service_type='orchestration')
        return self._heat_client

    def get_tenant_id_list(self, tenant_name_list):
        tenant_list = self.keystone_client.tenants.list()
        tenant_id_list = []
        # Should I change the searching way?
        for tenant in tenant_list:
            if tenant.name in tenant_name_list:
                tenant_id_list.append(tenant.id)
        return tenant_id_list

    def get_tenant_id(self, tenant_name=None):
        if tenant_name is None:
            tenant_name = self.cred.get("tenant_name")
        tenant_list = self.keystone_client.tenants.list()
        for tenant in tenant_list:
            if tenant.name == tenant_name:
                tenant_id = tenant.id
                return tenant_id
        return None

    def get_service_id(self, service_name):
        service_list = self.keystone_client.services.list()
        for s in service_list:
            if s.name == service_name:
                return s.id

    def get_endpoint_url(self, service_name, endpoint_type):
        """
        :param service_name:
        :param endpoint_type: adminurl, internalurl, publicurl
        :return:
        """
        service_id = self.get_service_id(service_name)
        endpoint_list = self.keystone_client.endpoints.list()
        for e in endpoint_list:
            if e.service_id == service_id:
                return getattr(e, endpoint_type)

    def tenant_network_is_exist(self, network_name):
        network_list = list(self.neutron_client.list_networks().values())[0]
        network_name_list = []
        for network in network_list:
            network_name_list.append(network['name'])
        if network_name in network_name_list:
            return True
        else:
            return False

    def create_tenant(self, tenant_name):
        try:
            tenant = self.keystone_client.tenants.create(tenant_name)
            return tenant
        except Exception as e:
            self.logger.error("Exception: create tenant \"%s\" fail. %s" % (tenant_name, e))

    def create_user(self, tenant_id, user_name, user_pwd):
        # create user connect to the tenant
        try:
            user = self.keystone_client.users.create(user_name, password=user_pwd, tenant_id=tenant_id, enabled=True)
        except Exception as e:
            self.logger.error("Exception: create user \"%s\" fail. %s" % (user_name, e))
            user = None
        if user is not None:
            tenant = self.keystone_client.tenants.get(tenant_id)
            roles_list = self.keystone_client.roles.list()
            for role in roles_list:
                if role.name == 'admin':
                    self.keystone_client.roles.add_user_role(user=user, role=role, tenant=tenant)
                elif role.name == 'heat_stack_owner':
                    self.keystone_client.roles.add_user_role(user=user, role=role, tenant=tenant)
        return user

    def update_quota(self, tenant_id, instances, cpus, rams, volumes, networks, subnets, ports, routers):
        # update quotas
        try:
            self.nova_client.quotas.update(tenant_id, instances=instances, cores=cpus, ram=rams)
            self.cinder_client.quotas.update(tenant_id, volumes=volumes, snapshots=volumes)
            self.update_neutron_quota(tenant_id, networks, subnets, ports, routers)
        except Exception as e:
            self.logger.error("Exception: update quota of tenant_id \"%s\" fail. %s" % (tenant_id, e))

    def update_neutron_quota(self, tenant_id, networks, subnets, ports, routers):
        neutron_quota = self.neutron_client.show_quota(tenant_id)
        neutron_quota_value = neutron_quota['quota']
        neutron_quota_value['subnet'] = subnets
        neutron_quota_value['network'] = networks
        neutron_quota_value['router'] = routers
        neutron_quota_value['port'] = ports
        neutron_quota['quota'] = neutron_quota_value
        self.neutron_client.update_quota(tenant_id, body=neutron_quota)

    def create_flavor(self, name, id, ram, root_disk, vcpu, flavor_keys, cpu_policy):
        flavor_keys_list = flavor_keys.split()
        metadata = {}
        for keypair in flavor_keys_list:
            keypair_dict = keypair.split('=')
            uni_key = keypair_dict[0]
            uni_value = keypair_dict[1]
            metadata.setdefault(uni_key, uni_value)
        metadata.setdefault('hw:cpu_policy', cpu_policy)
        try:
            new_flavor = self.nova_client.flavors.create(name, ram, vcpu, root_disk, id)
            new_flavor.set_keys(metadata)
            return new_flavor
        except Exception as e:
            self.logger.error("Exception: creat flavor \"%s\" fail. %s" % (name, e))

    def get_user_by_name(self, name):
        user_list = self.keystone_client.users.list()
        for user in user_list:
            if user.name == name:
                return user

    def get_role_by_name(self, name):
        roleslist = self.keystone_client.roles.list()
        for role in roleslist:
            if role.name == name:
                return role

    def add_user_to_tenant(self, user, role, tid):
        user_t = self.get_user_by_name(user)
        role_t = self.get_role_by_name(role)
        try:
            self.keystone_client.tenants.add_user(tenant=tid, user=user_t, role=role_t)
        except Exception as e:
            self.logger.error(
                "Exception: Add user \"%s\" to tenant \"%s\" as role \"%s\" failed. %s" % (user, tid, role, e))

    def get_networks(self):
        try:
            return list(self.neutron_client.list_networks().values())[0]
        except Exception as e:
            self.logger.error("Exception: get_networks fail. %s" % e)

    def get_network(self, network):
        """

        :param network: Network name
        :return: network information.
        """
        try:
            nets = list(self.neutron_client.list_networks().values())[0]
        except Exception as e:
            self.logger.error("Exception: get_network \"%s\" fail. %s" % (network, e))
            return None

        for net in nets:
            if net['name'] == network:
                return net
        return None

    def get_subnets(self):
        try:
            return list(self.neutron_client.list_subnets().values())[0]
        except Exception as e:
            self.logger.error("Exception: get_subnets fail. %s" % e)

    def get_subnet(self, subnet_id):
        try:
            subnet = self.neutron_client.show_subnet(subnet=subnet_id)
            return subnet["subnet"]
        except Exception as e:
            self.logger.error("Exception: get_network \"%s\" fail. %s" % (subnet_id, e))

    def get_ports(self):
        try:
            return list(self.neutron_client.list_ports().values())[0]
        except Exception as e:
            self.logger.error("Exception: get_ports fail. %s" % e)

    def get_hypervisor_states(self):
        try:
            hs = self.nova_client.hypervisor_stats.statistics()
            return {'vcpu_total': hs.vcpus, 'vcpu_used': int(hs.vcpus_used),
                    'vcpu_free': hs.vcpus - int(hs.vcpus_used),
                    'ram_total': hs.memory_mb, 'ram_used': hs.memory_mb_used,
                    'ram_free': hs.free_ram_mb, 'disk_total': hs.local_gb,
                    'disk_used': hs.local_gb_used, 'disk_free': hs.free_disk_gb,
                    'cinder_total': 0} if hs else None
        except Exception as e:
            self.logger.error("Exception: get_hypervisor_states fail. %s" % e)

    def get_floating_ips(self):
        try:
            return self.neutron_client.list_floatingips()['floatingips']
        except Exception as e:
            self.logger.error("Exception: get_floating_ips fail. %s" % e)

    def tenant_usage(self, tenant_id, start, end):
        try:
            return self.nova_client.usage.get(tenant_id, start, end)
        except Exception as e:
            self.logger.error("Exception: list_network_ip_availabilities fail. %s" % e)

    def list_network_ip_availabilities(self):
        return self.neutron_client.list_network_ip_availabilities()['network_ip_availabilities']

    def list_alarms(self):
        # need to be rewrite in children class
        return []

    def get_servers(self, project_id):
        result_list = []
        server_list = self.nova_client.servers.list(search_opts={'all_tenants': 1, 'tenant_id': project_id})
        for server in server_list:
            result_list.append({'server': server.id, 'flavor_id': server.flavor.get('id')})
        return result_list

    def get_flavor_by_id(self, flavor_id):
        try:
            flavor = self.nova_client.flavors.get(flavor_id)
            return {'vcpus': flavor.vcpus, 'ram': flavor.ram,
                    'disk': flavor.disk, 'ephemeral': flavor.ephemeral}
        except nova_exceptions.NotFound:
            self.logger.warning('Flavor %s not found' % flavor_id)
            return None

    def get_tenant_id_from_user(self, user_name):
        try:
            return self.keystone_client.users.find(name=user_name).default_project_id
        except keystone_exceptions.NotFound:
            return None

    def get_project_name_from_project_id(self, project_id):
        try:
            project_list = self.keystone_client.projects.list()
            for project in project_list:
                if project.id == project_id:
                    return project.name
        except keystone_exceptions.NotFound:
            return None

    def get_cinder_usage(self, cred=None, session=None):
        if cred:
            project_limits = CinderLimits(cred, session=session)
        else:
            project_limits = CinderLimits(self.cred, session=self.sess)
        return project_limits.get_cinder_used()

    def get_vim_version(self):
        raise NoGetVIMMethod()

    def query_patch(self):
        raise NoQueryPatchMethod()

    def get_endpoint(self, service, interface="public"):
        return self.keystone_endpoint(cred=self.cred, session=self.sess).get(service=service, interface=interface)

    def get_one_available_zone_name(self):
        self.logger.info("===================start list zones===================")
        zones = self.nova_client.availability_zones.list()
        self.logger.info("Zone list: %s" % list(zones))
        for zone in zones:
            if zone.zoneState["available"] is True and zone.zoneName != "internal":
                self.logger.info("Got a zone: %s" % zone)
                return zone.zoneName

    def prepare_single_image_by_name(self, image_file_path, image_name="rocky_image", force_create=False, container_format="bare",
                     disk_format="qcow2", timeout=1800):
        """
        Find images by name. If there are multiple images, delete images to leave only one image. If no image, create a image.
        :param image_file_path: str. The image file stored path.
        :param image_name:
        :param force_create: boolean. If force_create is true, function will delete all the found images, and create a new one.
        :param container_format:
        :param disk_format:
        :param timeout: integer. Timeout for waiting until the created image is active.
        :return:
        """
        self.logger.info("===================start create_or_get_image===================")
        image_list = self.glance_client.images.list(filters={"name": image_name})
        image_list = list(image_list)
        self.logger.info("Image list: %s" % image_list)
        while len(image_list) > 1:
            self.glance_client.images.delete(image_list.pop().id)
        else:
            if len(image_list) == 1:
                if force_create:
                    image = image_list.pop()
                    self.glance_client.images.delete(image.id)
                    self.logger.info("Delete image: %s" % image)
                else:
                    image = image_list.pop()
                    self.logger.info("Got a image, image:\n%s" % image)
                    return image
        image = self.create_image(image_file_path, image_name, container_format, disk_format, timeout)
        self.logger.info(("Created a image: %s" % image))
        return image

    def create_image(self, image_file_path, image_name="rocky_image", container_format="bare", disk_format="qcow2", timeout=1800):
        self.logger.info("===================start create image===================")
        with open(image_file_path, "rb") as image_file:
            image_kwargs = {
                "container_format": container_format,
                "disk_format": disk_format,
                "name": image_name
            }
            image = self.glance_client.images.create(**image_kwargs)
            self.glance_client.images.upload(image_id=image.id, image_data=image_file)
        self.logger.info("Creating image: %s" % image)
        wait_time = 0
        while wait_time <= timeout:
            sleep(5)
            wait_time += 5
            image = self.glance_client.images.get(image.id)
            self.logger.info("Image status is %s" % image.status)
            if image.status == "queued":
                continue
            elif image.status == "active":
                break
            else:
                raise Exception("Create image fail, image status is %s" % image.status)
        else:
            raise Exception("Created image timeout, wait_time is %s" % timeout)
        return image

    def get_or_create_one_key_pair_name(self):
        self.logger.info("===================start get key pair===================")
        key_pairs = self.nova_client.keypairs.list()
        if len(key_pairs) == 0:
            key_pair = self.nova_client.keypairs.create(name="probe_key_pair")
            self.logger.info("Created a key pair: %s" % key_pair)
        else:
            key_pair = key_pairs[0]
            self.logger.info("Got a key pair: %s" % key_pair)
        return key_pair.name

    def prepare_huge_page_flavor(self, name, ram, vcpus, disk, force_create=False):
        self.prepare_flavor(name, ram, vcpus, disk,
                            spec_kwargs={"hw:mem_page_size": "large"}, force_create=force_create)

    def prepare_flavor(self, name, ram, vcpus, disk, spec_kwargs=None, force_create=False):
        self.logger.info("===================start create flavor===================")
        flavor_list = self.nova_client.flavors.list()
        self.logger.info("Flavor list: %s" % flavor_list)
        for flavor in flavor_list:
            if flavor.name == name:
                if force_create is True:
                    self.nova_client.flavors.delete(flavor)
                    self.logger.info("Delete flavor: %s" % flavor)
                else:
                    self.logger.info("Get a flavor: %s" % flavor)
                    return flavor
        flavor = self.nova_client.flavors.create(name=name, ram=ram, vcpus=vcpus, disk=disk)
        if isinstance(spec_kwargs, dict):
            flavor.set_keys(spec_kwargs)
        self.logger.info("Create a flavor: %s" % flavor)

    def prepare_security_group_rule(self, rule_kwargs):
        """
        Create security group rule with the rule_kwargs. If there is rule with rule_kwargs exist, firstly delete it then
        create a new one.
        :param rule_kwargs:
        :return: dict, security group rule.
        """
        rule_list = self.neutron_client.list_security_group_rules(**rule_kwargs)["security_group_rules"]
        self.logger.info("S_g rule list: %s" % rule_list)
        for rule in rule_list:
            self.neutron_client.delete_security_group_rule(rule["id"])
            self.logger.info("Deleted s_g rule: %s" % rule)
        rule = self.neutron_client.create_security_group_rule({"security_group_rule": rule_kwargs})
        self.logger.info("Created s_g rule: %s" % rule)
        return rule

    def prepare_all_pass_security_group(self, name="rocky_sg"):
        """
        Create all pass security group by name. If group exist, delete it and create new one.
        :param name:
        :return: dict, security group.
        """
        self.logger.info("===================start create security group===================")
        security_group_list = self.neutron_client.list_security_groups(
            project_id=self.project_id, name=name)['security_groups']
        self.logger.info("Security group list: %s" % security_group_list)
        for s_g in security_group_list:
            self.neutron_client.delete_security_group(s_g["id"])
            self.logger.info("Deleted security group: %s" % s_g)
        body = self.neutron_client.create_security_group({"security_group": {"name": name, "description": name}})
        security_group = body["security_group"]
        self.logger.info("Created security group: %s" % body)
        self.logger.info("===================start prepare security group rule===================")
        rule_in_v4 = {
            "ethertype": "IPv4", "direction": "ingress", "remote_ip_prefix": "0.0.0.0/0",
            "security_group_id": security_group["id"]
        }
        self.logger.info("Ingress v4 rule")
        self.prepare_security_group_rule(rule_in_v4)
        rule_in_v6 = {
            "ethertype": "IPv6", "direction": "ingress", "remote_ip_prefix": "::/0",
            "security_group_id": security_group["id"]
        }
        self.logger.info("Ingress v6 rule")
        self.prepare_security_group_rule(rule_in_v6)
        rule_e_v4 = {
            "ethertype": "IPv4", "direction": "egress",
            "security_group_id": security_group["id"]
        }
        self.logger.info("Egress v4 rule")
        self.prepare_security_group_rule(rule_e_v4)
        rule_e_v6 = {
            "ethertype": "IPv6", "direction": "egress",
            "security_group_id": security_group["id"]
        }
        self.logger.info("Egress v6 rule")
        self.prepare_security_group_rule(rule_e_v6)
        return security_group

    def delete_stack(self, stack_name, timeout=1800):
        # list stack
        stack_list = self.heat_client.stacks.list(filters={"project": self.project_id, "stack_name": stack_name})
        stack_list = list(stack_list)
        self.logger.info("Stack list: %s" % stack_list)

        # delete stack
        for stack in stack_list:
            self.heat_client.stacks.delete(stack.id)
            self.logger.info("Deleting stack: %s" % stack)
        wait_time = 0
        for stack in stack_list:
            while wait_time <= timeout:
                sleep(10)
                wait_time += 10
                _stack = self.heat_client.stacks.get(stack.id)
                if _stack.stack_status == "DELETE_COMPLETE":
                    self.logger.info("Delete stack ok: %s" % _stack)
                    break
                elif _stack.stack_status == "DELETE_FAILED":
                    raise Exception("Delete stack failed: %s" % _stack)
                else:
                    self.logger.info("Deleting stack, stack status: %s" % _stack.stack_status)
            else:
                raise Exception("Delete stack timeout<%s>: %s" % (timeout, _stack))

    def trigger_deploy_one_server_stack(
            self, image_file_path, external_networks_list, image_name="rocky_image", flavor_name="rocky_flavor",
            flavor_ram=4096, flavor_vcpu=2, flavor_disk=30, stack_name="rocky_stack", server_name="rocky_server",
            security_group_name="rocky_sg", timeout=1800, force_create_image=False, force_create_flavor=False,
            user_data=""):
        """
        Function will perform whole steps for creating a stack which only have one server. Steps are:
        prepare image, prepare flavor, find available zone, prepare key pair, create stack.
        Function will trigger creating stack, but will not wait until stack create completed.
        :param image_file_path:
        :param external_networks_list:
        :param image_name:
        :param flavor_name:
        :param flavor_ram:
        :param flavor_vcpu:
        :param flavor_disk:
        :param stack_name:
        :param server_name:
        :param security_group_name:
        :param timeout:
        :param force_create_image:
        :param force_create_flavor:
        :param user_data: string. The user data for the server.
        :return: dict. Stack info,e.g.{u'stack': {u'id': u'xxx', u'links': [{u'href': u'xxx', u'rel': u'xxx'}]}}
        """
        if len(external_networks_list) <= 0:
            raise Exception("No external_networks input.")

        self.delete_stack(stack_name, timeout)

        # get zone
        zone_name = self.get_one_available_zone_name()
        if zone_name is None:
            raise Exception("No available_zone.")

        # get key pair
        key_pair_name = self.get_or_create_one_key_pair_name()

        # create security group
        self.prepare_all_pass_security_group(security_group_name)

        # create flavor
        self.prepare_huge_page_flavor(flavor_name, flavor_ram, flavor_vcpu, flavor_disk, force_create=force_create_flavor)

        # create image
        self.prepare_single_image_by_name(image_file_path, image_name, force_create=force_create_image)

        # create stack start
        self.logger.info("===================start create stack===================")
        heat_kwargs = {
            "disable_rollback": True,
            "parameters": {},
            "stack_name": stack_name,
            "environment": {},
            "template": {
                "heat_template_version": "2016-10-14",
                "description": "NA",
                "resources": {
                    "server": {
                        "type": "OS::Nova::Server",
                        "properties": {
                            "flavor": flavor_name,
                            "name": server_name,
                            "availability_zone": zone_name,
                            "key_name": key_pair_name,
                            "image": image_name,
                            "user_data": user_data,
                            "networks": [],
                            "config_drive": True
                        }
                    }
                }
            }
        }
        net_num = 0
        for ext_net in external_networks_list:
            net_num += 1
            port_name = "port%s" % net_num
            heat_kwargs["template"]["resources"].update({
                port_name: {
                    "type": "OS::Neutron::Port",
                    "properties": {
                        "network": ext_net,
                        "security_groups": [security_group_name]
                    }
                }
            })
            heat_kwargs["template"]["resources"]["server"]["properties"]["networks"].append(
                {"port": {"get_resource": port_name}})
        heat_kwargs["template"].update({
            "outputs": {
                "oam_ip": {
                    "value": {
                        "get_attr": [port_name, "fixed_ips", 0, "ip_address"]
                    }
                }
            }
        })

        # create stack
        body = self.heat_client.stacks.create(**heat_kwargs)
        self.logger.info("Creating stack, body: %s" % body)
        return body

    def deploy_one_server_stack(self, image_file_path, external_networks_list, image_name="rocky_image",
                                flavor_name="rocky_flavor", flavor_ram=4096, flavor_vcpu=2, flavor_disk=30,
                                stack_name="rocky_stack", server_name="rocky_server", timeout=1800,
                                force_create_image=False, force_create_flavor=False, security_group_name="rocky_sg",
                                user_data=""):
        """
        Function will first call self method 'trigger_deploy_one_server_stack', then wait until the stack is create
        completed.
        :param image_file_path:
        :param external_networks_list:
        :param image_name:
        :param flavor_name:
        :param flavor_ram:
        :param flavor_vcpu:
        :param flavor_disk:
        :param stack_name:
        :param server_name:
        :param timeout:
        :param force_create_image:
        :param force_create_flavor:
        :param security_group_name:
        :param user_data: string. The user data for the server.
        :return:
        """
        body = self.trigger_deploy_one_server_stack(
            image_file_path, external_networks_list, image_name=image_name, flavor_name=flavor_name,
            flavor_ram=flavor_ram, flavor_vcpu=flavor_vcpu, flavor_disk=flavor_disk, stack_name=stack_name,
            server_name=server_name, timeout=timeout, force_create_image=force_create_image,
            force_create_flavor=force_create_flavor, security_group_name=security_group_name, user_data=user_data
        )
        wait_time = 0
        while wait_time <= timeout:
            sleep(10)
            wait_time += 10
            stack = self.heat_client.stacks.get(body["stack"]["id"])
            if stack.stack_status == "CREATE_COMPLETE":
                break
            elif stack.stack_status == "CREATE_FAILED":
                raise Exception("Create stack fail: %s" % stack)
            else:
                self.logger.info("Creating stack: %s" % stack)
        else:
            raise Exception("Creating stack<%s> blocking in status<%s>." % (stack.stack_name, stack.stack_status))
        self.logger.info("Stack create ok: %s" % stack)
        return stack

    def get_external_networks(self):
        kwargs = {"router:external": True}
        self.logger.info("===================start list networks===================")
        external_networks = self.neutron_client.list_networks(**kwargs)["networks"]
        re_list = []
        for network in external_networks:
            self.logger.info("name:%s, external:%s" % (network["name"], network["router:external"]))
            re_list.append(network["name"])
        self.logger.info("===================end list networks===================")
        return re_list

    def list_external_networks_with_cidr(self):
        kwargs = {"router:external": True}
        external_networks = list(self.neutron_client.list_networks(**kwargs).values())[0]
        network_list = []
        ip_list = []
        mask_list = []
        for network in external_networks:
            network_list.append(network.get("name"))
            subnet_id_list = network.get("subnets")
            tag_find_ip_mask = False
            for subnet_id in subnet_id_list:
                subnet_list = list(self.neutron_client.list_subnets(id=subnet_id).values())[0]
                for subnet in subnet_list:
                    if subnet.get("ip_version") == 4:
                        ip_mask = subnet.get("cidr", "").split("/")
                        tag_find_ip_mask = True
                        ip_list.append(ip_mask[0])
                        mask_list.append(ip_mask[-1])
                        break
                if tag_find_ip_mask:
                    break
        return network_list, ip_list, mask_list

    def get_network_gateway(self, network_name):
        networks = self.neutron_client.list_networks(name=network_name)["networks"]
        if len(networks) == 0:
            raise Exception("No network with name %s found." % network_name)
        subnet_id_list = networks[0]["subnets"]
        for subnet_id in subnet_id_list:
            subnet_list = self.neutron_client.list_subnets(id=subnet_id, ip_version=4)["subnets"]
            if len(subnet_list) > 0:
                return subnet_list[0]["gateway_ip"]

    def get_servers_with_net_info(self):
        """
        list servers and add net_info to server object.
        server.net_info = {
        u'RCP-1234-internal-net': {
            'mac': 'fa:16:3e:38:b4:d5',
            'allowed_address_pairs': [{"ip_address": "192.168.1.0/24", "mac_address": "fa:16:3e:95:6a:d8"}],
            'subnets': {
                u'58ec5872-a3eb-4736-bde7-11dce2e6d904': {
                    'ip_version': 4, 'subnet_name': u'RCP-1234-internal-subnet',
                    'cidr': u'192.168.1.0/24', 'ip_address': u'192.168.1.12',
                    'allocation_pools': [{u'start': u'192.168.1.2', u'end': u'192.168.1.205'}]
                }
            }
        :return:
        """
        servers = self.nova_client.servers.list()
        result = []
        for server in servers:
            if server.tenant_id == self.project_id:
                server.net_info = {}
                for net_name, subnet in server.addresses.items():
                    port = list(self.neutron_client.list_ports(mac_address=subnet[0]["OS-EXT-IPS-MAC:mac_addr"]).values())[0][0]
                    server.net_info[net_name] = {"mac": port["mac_address"],
                                                 "subnets": {},
                                                 "allowed_address_pairs": port["allowed_address_pairs"]}
                    for i in port["fixed_ips"]:
                        subnet = list(self.neutron_client.list_subnets(id=i["subnet_id"]).values())[0][0]
                        server.net_info[net_name]["subnets"].update(
                            {
                                i["subnet_id"]: {
                                    "ip_address": i["ip_address"],
                                    "cidr": subnet["cidr"],
                                    "allocation_pools": subnet["allocation_pools"],
                                    "subnet_name": subnet["name"],
                                    "ip_version": subnet["ip_version"]
                                }
                            }
                        )
                result.append(server)
        return result


