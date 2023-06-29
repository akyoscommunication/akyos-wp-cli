import _global, sys
from _global import *
from classes.command import CommandHandler, Command
from classes.cli import CLI
from classes.updater import Updater


def main():
    _global.HANDLER = CommandHandler()
    CommandHandler.registerCommands()
    command = Command(sys.argv[1:])
    CLI.execute(command)


if __name__ == "__main__":
    main()
