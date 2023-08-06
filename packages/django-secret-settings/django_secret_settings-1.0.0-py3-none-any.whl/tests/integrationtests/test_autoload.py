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

import logging
import os
import sys
import unittest

from django_secret_settings.django.error import SettingsManagerError
from django_secret_settings.store.error import CryptographyError, SecretStoreError, SecretStoreFactoryError


class DjangoSecretSettingsAutoloadIntegrationTest(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        pass

    def tearDown(self):
        logging.disable(logging.NOTSET)
        os.environ.clear()
        try:
            del sys.modules['django_secret_settings.autoload']
        except KeyError:
            pass

    @staticmethod
    def _use_settings_fixture(package_name):
        os.environ.setdefault(
            'DJANGO_SETTINGS_MODULE',
            'tests.integrationtests.settings_fixtures.{}'.format(package_name)
        )

    def test_settings_manager_raises_exception_if_django_environment_variable_unset(self):
        with self.assertRaises(SettingsManagerError):
            import django_secret_settings.autoload

    def test_settings_manager_raises_exception_if_settings_package_unavailable(self):
        self._use_settings_fixture('nonexistent')
        with self.assertRaises(SettingsManagerError):
            import django_secret_settings.autoload

    def test_secret_store_factory_raises_exception_if_settings_package_empty(self):
        self._use_settings_fixture('empty')
        with self.assertRaises(SecretStoreFactoryError):
            import django_secret_settings.autoload

    def test_secret_store_factory_raises_exception_if_no_private_key_present(self):
        self._use_settings_fixture('no_private_key')
        with self.assertRaises(SecretStoreFactoryError):
            import django_secret_settings.autoload

    def test_secret_store_factory_raises_exception_if_multiple_private_key_present(self):
        self._use_settings_fixture('two_private_keys')
        with self.assertRaises(SecretStoreFactoryError):
            import django_secret_settings.autoload

    def test_settings_manager_raises_exception_if_corresponding_settings_module_unavailable(self):
        self._use_settings_fixture('missing_module')
        with self.assertRaises(SettingsManagerError):
            import django_secret_settings.autoload

    def test_development_settings_are_imported_successfully(self):
        self._use_settings_fixture('unencrypted')
        import django_secret_settings.autoload
        self.assertTrue(hasattr(django_secret_settings.autoload, 'SECRET_KEY'))
        self.assertEqual('My h0v3rcraft is fu11 of eels.', django_secret_settings.autoload.SECRET_KEY)

    def test_encrypted_settings_are_imported_successfully(self):
        self._use_settings_fixture('encrypted')
        import django_secret_settings.autoload
        self.assertTrue(hasattr(django_secret_settings.autoload, 'SECRET_KEY'))
        self.assertEqual('I will not buy this record, it is scratched.', django_secret_settings.autoload.SECRET_KEY)
        self.assertTrue(hasattr(django_secret_settings.autoload, 'EMAIL_HOST_USER'))
        self.assertEqual('the_user_name', django_secret_settings.autoload.EMAIL_HOST_USER)
        self.assertTrue(hasattr(django_secret_settings.autoload, 'EMAIL_HOST_PASSWORD'))
        self.assertEqual('the_very_secret_password', django_secret_settings.autoload.EMAIL_HOST_PASSWORD)

    def test_cryptography_facade_raises_exception_if_secret_file_unavailable(self):
        self._use_settings_fixture('missing_secret_file')
        with self.assertRaises(CryptographyError):
            import django_secret_settings.autoload

    def test_secret_store_raises_exception_if_secret_cannot_be_unpacked(self):
        self._use_settings_fixture('missing_secret_key')
        with self.assertRaises(SecretStoreError):
            import django_secret_settings.autoload


if __name__ == '__main__':
    unittest.main()
