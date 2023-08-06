import sys
import json
from sparrow.src.commands import global_flags, commands
from sparrow.src.helper import general_help, command_not_found
from sparrow.src import __version__
from sparrow.src.manager import SparrowManager


class Parser:
    """
    Parser responsibility is to direct the execution to the right
    channel.
    """

    def __init__(self):
        self.args = sys.argv[1:]
        if len(self.args) == 0:
            print(general_help())
        else:
            self.validate(self.args)

    def validate(self, cmd):
        """
        general validation mechanism for all
        commands and global flags
        :param cmd:
        :return: global_flags or commands
        """
        _global = global_flags.key
        if cmd[0] in _global['version']['key'] or cmd[0] in _global['help']['key']:
            return self.global_flags()

        if cmd[0] in [commands.key['extract']['key'], commands.key['info']['key']]:
            return self.commands()

        print(general_help(gray=True))
        print(command_not_found(cmd))

    def global_flags(self):
        """
        :return: None
        """
        if self.args[0] in ['--version', '-v'] and len(self.args) is 1:
            print("sparrow version:", __version__)
        elif self.args[0] in ['--help', '-h'] and len(self.args) is 1:
            print(general_help())
        else:
            print(general_help(gray=True))
            print(command_not_found(self.args))

    def commands(self):
        """
        commands maps to SparrowManager a valid json files
        :return:
        """
        _sparrow = SparrowManager()
        if self.args[0] == "extract" and len(self.args) == 3:
            inp = self.args[1] if self.args[1].find(".") != -1 else self.args[1] + ".json"
            tar = self.args[2] if self.args[2].find(".") != -1 else self.args[2] + ".json"
            try:
                with open(inp, 'r') as f:
                    source = json.load(f)
            except FileNotFoundError as e:
                print(e)
                exit(1)

            try:
                with open(tar, 'r') as f:
                    target = json.load(f)
            except FileNotFoundError as e:
                print(e)
                exit(1)
            return _sparrow.extract(source, target)
        elif self.args[0] == "info" and len(self.args) == 2:
            inp = self.args[1] if self.args[1].find(".") != -1 else self.args[1] + ".json"
            try:
                with open(inp, 'r') as f:
                    source = json.load(f)
            except FileNotFoundError as e:
                print(e)
                exit(1)
            return _sparrow.info(source)
        else:
            if len(self.args) == 1:
                print(general_help())
            else:
                print(general_help(gray=True))
                print(command_not_found(self.args[1:]))
