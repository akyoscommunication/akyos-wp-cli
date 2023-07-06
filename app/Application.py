import sys

from console.ConsoleIO import IOManager, ConsoleIO
from core.commands.Command import Command
from core.commands.CommandManager import CommandManager
from core.framework.Configuration import Configuration
from core.framework.Updater import Updater
from core.functions import err


class Application:

    def __init__(self):
        self.env = Configuration.get('APP_ENV')

        # check for updates
        Updater.check()

        # register commands
        self.commandManager: CommandManager = CommandManager()
        self.commandManager.registerCommands()

        # parse current args into command object
        self.command: Command = Command(sys.argv[1:])

    def boot(self):

        # check if command exist
        if not self.commandManager.exist(self.command):
            err('unable to find "' + self.command.arg + '", type "help" for a list of commands')

        # check if command is available only in dev environment
        command = self.commandManager.get(self.command.arg)  # get command class
        if self.commandManager.isDev(command) and self.env == PRODUCTION_ENV:
            err('command not available in production environment')

        # invoke command & exit w/ proper status code
        status_code = command.invoke(self, ConsoleIO())
        sys.exit(status_code)