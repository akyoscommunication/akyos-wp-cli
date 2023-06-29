import _global
from _global import *
from modules.colors import color as c
from classes.config import Config
from classes.system import System


class help_cmd:

    @staticmethod
    def description():
        return "List of commands"

    @staticmethod
    def execute(_command):

        _env = Config.get('APP_ENV')

        if len(_command.args) == 1:
            if _global.HANDLER.exist(_command.args[0]):
                _cmd = _global.HANDLER.commands[_command.args[0]]
                if _global.HANDLER.isDev(_cmd) and _env == PRODUCTION_ENV:
                    err('command not available in production environment')
                print(c('&9' + _command.args[0]) + c('&7 → ' + _cmd.description()))
                if System.methodExist(_cmd, 'usage'):
                    print(c('&9Usage: ') + c(_cmd.usage()))
                else:
                    sysout(f'No instructions available for &9"{_command.args[0]}"', type="info")
            else:
                err('unable to find "' + _command.args[0] + '", type "help" for a list of commands')
            return

        print(c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━&7[ &9Akyos CLI &7]&9━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'))
        sysout('Type &9"help <command>" &7to get more information about a command\n', type="info")
        for command in _global.HANDLER.commands.keys():

            _cmd = _global.HANDLER.commands[command]
            if _global.HANDLER.isDev(_cmd) and _env == PRODUCTION_ENV:
                continue

            print(c('&9' + command) + c('&7 → ' + _cmd.description()))
        print(c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))