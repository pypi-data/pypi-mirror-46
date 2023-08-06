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

MESSAGE_ERROR_ON_DECODING = """Could not decode contents of decrypted file "{}" to UTF-8!
    Private key used for decryption: "{}"
"""
MESSAGE_ERROR_ON_DECRYPTION = """Could not decrypt file "{}" using private key "{}"!
    See log entry of previous exception for details.
"""
MESSAGE_ERROR_ON_DESERIALIZATION = """Could not deserialize decoded JSON content of decrypted file "{}"!
    Private key used for decryption: "{}"
"""
MESSAGE_MISSING_OPENSSL_EXECUTABLE = """Could not find valid OpenSSL executable!
    Need OpenSSL to decrypt file "{}" using private key "{}". You must install it first.
"""


class CryptographyError(DjangoSecretSettingsError):
    @classmethod
    def due_to_error_on_decoding(cls, file_name, private_key_file):
        return cls(MESSAGE_ERROR_ON_DECODING.format(file_name, private_key_file))

    @classmethod
    def due_to_error_on_decryption(cls, file_name, private_key_file):
        return cls(MESSAGE_ERROR_ON_DECRYPTION.format(file_name, private_key_file))

    @classmethod
    def due_to_error_on_deserialization(cls, file_name, private_key_file):
        return cls(MESSAGE_ERROR_ON_DESERIALIZATION.format(file_name, private_key_file))

    @classmethod
    def due_to_missing_openssl(cls, file_name, private_key_file):
        return cls(MESSAGE_MISSING_OPENSSL_EXECUTABLE.format(file_name, private_key_file))


MESSAGE_ERROR_ON_UNPACKING = """Can not unpack keys "{1}" in secret "{0}"!
    To add this, manually decrypt the file with the private key, add the value, and encrypt it again.
"""


class SecretStoreError(DjangoSecretSettingsError):
    @classmethod
    def due_to_error_on_unpacking(cls, secret_name, keys):
        return cls(MESSAGE_ERROR_ON_UNPACKING.format(secret_name, keys))


MESSAGE_MISSING_PRIVATE_KEY_FILE = """Did not find exactly 1 private key in "{0}"!
    If you intend to use the development mode, please create a fake private key by running
    $ touch "{0}/development.pem"
"""
MESSAGE_MISSING_STORE_SEARCH_DIR = """Did not find the store directory "{0}" in the settings directory "{1}"!
    This means that you do not have any secret stores available.
    If this is correct, please create the store directory by running
    $ mkdir "{1}/{0}"
"""
MESSAGE_MULTIPLE_PRIVATE_KEY_FILES = """Found multiple private key files in the store search directory "{}"!
    Please remove all private key files in this directory except the one you intend to use.
    Ambiguity is considered a fatal error for security reasons.
"""


class SecretStoreFactoryError(DjangoSecretSettingsError):
    @classmethod
    def due_to_missing_private_key_file(cls, store_search_dir):
        return cls(MESSAGE_MISSING_PRIVATE_KEY_FILE.format(store_search_dir))

    @classmethod
    def due_to_missing_store_search_dir(cls, secret_store_dir, parent_dir):
        return cls(MESSAGE_MISSING_STORE_SEARCH_DIR.format(secret_store_dir, parent_dir))

    @classmethod
    def due_to_multiple_private_key_files(cls, store_search_dir):
        return cls(MESSAGE_MULTIPLE_PRIVATE_KEY_FILES.format(store_search_dir))
