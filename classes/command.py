import _global
from _global import *
from classes.system import System
from commands._imports import *
from classes.wordpress import Wordpress
from classes.config import Config
from classes.updater import Updater


class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register(self, command, fn):
        self.commands[command] = fn

    def exist(self, command):
        _type = str(type(command))
        if _type == "<class 'str'>":
            return command in self.commands.keys()
        elif _type == "<class 'classes.command.Command'>":
            return command.arg in self.commands.keys()

    def execute(self, command):
        _COMMAND = self.commands[command.arg]
        _COMMAND.execute(command)

    def exec(self, command_name):
        """Execute command outside CLI lifecycle"""
        _command = Command([command_name])
        return self.commands[_command.arg].execute(_command)

    def get(self, command):
        """Get command object"""
        if self.exist(command):
            return self.commands[command.arg]
        return None

    @staticmethod
    def isDev(command):
        """Check if command is available only in dev environment"""
        _env = PRODUCTION_ENV
        try:
            _env = command.env()
        except AttributeError:
            pass
        return _env == DEVELOPMENT_ENV

    @staticmethod
    def registerCommands():
        commandHandler = _global.HANDLER

        commandHandler.register('help', help_cmd)
        commandHandler.register('doctor', doctor_cmd)
        commandHandler.register('update', update_cmd)

        commandHandler.register('component:create', create_cmd)
        commandHandler.register('component:import', import_cmd)
        commandHandler.register('component:export', export_cmd)

        commandHandler.register('project:create', createproject_cmd)
        commandHandler.register('project:install', install_cmd)
        commandHandler.register('project:serve', serve_cmd)
        commandHandler.register('project:build', build_cmd)
        commandHandler.register('project:push', push_cmd)

        commandHandler.register('database:replace', replace_cmd)
        commandHandler.register('database:import', dbimport_cmd)
        commandHandler.register('database:dump', dump_cmd)

        commandHandler.register('test', test_cmd)


class Command:

    _globals = ['help', 'doctor', 'test', 'update', 'project:create', 'project:install']
    _no_doctor = ['help', 'doctor', 'test', 'update']
    _no_updater = ['help', 'doctor', 'test', 'update']

    def __init__(self, arguments, _silent=False):
        self.command = ' '.join(arguments)
        if not self.check(arguments):
            exit()
        self.arg = arguments[0]
        self.args = arguments[1:]
        self.silent = _silent

    def check(self, arguments):

        WP_INSTALLATION = Wordpress.getWordpressInstallation()
        if len(self.command) == 0:
            print(c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━&7[ &9Akyos CLI &7]&9━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
            print(c('&9 Akyos CLI &7→ &7v&9' + _global.VERSION + ' &7(&9' + Config.get('APP_ENV') + '&7)'))
            if WP_INSTALLATION != UNDEFINED:
                print(c(f'&9 Wordpress &7(&9{Wordpress.getWordpressInstallation()}&7) &7→ &7v&9' + Wordpress.getWPVersion()))
            print(c('&9 → &7Type &9aky help &7to see a list of commands'))
            print(c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
            return False

        if arguments[0] not in self._no_updater:
            Updater.check()

        if WP_INSTALLATION == UNDEFINED and arguments[0] not in self._globals:
            sysout('Wordpress installation not found, please move to wordpress project folder.', type="error")
            return False

        # if arguments[0] not in self._no_doctor and not doctor_cmd.check():
        #     sysout('Doctor check failed, please fix errors before running commands. run &7"aky doctor" &cfor more infos.', type="error")
        #     return False

        return True

    def __str__(self) -> str:
        string = 'Command(\n'
        string += '   command : ' + self.command + '\n'
        string += '   arg : ' + str(self.arg) + '\n'
        string += '   args : ' + str(self.args) + '\n'
        string += ')'
        return string

