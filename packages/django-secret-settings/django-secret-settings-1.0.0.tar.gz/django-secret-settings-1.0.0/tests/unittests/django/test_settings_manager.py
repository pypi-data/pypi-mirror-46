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

import os
import unittest
from unittest import mock

from django_secret_settings.django import settings_manager


class SettingsManagerTest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.package')
        settings_manager.logger = mock.Mock()
        self.under_test = settings_manager.SettingsManager()

    def test_constructor_sets_settings_package_from_environment_variable(self):
        self.assertEqual('settings.package', self.under_test._settings_package_name)

    def test_constructor_logs_and_raises_exception_if_environment_variable_is_unset(self):
        del os.environ['DJANGO_SETTINGS_MODULE']
        with self.assertRaises(settings_manager.SettingsManagerError):
            self.under_test = settings_manager.SettingsManager()

        settings_manager.logger.critical.assert_called_with('Environment variable DJANGO_SETTINGS_MODULE unset')

    @mock.patch('importlib.import_module')
    def test_get_globals_yields_globals_from_settings_module(self, mock_import_module):
        mock_settings_module = mock.MagicMock()
        mock_import_module.return_value = mock_settings_module

        self.assertEqual(mock_settings_module.__dict__, self.under_test.get_globals('testing'))

    def test_get_globals_logs_and_raises_exception_if_settings_module_cannot_be_imported(self):
        with self.assertRaises(settings_manager.SettingsManagerError):
            self.under_test.get_globals('testing')

        settings_manager.logger.exception.assert_called_with('Error importing the settings module')

    @mock.patch('inspect.getfile')
    @mock.patch('importlib.import_module')
    def test_get_settings_package_dir_returns_path_from_package_inspection(self, mock_import_module, mock_getfile):
        mock_settings_package = mock.Mock()
        mock_import_module.return_value = mock_settings_package

        expected_settings_package_dir = '/path/to/settings/package'
        mock_getfile.return_value = expected_settings_package_dir

        self.assertEqual(expected_settings_package_dir, self.under_test.get_settings_package_dir())

    def test_get_settings_package_dir_logs_and_raises_exception_if_settings_package_cannot_be_imported(self):
        with self.assertRaises(settings_manager.SettingsManagerError):
            self.under_test.get_settings_package_dir()

        settings_manager.logger.exception.assert_called_with('Error importing the settings package')

    @mock.patch('importlib.import_module')
    def test_get_settings_package_dir_raises_exception_if_directory_cannot_be_determined(self, mock_import_module):
        mock_settings_package = mock.Mock()
        mock_import_module.return_value = mock_settings_package

        with self.assertRaises(settings_manager.SettingsManagerError):
            self.under_test.get_settings_package_dir()

        settings_manager.logger.exception.assert_called_with('Error determining the path to the settings package')


if __name__ == '__main__':
    unittest.main()
