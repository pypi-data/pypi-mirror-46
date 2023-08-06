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

from .django.settings_manager import SettingsManager
from .store.factory import ActiveSecretStoreFactory


logger = logging.getLogger(__name__)

logger.info('Using django-secret-settings to bootstrap Django settings')

settings_manager = SettingsManager()
secret_store = ActiveSecretStoreFactory.get_instance(settings_manager.get_settings_package_dir())

locals().update(settings_manager.get_globals(secret_store.get_name()))
logger.info('Successfully added * from settings module to the scope')
