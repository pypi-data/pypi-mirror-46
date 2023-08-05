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

Invocation:
    led [args] [<command>] [<args>]
"""

from led import api
from led.cli import parser
from led.error import ExitCode
from led.log import get_logger

logger = get_logger(__name__)

args_optional = set(
    {
        'limit': None,
    }
)


def main():
    """Run `led` command
    If the user calls `led --help`, or `led COMMAND` with out the expected
    COMMAND arguments, the parser will catch this in the parser.parse_args()
    method and then print the Help and exit before going any further
    in the main() function.

    The 'check' that is performed in main() ensures that if the user runs
    `led` without *any* arguments, the Help will still be displayed.
    """
    """Setup logging configuration."""
    args = parser.parse_args() or None
    logger.info(f"cli args: {vars(args)}")
    args_given = set(vars(args))
    check = args_given ^ args_optional

    if len(check) > 0:
        try:
            getattr(api, args.cmd)(args)
        except SystemExit as e:
            return e.value
        else:
            return ExitCode.EX_SUCCESS
    else:
        parser.print_help()
        return ExitCode.EX_USAGE
