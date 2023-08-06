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
import logging
import subprocess

from .error import CryptographyError

logger = logging.getLogger(__name__)


class CryptographyFacade:
    @staticmethod
    def decrypt(file_name, private_key_file):
        try:
            completed_process = subprocess.run(
                ['openssl', 'rsautl', '-decrypt', '-inkey', private_key_file, '-in', file_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            logger.debug(
                'Successfully decrypted file_name="{}" using private_key_file="{}"'.format(
                    file_name,
                    private_key_file
                )
            )

            decoded_secret = completed_process.stdout.decode('utf-8')
            logger.debug('Successfully decoded secret file content')

            secret = json.loads(decoded_secret)
            logger.debug('Successfully deserialized decrypted JSON content')

            return secret
        except FileNotFoundError as file_not_found_error:
            logger.exception('OpenSSL executable not present')
            raise CryptographyError.due_to_missing_openssl(file_name, private_key_file) from file_not_found_error
        except subprocess.CalledProcessError as called_process_error:
            logger.exception('Error decrypting secret')
            raise CryptographyError.due_to_error_on_decryption(file_name, private_key_file) from called_process_error
        except UnicodeDecodeError as unicode_decode_error:
            logger.exception('Error decoding secret')
            raise CryptographyError.due_to_error_on_decoding(file_name, private_key_file) from unicode_decode_error
        except json.JSONDecodeError as json_decode_error:
            logger.exception('Error deserializing secret')
            raise CryptographyError.due_to_error_on_deserialization(file_name, private_key_file) from json_decode_error
