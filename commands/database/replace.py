import random
from _global import *
import _global
from modules.file import File, Directory, ABS
from commands.database._import import dbimport_cmd
from commands.database.dump import dump_cmd
from classes.wordpress import Wordpress
from os.path import join as join
from classes.system import System


class replace_cmd:

    @staticmethod
    def description():
        return "replace database url"

    @staticmethod
    def execute(_command):

        DB_CREDENTIALS = Wordpress.getDatabaseCredentials()
        DB_PASSWORD = f'-p{DB_CREDENTIALS["DB_PASSWORD"]} ' if len(DB_CREDENTIALS["DB_PASSWORD"]) != 0 else ''
        EXPORT_PATH = join(System.getTempDir(), f'sageCLI_{randKey(32)}_temp')
        dump_cmd.dumpDatabase(DB_CREDENTIALS, DB_PASSWORD, EXPORT_PATH)

        DATABASE_FILE_CONTENT = File(f'{EXPORT_PATH}.sql', path_type=ABS).content()
        REPLACE_URLS = replace_cmd.getDatabaseReplacments(DATABASE_FILE_CONTENT)
        for URL in REPLACE_URLS:
            DATABASE_FILE_CONTENT = DATABASE_FILE_CONTENT.replace(URL[0], URL[1])
        PROCESSED_DATABASE = File(f'{EXPORT_PATH}.sql', path_type=ABS).setContent(DATABASE_FILE_CONTENT).save(force=True)

        dbimport_cmd.dropDatabase(DB_CREDENTIALS, DB_PASSWORD)
        dbimport_cmd.createDatabase(DB_CREDENTIALS, DB_PASSWORD)
        dbimport_cmd.importDatabase(f'{EXPORT_PATH}.sql', DB_CREDENTIALS, DB_PASSWORD)
        os.remove(f'{EXPORT_PATH}.sql')

        sysout('Database urls replaced successfully !', type='success', new_line=True)

    @staticmethod
    def getDatabaseReplacments(DATABASE_FILE_CONTENT):
        REPLACE_URLS = []

        _continue = True
        while _continue:
            old_url = sysin('Enter old URL')
            new_url = sysin('Enter new URL')
            REPLACE_URLS.append([old_url, new_url])
            REPLACE_URLS.append(
                [old_url.replace(':', '%3A').replace('/', '%2F'), new_url.replace(':', '%3A').replace('/', '%2F')])
            if not confirm('Add more URLs'):
                _continue = False

        REPLACMENTS = 0
        print('\n' + c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        for URL in REPLACE_URLS:
            print(c(f'&7[&9 * &7] {URL[0]} &9→ &a{URL[1]} &7(&9{DATABASE_FILE_CONTENT.count(URL[0])}&7)'))
            REPLACMENTS += DATABASE_FILE_CONTENT.count(URL[0])
        print(c(f'&7[&9 > &7] A total of &9{REPLACMENTS} &7changes will be applied to the database'))
        print(c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        if not confirm('Apply these change to the database ?'):
            ex()

        return REPLACE_URLS


def randKey(lenght):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = ''
    for _ in range(lenght):
        key += chars[random.randint(0, len(chars) - 1)]
    return key
