# from tkinter import filedialog as fd
# from tkinter import Tk
from classes.wordpress import Wordpress
from classes.system import System
from modules.loader import Loader
from _global import *


class dbimport_cmd:

    @staticmethod
    def description():
        return "import database"

    @staticmethod
    def execute(_command):
        sysout('This command is not available yet', type='error')
        # DB_CREDENTIALS = Wordpress.getDatabaseCredentials()
        # DB_PASSWORD = f'-p{DB_CREDENTIALS["DB_PASSWORD"]} ' if len(DB_CREDENTIALS["DB_PASSWORD"]) != 0 else ''
        # sysout('Select database file you want to import')
        # Tk().withdraw()
        # DB_IMPORT_PATH = fd.askopenfilename(title='Select a Database file', initialdir='/', filetypes=(
        #     ('Database File', '*.sql'),
        # ))
        # _confirm = confirm('Importing database will override existing one, do you want to continue', warning=True)
        # if not _confirm or DB_IMPORT_PATH is None:
        #     ex()
        #
        # loader = Loader(f'Importing database {DB_CREDENTIALS["DB_NAME"]}', color='&9').start()
        #
        # dbimport_cmd.dropDatabase(DB_CREDENTIALS, DB_PASSWORD)
        # dbimport_cmd.createDatabase(DB_CREDENTIALS, DB_PASSWORD)
        # dbimport_cmd.importDatabase(DB_IMPORT_PATH, DB_CREDENTIALS, DB_PASSWORD)
        #
        # loader.stop(custom_message=f'Database imported successfully into {DB_CREDENTIALS["DB_NAME"]}', custom_color='&a')

    @staticmethod
    def dropDatabase(DB_CREDENTIALS, DB_PASSWORD):
        COMMAND = f'mysqladmin -u {DB_CREDENTIALS["DB_USER"]} {DB_PASSWORD}-h {DB_CREDENTIALS["DB_HOST"]} -f drop {DB_CREDENTIALS["DB_NAME"]}'
        return_code = System.execute(COMMAND, type='raw', replace=False)
        if return_code != 0:
            err(f'Unable to drop database, try running "{COMMAND}" manually for more infos')

    @staticmethod
    def createDatabase(DB_CREDENTIALS, DB_PASSWORD):
        COMMAND = f'mysqladmin -u {DB_CREDENTIALS["DB_USER"]} {DB_PASSWORD}-h {DB_CREDENTIALS["DB_HOST"]} create {DB_CREDENTIALS["DB_NAME"]}'
        return_code = System.execute(COMMAND, type='raw', replace=False)
        if return_code != 0:
            err(f'Unable to create database, try running "{COMMAND}" manually for more infos')

    @staticmethod
    def importDatabase(DB_IMPORT_PATH, DB_CREDENTIALS, DB_PASSWORD):
        COMMAND = f'mysql -u {DB_CREDENTIALS["DB_USER"]} {DB_PASSWORD}-h {DB_CREDENTIALS["DB_HOST"]} -e ' \
                  f'use%_{DB_CREDENTIALS["DB_NAME"]};%_source%_{DB_IMPORT_PATH};'
        return_code = System.execute(COMMAND, type='raw')
        if return_code != 0:
            COMMAND = COMMAND.replace('%_', '')
            err(f'Unable to import database, try running "{COMMAND}" manually for more infos')
        # sysout(f'Database imported successfully into "{DB_CREDENTIALS["DB_NAME"]}"', type='success')
