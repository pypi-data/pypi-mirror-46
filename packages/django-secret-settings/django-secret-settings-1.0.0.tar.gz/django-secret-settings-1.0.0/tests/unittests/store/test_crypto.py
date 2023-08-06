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

import json
from subprocess import CalledProcessError
import unittest
from unittest import mock

from django_secret_settings.store import crypto


class CryptographyFacadeTest(unittest.TestCase):
    def setUp(self):
        crypto.logger = mock.Mock()
        self.under_test = crypto.CryptographyFacade

    @mock.patch('subprocess.run')
    def test_decrypt_decodes_and_deserializes_secret_from_json_representation(self, mock_subprocess_run):
        expected_secret = {
            'SECRET_KEY': 'I will not buy this record, it is scratched.',
        }
        mock_subprocess_run.return_value.stdout = json.dumps(expected_secret).encode('utf-8')

        self.assertEqual(expected_secret, self.under_test.decrypt('file_name', 'private_key_file'))

    @mock.patch('subprocess.run')
    def test_decrypt_logs_and_raises_exception_on_missing_openssl_executable(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = FileNotFoundError("[Errno 2] No such file or directory: 'openssl'")

        with self.assertRaises(crypto.CryptographyError):
            self.under_test.decrypt('file_name', 'private_key_file')

        crypto.logger.exception.assert_called_with('OpenSSL executable not present')

    @mock.patch('subprocess.run')
    def test_decrypt_logs_and_raises_exception_on_decryption_error(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = CalledProcessError(
            cmd="['openssl', 'rsautl', '-decrypt', '-inkey', 'private_key_file', '-in', 'file_name']",
            returncode=1
        )

        with self.assertRaises(crypto.CryptographyError):
            self.under_test.decrypt('file_name', 'private_key_file')

        crypto.logger.exception.assert_called_with('Error decrypting secret')

    @mock.patch('subprocess.run')
    def test_decrypt_logs_and_raises_exception_on_decoding_error(self, mock_subprocess_run):
        mock_stdout = mock.Mock()
        mock_stdout.decode.side_effect = UnicodeDecodeError('utf-8', bytes(), 0, 1, 'whoops')

        mock_subprocess_run.return_value.stdout = mock_stdout

        with self.assertRaises(crypto.CryptographyError):
            self.under_test.decrypt('file_name', 'private_key_file')

        crypto.logger.exception.assert_called_with('Error decoding secret')

    @mock.patch('subprocess.run')
    def test_decrypt_logs_and_raises_exception_on_deserialization_error(self, mock_subprocess_run):
        mock_subprocess_run.return_value.stdout = 'invalid_json'.encode('utf-8')

        with self.assertRaises(crypto.CryptographyError):
            self.under_test.decrypt('file_name', 'private_key_file')

        crypto.logger.exception.assert_called_with('Error deserializing secret')


if __name__ == '__main__':
    unittest.main()
