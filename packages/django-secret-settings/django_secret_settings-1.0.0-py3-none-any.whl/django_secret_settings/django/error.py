# Copyright 2019 Carsten E. Mahr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..error import DjangoSecretSettingsError

MESSAGE_SETTINGS_PACKAGE_HAS_NO_DIR = """Unable to determine the path to the settings module "{}"!
    Given that the secrets must reside in the settings directory, this package won't do.
"""
MESSAGE_UNAVAILABLE_SETTINGS_MODULE = """Unable to import the settings module "{}"!
    Verify that the module is on the import path.
"""
MESSAGE_UNAVAILABLE_SETTINGS_PACKAGE = """Unable to determine the path to the settings package "{}"!
    Verify that the environment variable "{}" is set correctly and that the module is on the import path.
"""
MESSAGE_UNSET_ENVIRONMENT_VARIABLE = """Unable to determine the settings package name!
    Make sure that the environment variable "{}" is set.
"""


class SettingsManagerError(DjangoSecretSettingsError):
    @classmethod
    def due_to_settings_package_has_no_dir(cls, package_name):
        return cls(MESSAGE_SETTINGS_PACKAGE_HAS_NO_DIR.format(package_name))

    @classmethod
    def due_to_unavailable_settings_module(cls, fully_qualified_module_name):
        return cls(MESSAGE_UNAVAILABLE_SETTINGS_MODULE.format(fully_qualified_module_name))

    @classmethod
    def due_to_unavailable_settings_package(cls, package_name, environment_variable):
        return cls(MESSAGE_UNAVAILABLE_SETTINGS_PACKAGE.format(package_name, environment_variable))

    @classmethod
    def due_to_unset_environment_variable(cls, environment_variable):
        return cls(MESSAGE_UNSET_ENVIRONMENT_VARIABLE.format(environment_variable))
