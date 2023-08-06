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
from unittest import mock

from django_secret_settings.store import secret_store


class SecretStoreTest(unittest.TestCase):
    def setUp(self):
        secret_store.logger = mock.Mock()
        self.under_test = secret_store.SecretStore('store_name', '/store/base/dir', 'private_key_file')

    def test_constructor_initializes_the_secret_store(self):
        self.assertEqual('store_name', self.under_test._store_name)
        self.assertEqual('/store/base/dir', self.under_test._store_base_dir)
        self.assertEqual('private_key_file', self.under_test._private_key_file)

    def test__get_secret_file_name_is_generated_from_store_base_dir(self):
        self.assertEqual('/store/base/dir/secret', self.under_test._get_secret_file_name('secret'))
        self.assertEqual('/store/base/dir/email', self.under_test._get_secret_file_name('email'))

    @mock.patch('django_secret_settings.store.crypto.CryptographyFacade.decrypt')
    def test_get_uses_cryptography_facade_to_decrypt_secret(self, decrypt):
        mock_secret_value = 'secret_value'
        decrypt.return_value = mock_secret_value

        self.assertEqual(mock_secret_value, self.under_test.get('secret_name'))

    @mock.patch('django_secret_settings.store.crypto.CryptographyFacade.decrypt')
    def test_get_uses_given_keys_to_access_structured_data(self, decrypt):
        mock_secret_value = {'key1': {'key2': {'key3': 'value3'}}}
        decrypt.return_value = mock_secret_value

        self.assertEqual(mock_secret_value['key1'], self.under_test.get('secret_name', 'key1'))
        self.assertEqual(mock_secret_value['key1']['key2'], self.under_test.get('secret_name', 'key1', 'key2'))
        self.assertEqual(
            mock_secret_value['key1']['key2']['key3'],
            self.under_test.get('secret_name', 'key1', 'key2', 'key3')
        )

    @mock.patch('django_secret_settings.store.crypto.CryptographyFacade.decrypt')
    def test_get_logs_and_raises_exception_if_key_unpacking_fails_due_to_type_error(self, decrypt):
        mock_secret_value = mock.MagicMock()
        mock_secret_value.__getitem__.side_effect = TypeError('string indices must be integers')

        decrypt.return_value = mock_secret_value

        with self.assertRaises(secret_store.SecretStoreError):
            self.under_test.get('secret_name', 'key')

        secret_store.logger.exception.assert_called_with('Cannot unpack keys')

    @mock.patch('django_secret_settings.store.crypto.CryptographyFacade.decrypt')
    def test_get_logs_and_raises_exception_if_key_unpacking_fails_due_to_key_error(self, decrypt):
        mock_secret_value = mock.MagicMock()
        mock_secret_value.__getitem__.side_effect = KeyError('key')

        decrypt.return_value = mock_secret_value

        with self.assertRaises(secret_store.SecretStoreError):
            self.under_test.get('secret_name', 'key')

        secret_store.logger.exception.assert_called_with('Cannot unpack keys')

    def test_get_name_returns_name_of_the_store(self):
        self.assertEqual('store_name', self.under_test.get_name())


if __name__ == '__main__':
    unittest.main()
