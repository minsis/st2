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

__all__ = [
    "ClientConfig",
    "ClientConfigManager"
]

from re import search
from pathlib import Path

from st2client.models import core
from st2client.config_parser import (
    ST2_CONFIG_DIRECTORY, ST2_CONFIG_PATH,
    ST2_CONFIG_PREFIX, ST2_CONFIG_EXTENSION
)

RE_GLOB = r"{prefix}(.*){extension}".format(
    prefix=ST2_CONFIG_PREFIX,
    extension=ST2_CONFIG_EXTENSION
)


class ClientConfig(core.Resource):
    _alias = "Config"
    _display_name = "Client Config"
    _plural = "ClientConfigs"
    _plural_display_name = "Client Configs"


def _get_selected_client_config_name():
    st2_config_path = Path(ST2_CONFIG_PATH)
    if st2_config_path.is_symlink():
        return search(
            RE_GLOB,
            st2_config_path.resolve().name
        ).group(1)
    return None


class ClientConfigFile(object):
    def __init__(self, config_file_path):
        self._config_file = config_file_path
        self._get_selected_config = _get_selected_client_config_name

    @property
    def config_file(self):
        return self._config_file

    @property
    def selected(self):
        return "yes" if self._get_selected_config() == self.name else ""

    @property
    def name(self):
        return search(
            RE_GLOB,
            self.config_file.name
        ).group(1)

    @property
    def filepath(self):
        return str(self.config_file)

    def __repr__(self):
        return "{class_}(selected='{selected}', name='{name}', filepath='{filepath}')".format(
            class_=self.__class__.__name__,
            selected=self.selected,
            name=self.name,
            filepath=self.filepath
        )


class ClientConfigManager(object):
    def __init__(self, resource):
        self.resource = resource
        self._get_selected_client_config_name = _get_selected_client_config_name

    @property
    def st2_config_path(self):
        return Path(ST2_CONFIG_PATH)

    @property
    def st2_config_directory(self):
        st2_config_directory = Path(ST2_CONFIG_DIRECTORY)
        if not st2_config_directory.exists() or not st2_config_directory.is_dir():
            raise NotADirectoryError("No base st2 client configuration has been created")
        return st2_config_directory

    def get_client_configs_list(self):
        all_config_files = self.st2_config_directory.glob(
            "{prefix}*{extension}".format(
                prefix=ST2_CONFIG_PREFIX,
                extension=ST2_CONFIG_EXTENSION
            )
        )

        return [ClientConfigFile(cfg) for cfg in all_config_files]
