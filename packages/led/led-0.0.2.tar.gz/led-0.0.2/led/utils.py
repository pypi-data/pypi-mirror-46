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

from led.error import ExitCode


class Esc(object):
    BOLD = '\033[1m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    GREEN = '\033[92m'
    PURPLE = '\033[95m'
    RED = '\033[91m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[93m'


def get_dir(directory):
    path = os.path.abspath(directory)
    if os.path.isdir(path):
        return path
    else:
        try:
            os.makedirs(path)
        except OSError as e:
            print(f"Failed to create directory at {path}\nExiting...\n\n")
            raise e
            sys.exit(ExitCode.EX_CANTCREAT)
        else:
            return path


def new_warn_format(message, category, filename, lineno,
                    file=None, line=None):
    """Update the format of Python Warnings.

    The default format of Python Warnings is weird and annoying. For
    some reason, it insists on printing the call 'warn(message)' below the
    actual warning message, which only serves to make the message more
    confusing.

    This new format removes the annoying line. It also updates the Warning
    message format to support the new f-string syntax.
    """
    filename = os.path.basename(filename)
    return f"{filename}:{lineno} {category.__name__}:{message}"
