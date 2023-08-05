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

from led import core
from led import show as showit

__all__ = ['show']


def create():
    pass


def register(args):
    """Register new account with Let's Encrypt

    Any information required for registration will be pulled from the config.yaml
    file. A contact_email is *required* to be provided in the config. If other required
    values are not provided, reasonable defaults will be used.
    """
    core._register_account()


def show(args):
    """Show various information.

    If the operator would like to inspect any values pertinent to the
    operation of LED, they should be able to find them by running
    `led show TARGET`, specifying TARGET as one of the values described below.

    Args:
        args (object): A Namspace object passed from the Standard Library's
                       argparse module.

                       TARGET is **required** to be passed as an argument to
                       the `show` sub-command.

    The TARGET string may be one of the Following:

    **config:** Show the configuration values of LED.

            These values are initialized from the YAML configuration file
            passed-in at runtime. The values may be updated from the command
            line using the `led update` command. The values displayed
            here may include the result of such an update.

            Anytime a change is made to the configutation, that change
            is reflected in the log file. If the configuration
            displayed here is different from the expected config, the
            operator should inspect the log file for an explanation.

    **status:** Show the status of the Docker setup in the context of LED.

            There are plenty of native Docker commands to show the state of
            Docker. This status command only provides information about the
            Docker daemon and the service that is relevant in
            the context of LED and the TLS certificates that it manages.
    """
    target = args.target
    if target == 'config':
        value = showit._show_config(args)
    elif target == 'status':
        value = showit._show_status(args)
    return value
