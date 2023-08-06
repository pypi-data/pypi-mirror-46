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

import unittest
from unittest.mock import patch, Mock

from django_secret_settings.store import factory


class ActiveSecretStoreFactoryTest(unittest.TestCase):
    def setUp(self):
        factory.logger = Mock()
        self.under_test = factory.ActiveSecretStoreFactory

    @patch('os.path.isdir')
    @patch('glob.glob')
    @patch('django_secret_settings.store.factory.SecretStore')
    def test_get_instance_builds_initialized_secret_store(self, mock_secret_store_class, mock_glob, mock_isdir):
        mock_glob.return_value = ['/parent/dir/secrets/store_name.pem']
        mock_isdir.return_value = True

        self.under_test.get_instance('/parent/dir')

        mock_secret_store_class.assert_called_with(
            'store_name', '/parent/dir/secrets/store_name', '/parent/dir/secrets/store_name.pem'
        )

    def test_get_instance_logs_and_raises_exception_if_store_search_dir_is_not_present(self):
        with self.assertRaises(factory.SecretStoreFactoryError):
            self.under_test.get_instance('/parent/dir')

        factory.logger.critical.assert_called_with('Secret store search directory missing')

    @patch('os.path.isdir')
    def test_get_instance_logs_and_raises_exception_if_no_private_key_is_found(self, mock_isdir):
        mock_isdir.return_value = True

        with self.assertRaises(factory.SecretStoreFactoryError):
            self.under_test.get_instance('/parent/dir')

        factory.logger.critical.assert_called_with('No private key file present')

    @patch('os.path.isdir')
    @patch('glob.glob')
    def test_get_instance_logs_and_raises_exception_if_multiple_private_keys_are_found(self, mock_glob, mock_isdir):
        mock_glob.return_value = ['/parent/dir/secrets/store1.pem', '/parent/dir/secrets/store2.pem']
        mock_isdir.return_value = True

        with self.assertRaises(factory.SecretStoreFactoryError):
            self.under_test.get_instance('/parent/dir')

        factory.logger.critical.assert_called_with('Multiple private key files present')

    @patch('os.path.isdir')
    @patch('glob.glob')
    def test_get_instance_logs_warning_if_store_base_dir_is_not_present(self, mock_glob, mock_isdir):
        mock_glob.return_value = ['/parent/dir/secrets/store_name.pem']
        mock_isdir.side_effect = [True, False]

        self.under_test.get_instance('/parent/dir')

        factory.logger.warning.assert_called_with(unittest.mock.ANY)


if __name__ == '__main__':
    unittest.main()
