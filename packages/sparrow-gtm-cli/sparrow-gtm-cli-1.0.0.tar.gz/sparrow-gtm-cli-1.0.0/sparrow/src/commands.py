"""
config is the entry point to add, edit and remove commands
and their help to extend sparrow-cli

All commands and flags are defined in the config module.
"""
from collections import namedtuple

_args = namedtuple('commands', "key help")

global_flags = _args(
    {
        'version': {'key': ['-v', '--version'], 'help': "output the version number"},
        'help'   : {'key': ['-h', '--help'], 'help': "output help information"},
    }
    , "")

commands = _args(
    {
        'extract': {'key': 'extract', 'help': "extract configuration file"},
        'info'   : {'key': 'info', 'help': "print information about the container"},
    }
    , ""
)

