# Copyright 2020 The StackStorm Authors.
# Copyright 2019 Extreme Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import logging

from st2client.commands import resource
from st2client.formatters import table
from st2client.models.config_manager import ClientConfig


LOG = logging.getLogger(__name__)


class ConfigMgrBranch(resource.ClientConfigResourceBranch):
    def __init__(self, description, app, subparsers, parent_parser=None):
        super().__init__(
            ClientConfig,
            description,
            app,
            subparsers,
            parent_parser=parent_parser,
        )

        self.commands = {
            "list": ConfigMgrListCommand(self.resource, self.app, self.subparsers)
        }


class ConfigMgrListCommand(resource.ResourceListCommand):

    display_attributes = ["selected", "name", "filepath"]

    def __init__(self, resource, *args, **kwargs):
        kwargs["has_token_opt"] = False

        super().__init__(
            resource,
            *args,
            **kwargs,
        )

        self.resource_name = resource.get_plural_display_name().lower()

    def run(self, args, **kwargs):
        return self.manager.get_client_configs_list()

    def run_and_print(self, args, **kwargs):
        instances = self.run(args, **kwargs)

        self.print_output(
            sorted(instances, key=lambda f: f.name),
            table.MultiColumnTable,
            attributes=args.attr,
            widths=args.width,
            json=args.json,
            yaml=args.yaml,
        )


class ConfigMgrCreateCommand(resource.ResourceCreateCommand):
    def __init__(self, resource, *args, **kwargs):
        kwargs["has_token_opt"] = False

        super().__init__(
            resource,
            *args,
            **kwargs,
        )

    def run(self, args, **kwargs):
        pass

    def run_and_print(self, args, **kwargs):
        pass
