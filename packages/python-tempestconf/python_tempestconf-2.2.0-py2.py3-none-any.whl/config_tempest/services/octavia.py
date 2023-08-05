# Copyright 2018 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from config_tempest.services.base import VersionedService


class LoadBalancerService(VersionedService):

    def set_versions(self):
        super(LoadBalancerService, self).set_versions(top_level=False)

    def set_default_tempest_options(self, conf):
        conf.set('load_balancer', 'enable_security_groups', 'True')
        conf.set('load_balancer', 'member_role', '_member_')
        conf.set('load_balancer', 'admin_role', 'admin')
        conf.set('load_balancer', 'RBAC_test_type', 'owner_or_admin')

    @staticmethod
    def get_service_name():
        return ['octavia']

    @staticmethod
    def get_codename():
        return 'octavia'
