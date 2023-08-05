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

import getpass
import json

from acme import challenges
from acme import client
from acme import crypto_util
from acme import errors
from acme import messages
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import josepy as jose
from josepy.errors import DeserializationError

from led.config import config
from led.constants import (DEFAULT_KEY_SIZE, PUBLIC_EXPONENT,
                           PROD_API_URL, STAG_API_URL, USER_AGENT)
from led.log import get_logger
from led.utils import get_dir

logger = get_logger(__name__)


def _create_acc_key():
    """Generate RSA Key
    Default key_size is 3072, but MUST be at least 2048.

    Certificate Authorities like Let's Encrypt can’t provide
    EdDSA certificates yet, so this rules-out using ed25519 keys.
    See:
    https://letsencrypt.org/docs/glossary/#def-EdDSA
    and
    https://community.letsencrypt.org/t/support-ed25519-and-ed448/69868
    """
    key_size = config.rsa_key_size or DEFAULT_KEY_SIZE
    le_acc_key = jose.JWKRSA(
        key=rsa.generate_private_key(public_exponent=PUBLIC_EXPONENT,
                                     key_size=key_size,
                                     backend=default_backend()))

    return le_acc_key


def _register_account():
    # Register account and accept TOS

    if config.staging:
        directory_url = STAG_API_URL
    else:
        directory_url = PROD_API_URL

    le_acc_key = _create_acc_key()
    net = client.ClientNetwork(le_acc_key, user_agent=USER_AGENT)
    directory = messages.Directory.from_json(net.get(directory_url).json())
    client_acme = client.ClientV2(directory, net=net)

    # Terms of Service URL is in client_acme.directory.meta.terms_of_service
    # Registration Resource: registration
    # Creates account with contact information.
    email = (config.contact_email)
    registration = client_acme.new_account(
        messages.NewRegistration.from_data(
            email=email, terms_of_service_agreed=True
        )
    )
    jobj = registration.fields_to_partial_json()
    logger.info(f"LE Registration: {jobj}")
