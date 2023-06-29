import _global
from _global import *
from classes.command import Command
from classes.config import Config


class CLI:

    @staticmethod
    def execute(command: Command) -> None:

        if not _global.HANDLER.exist(command):  # check if command exist
            err('unable to find "' + command.arg + '", type "help" for a list of commands')

        _cmd = _global.HANDLER.commands[command.arg]  # get command object
        if _global.HANDLER.isDev(_cmd) and Config.get('APP_ENV') == PRODUCTION_ENV:
            err('command not available in production environment')

        _global.HANDLER.execute(command)
