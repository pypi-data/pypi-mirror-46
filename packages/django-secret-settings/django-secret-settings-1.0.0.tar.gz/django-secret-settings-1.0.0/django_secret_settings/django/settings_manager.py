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

import importlib
import inspect
import logging
import os

from .error import SettingsManagerError

logger = logging.getLogger(__name__)


class SettingsManager:
    DJANGO_SETTINGS_ENV_VAR = 'DJANGO_SETTINGS_MODULE'

    _settings_package_name = None

    def __init__(self):
        self._settings_package_name = os.environ.get(self.DJANGO_SETTINGS_ENV_VAR)
        if self._settings_package_name is None:
            logger.critical('Environment variable DJANGO_SETTINGS_MODULE unset')
            raise SettingsManagerError.due_to_unset_environment_variable(self.DJANGO_SETTINGS_ENV_VAR)
        logger.debug('Resolved settings_package_name="{}"'.format(self._settings_package_name))

    def get_globals(self, module_name):
        fully_qualified_module_name = '{}.{}'.format(self._settings_package_name, module_name)
        logger.debug('Resolved fully_qualified_module_name="{}"'.format(fully_qualified_module_name))

        try:
            settings_module = importlib.import_module(fully_qualified_module_name)
            logger.info('Successfully imported settings_module="{}"'.format(settings_module))
        except ImportError as import_error:
            logger.exception('Error importing the settings module')
            raise SettingsManagerError.due_to_unavailable_settings_module(fully_qualified_module_name) from import_error

        return settings_module.__dict__

    def get_settings_package_dir(self):
        try:
            settings_package = importlib.import_module(self._settings_package_name)
            logger.debug('Successfully imported settings_package="{}"'.format(settings_package))

            settings_package_dir = inspect.getfile(settings_package).replace('/__init__.py', '')
            logger.info('Determined settings_package_dir="{}"'.format(settings_package_dir))
            return settings_package_dir
        except ImportError as import_error:
            logger.exception('Error importing the settings package')
            raise SettingsManagerError.due_to_unavailable_settings_package(
                self._settings_package_name,
                self.DJANGO_SETTINGS_ENV_VAR
            ) from import_error
        except TypeError as type_error:
            logger.exception('Error determining the path to the settings package')
            raise SettingsManagerError.due_to_settings_package_has_no_dir(self._settings_package_name) from type_error
