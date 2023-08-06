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
import sys
import unittest
from unittest import mock


class DjangoSecretSettingsAutoloadTest(unittest.TestCase):
    def setUp(self):
        self.mock_settings_manager = mock.MagicMock()

        self.mock_settings_manager_module = mock.Mock()
        self.mock_settings_manager_module.SettingsManager.return_value = self.mock_settings_manager

        self.mock_store_factory = mock.Mock()

        self.mock_factory_module = mock.Mock()
        self.mock_factory_module.ActiveSecretStoreFactory.return_value = self.mock_store_factory

        sys.modules['django_secret_settings.django.settings_manager'] = self.mock_settings_manager_module
        sys.modules['django_secret_settings.store.factory'] = self.mock_factory_module

    @staticmethod
    def __do_fresh_import():
        import django_secret_settings.autoload
        importlib.reload(django_secret_settings.autoload)

    def test_active_secret_store_factory_builds_secret_store_based_on_parent_directory_from_settings_manager(self):
        self.mock_settings_manager.get_settings_package_dir.return_value = '/path/to/settings'

        self.__do_fresh_import()

        self.mock_settings_manager_module.SettingsManager.assert_called_with()
        self.mock_settings_manager.get_settings_package_dir.assert_called_with()
        self.mock_factory_module.ActiveSecretStoreFactory.get_instance.assert_called_with('/path/to/settings')

    def test_settings_manager_obtains_globals_based_on_store_name(self):
        mock_secret_store = mock.Mock()
        mock_secret_store.get_name.return_value = 'store_name'

        self.mock_factory_module.ActiveSecretStoreFactory.get_instance.return_value = mock_secret_store

        self.__do_fresh_import()

        mock_secret_store.get_name.assert_called_with()
        self.mock_settings_manager.get_globals.assert_called_with('store_name')

    @mock.patch('django_secret_settings.autoload.locals')
    def test_locals_are_updated_based_on_globals_provided_by_settings_manager(self, mock_locals):
        mock_globals = {'global1': 'value1', 'global2': 'value2'}
        self.mock_settings_manager.get_globals.return_value = mock_globals

        mock_locals_value = mock.Mock()
        mock_locals.return_value = mock_locals_value

        self.__do_fresh_import()

        mock_locals.assert_called_with()
        mock_locals_value.update.assert_called_with(mock_globals)


if __name__ == '__main__':
    unittest.main()
