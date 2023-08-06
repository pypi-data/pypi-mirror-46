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

import glob
import logging
import os

from .error import SecretStoreFactoryError
from .secret_store import SecretStore

logger = logging.getLogger(__name__)


class ActiveSecretStoreFactory:
    PRIVATE_KEY_SUFFIX = '.pem'
    SECRET_STORE_DIR = 'secrets'

    @classmethod
    def _get_private_key_file(cls, store_search_dir):
        available_private_key_files = glob.glob('{}/*{}'.format(store_search_dir, cls.PRIVATE_KEY_SUFFIX))
        logger.debug('Found available_private_key_files="{}"'.format(available_private_key_files))

        if len(available_private_key_files) == 0:
            logger.critical('No private key file present')
            raise SecretStoreFactoryError.due_to_missing_private_key_file(store_search_dir)
        elif len(available_private_key_files) > 1:
            logger.critical('Multiple private key files present')
            raise SecretStoreFactoryError.due_to_multiple_private_key_files(store_search_dir)

        private_key_file = available_private_key_files[0]
        logger.debug('Using private_key_file="{}"'.format(private_key_file))
        return private_key_file

    @classmethod
    def _get_store_base_dir(cls, private_key_file):
        store_base_dir = private_key_file.replace(cls.PRIVATE_KEY_SUFFIX, '')
        logger.debug('Resolved store_base_dir="{}"'.format(store_base_dir))
        if not os.path.isdir(store_base_dir):
            logger.warning(
                'The store_base_dir="{}" is not a directory! This means that you do not have any secrets encrypted '
                'with the private_key_file="{}".'.format(store_base_dir, private_key_file)
            )
        return store_base_dir

    @classmethod
    def _get_store_name(cls, store_search_dir, store_base_dir):
        store_name = store_base_dir.replace(store_search_dir + '/', '')
        logger.debug('Determined store_name="{}"'.format(store_name))
        return store_name

    @classmethod
    def _get_store_search_dir(cls, parent_dir):
        store_search_dir = os.path.join(parent_dir, cls.SECRET_STORE_DIR)
        if not os.path.isdir(store_search_dir):
            logger.critical('Secret store search directory missing')
            raise SecretStoreFactoryError.due_to_missing_store_search_dir(cls.SECRET_STORE_DIR, parent_dir)
        logger.debug('Assumed store_search_dir="{}"'.format(store_search_dir))
        return store_search_dir

    @classmethod
    def get_instance(cls, parent_dir):
        store_search_dir = cls._get_store_search_dir(parent_dir)
        private_key_file = cls._get_private_key_file(store_search_dir)
        store_base_dir = cls._get_store_base_dir(private_key_file)
        store_name = cls._get_store_name(store_search_dir, store_base_dir)

        return SecretStore(store_name, store_base_dir, private_key_file)
