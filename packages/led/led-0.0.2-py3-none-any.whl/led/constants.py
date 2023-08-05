"""
LED is a Docker utility for Lets Encrypt.
Copyright (C) 2019  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com
"""

import os
from pathlib import PurePath
import sys

platform = sys.platform


##### LED Values #####
LED_BASE_PATH = os.path.abspath(PurePath(__file__).parents[1])

if platform == 'darwin':
    LED_LOG_FILE = os.path.expanduser('~/.local/log/led.log')
elif platform == 'linux':
    LED_LOG_FILE = '/var/log/led.log'
LED_LOG_CONFIG = os.path.join(LED_BASE_PATH, 'conf', 'led_logging.json')
LED_LOG_LEVEL = 'INFO'


##### Certificate Config Values #####
DEFAULT_KEY_SIZE = 3072
KEY_SIZE_MODULUS = 64
MAX_KEY_SIZE = 15360
MAX_REC_KEY_SIZE = 4096
MIN_KEY_SIZE = 2048
# See https://www.johndcook.com/blog/2018/12/12/rsa-exponent/
# -- and --
# https://security.stackexchange.com/a/2339
PUBLIC_EXPONENT = 65537


##### Let's Encrypt Values #####
# These are the API endpoints for ACME-V2 within Let's Encrypt.
PROD_API_URL = 'https://acme-v02.api.letsencrypt.org/directory'
STAG_API_URL = 'https://acme-staging-v02.api.letsencrypt.org/directory'

USER_AGENT = 'LED-v001-ACME-v2'
