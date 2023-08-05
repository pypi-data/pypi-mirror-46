"""
This module should handle all of the command-line parsing and
invoke the correct command from commands.py
"""

import argparse

from led.__version__ import __version__

# create the top-level parser
parser = argparse.ArgumentParser(
    prog='led',
    usage='led [OPTIONS] COMMAND',
    description=('Use led to manage Lets Encrypt certificates'
                 ' for Docker containers.'),
    conflict_handler='resolve',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=("Run 'led COMMAND --help' for more information on"
            " a command.\n \n \n"),
)

parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s ' + f'version { __version__}'
)

LIMIT_DEFAULT = 1000
parser.add_argument(
    '-l', '--limit',
    type=int,
    default=LIMIT_DEFAULT,
    help=(f'limit the number of operations performed by the command '
          f'to LIMIT\nDefaults to {LIMIT_DEFAULT}'
          f'\n \nExample:'
          f'\n\t\t`mit --limit 5 archive playlist Movies`'
          f'\n\t\twill archive up to 5 movies missing from the archive')
)

# Add subparser below for each led command
subparsers = parser.add_subparsers(
    title='commands',
    metavar=''
)

# create the parser for the "create" command
parser_create = subparsers.add_parser(
    'create',
    formatter_class=argparse.RawTextHelpFormatter,
    help="Create various objects.",
    epilog="\n \n",
)

parser_create.add_argument(
    'target',
    choices=[
        'a',
        'b',
        'c'
    ],
    metavar='target',
)

parser_create.set_defaults(cmd='create')

# create the parser for the "register" command
parser_register = subparsers.add_parser(
    'register',
    argument_default=None,
    formatter_class=argparse.RawTextHelpFormatter,
    help="Register a user with Let's Encrypt.",
    epilog="\n \n",
)

parser_register.set_defaults(cmd='register')

# create the parser for the "show" command
parser_show = subparsers.add_parser(
    'show',
    usage='led show TARGET',
    formatter_class=argparse.RawTextHelpFormatter,
    help="Show various information.",
    epilog="\n \n",
)

parser_show.add_argument(
    'target',
    choices=[
        'config',
        'status',
    ],
    help=("The 'config' target shows the current configuration of led."
          "\nThe 'status' target shows the current status of the"
          " reverse proxy container."),
    metavar='target',
)

parser_show.add_argument(
    '-c', '--count',
    action='store_true',
    dest='count',
    help='Output the result set as a numbered list'
)

parser_show.add_argument(
    '-t', '--total',
    action='store_true',
    dest='total',
    help=('Include a total of the number of items in the output'
          '\nThis option cannot be used with the [-d, --delimited] option')
)

parser_show.set_defaults(cmd='show')
