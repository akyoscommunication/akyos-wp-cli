# import _global, sys
# from classes.command import CommandHandler, Command
# from classes.cli import CLI
# from classes.updater import Updater
from app.Application import Application


def main():
    app = Application()
    app.boot()
    # _global.HANDLER = CommandHandler()
    # CommandHandler.registerCommands()
    # command = Command(sys.argv[1:])
    # Updater.check()
    # CLI.execute(command)


if __name__ == "__main__":
    main()
