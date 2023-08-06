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

from .crypto import CryptographyFacade
from .error import SecretStoreError

logger = logging.getLogger(__name__)


class SecretStore:
    _private_key_file = None
    _store_base_dir = None
    _store_name = None

    def __init__(self, store_name, store_base_dir, private_key_file):
        self._store_name = store_name
        self._store_base_dir = store_base_dir
        self._private_key_file = private_key_file
        logger.info(
            'Initialized SecretStore with _store_name="{}", _store_base_dir="{}", _private_key_file="{}"'.format(
                self._store_name,
                self._store_base_dir,
                self._private_key_file
            )
        )

    def _get_secret_file_name(self, secret_name):
        secret_file_name = '{}/{}'.format(self._store_base_dir, secret_name)
        logger.debug('Built secret_file_name="{}"'.format(secret_file_name))

        return secret_file_name

    @staticmethod
    def _unpack_secret_value(secret_dict, keys):
        logger.debug('Trying to unpack keys="{}"'.format(keys))
        for key in keys:
            secret_dict = secret_dict[key]
            logger.debug('Successfully unpacked key="{}"'.format(key))

        return secret_dict

    def get(self, secret_name, *keys):
        secret_dict = CryptographyFacade.decrypt(self._get_secret_file_name(secret_name), self._private_key_file)

        try:
            secret = self._unpack_secret_value(secret_dict, keys)
            logger.info('Resolved secret: secret_name="{}", keys="{}"'.format(secret_name, keys))

            return secret
        except (KeyError, TypeError) as unpack_error:
            logger.exception('Cannot unpack keys')
            raise SecretStoreError.due_to_error_on_unpacking(secret_name, keys) from unpack_error

    def get_name(self):
        return self._store_name
