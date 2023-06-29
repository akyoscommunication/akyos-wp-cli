import os.path
from modules.file import *
from classes.wordpress import Wordpress
from classes.system import System
from os.path import join
from _global import *


class dump_cmd:

    @staticmethod
    def description():
        return "dump database"

    @staticmethod
    def execute(_command):
        DB_CREDENTIALS = Wordpress.getDatabaseCredentials()
        DB_PASSWORD = f'-p{DB_CREDENTIALS["DB_PASSWORD"]} ' if len(DB_CREDENTIALS["DB_PASSWORD"]) != 0 else ''
        DB_EXPORT_PATH = join(System.getHostUserFolder(), 'exports', f'{DB_CREDENTIALS["DB_NAME"]}')
        if not os.path.exists(join(System.getHostUserFolder(), 'exports')):
            Directory(join(System.getHostUserFolder(), 'exports'), path_type=ABS).create(move=True)
        while os.path.exists(DB_EXPORT_PATH + '.sql'):
            DB_EXPORT_PATH += '_'
        sysout(f'Database dumped successfully at {DB_EXPORT_PATH}.sql', type='success')

    @staticmethod
    def dumpDatabase(DB_CREDENTIALS, DB_PASSWORD, DB_EXPORT_PATH):
        COMMAND = f'mysqldump -u {DB_CREDENTIALS["DB_USER"]} {DB_PASSWORD}' \
                  f'-h {DB_CREDENTIALS["DB_HOST"]} --column-statistics=0 --result-file={DB_EXPORT_PATH}.sql ' \
                  f'{DB_CREDENTIALS["DB_NAME"]}'
        return_code = System.execute(COMMAND, type='raw', replace=False)
        if return_code != 0:
            err(f'Unable to dump database, try running "{COMMAND}" manually for more infos')
