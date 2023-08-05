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
import sys
import warnings

import yaml

from led.constants import (
    LED_BASE_PATH, MIN_KEY_SIZE, MAX_KEY_SIZE,
    MAX_REC_KEY_SIZE, KEY_SIZE_MODULUS
)
from led.error import ErrReason, ExitCode, KeySizeError, LEDError
from led.log import get_logger
from led.utils import new_warn_format, get_dir

CONFIG_FILE = os.path.join(LED_BASE_PATH, 'config.yaml')

warnings.formatwarning = new_warn_format
logger = get_logger(__name__)


class Namespace(object):
    """Simple object for storing attributes.

    Implements equality by attribute names and values.
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__


class Config(object):
    """docstring for Config"""

    def __init__(self, config_file=None):
        self._namespace = Namespace()

        base_config = self._load_config()

        self.certificates = base_config['certificates']
        self.contact_email = base_config['contact_email']
        self.rsa_key_size = base_config['rsa_key_size']
        self.service_name = base_config['service_name']
        self.staging = base_config['staging']
        self.work_dir = base_config['work_dir']

    @staticmethod
    def _load_config():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as stream:
            data = yaml.full_load(stream)

        return data

    @property
    def certificates(self):
        """A dictionary of requested certificates

        The keys are the domains for which a certificate should be issued and
        the values are a list of alternate names for which the certificate
        should be valid. If there is only one domain, it should still be
        provided as both the key and the value with the value represented as
        a single element list.
        """
        pass

    @certificates.setter
    def certificates(self, value):
        # for k, v in value:
        #    logger.info(f"Setting certifcate in config: {k}={k[v]}")
        setattr(self._namespace, 'certificates', value)

    @property
    def contact_email(self):
        pass

    @contact_email.setter
    def contact_email(self, value):
        logger.info(f"Setting contact_email in config: {value}")
        setattr(self._namespace, 'contact_email', value)

    @property
    def rsa_key_size(self):
        """The length of the modulus in bits.

        See https://en.wikipedia.org/wiki/Key_size for more information.
        """
        pass

    @rsa_key_size.setter
    def rsa_key_size(self, value):
        if value < MIN_KEY_SIZE:
            raise KeySizeError(value, ErrReason.TOO_SMALL)
        elif value > MAX_KEY_SIZE:
            raise KeySizeError(value, ErrReason.TOO_LARGE)
        if MAX_KEY_SIZE > value > MAX_REC_KEY_SIZE:
            message = (f"The specified RSA key size of {value} exceeds the "
                       f"maximum recommended key size of {MAX_REC_KEY_SIZE}. "
                       f"This will reduce performance significantly.")
            logger.warn(message)
            warnings.warn(f"{message}\n")
        if value % KEY_SIZE_MODULUS != 0:
            message = (f"The specified RSA key size of {value} is not a "
                       f"multiple of {KEY_SIZE_MODULUS}. This is not "
                       f"necessarily a problem, as long as you understand "
                       f"the potential implications.")
            logger.warn(message)
            warnings.warn(f"{message}\n")
        logger.info(f"Setting rsa_key_size in config: {value}")
        setattr(self._namespace, 'rsa_key_size', value)

    @property
    def service_name(self):
        """The name of the Docker Swarm Service where the TLS certificate(s)
        will be installed.
        """
        pass

    @service_name.setter
    def service_name(self, value):
        logger.info(f"Setting service_name in config: {value}")
        setattr(self._namespace, 'service_name', value)

    @property
    def staging(self):
        """Boolean value, indicating whether to use the Let's Encrypt staging
        environment or not. In a Production environment, this value should be
        False.

        See https://letsencrypt.org/docs/staging-environment/ for more
        information.
        """
        pass

    @staging.setter
    def staging(self, value):
        logger.info(f"Setting staging in config: {value}")
        setattr(self._namespace, 'staging', value)

    @property
    def work_dir(self):
        """Defines the 'work' directory

        The config.yaml file should be placed in this directory. All output
        from LED will be initially placed in this directory as well.
        Pertinent files from this directory will be copied over into the
        appropriate direcotries in the web server container, however, they
        should be preserved in this directory as well, for future use.

        Keep in mind that most of the files in this directory are sensitive
        and should be guarded carefully. LED will attempt to set the
        appropriate permissions, but it is ultimately up to you to ensure that
        these files are protected from those who do not need access, including
        threat actors.
        """
        pass

    @work_dir.setter
    def work_dir(self, value):
        logger.info(f"Setting work_dir in config: {value}")
        setattr(self._namespace, 'work_dir', get_dir(value))

    @property
    def namespace(self):
        """Return the current config as a Namespace object

        The namespace property is read-only. If you wish to modify the
        namespace, you either need to modify your config.yaml file
        (recommended), or update the individual namespace value using
        it's own settter property, accesed by running the `led update TARGET`
        command, where TARGET is the name of the configuration property that
        you wish to change.
        """
        return self._namespace


try:
    config = Config().namespace
except LEDError as e:
    logger.error(e)
    print(e)
    sys.exit(ExitCode.EX_CONFIG)
