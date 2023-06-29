import os
from os.path import join
from classes.wordpress import Wordpress
from _global import *
from classes.system import System


class serve_cmd():

    @staticmethod
    def description():
        return "start developpment server & build assets"

    @staticmethod
    def usage():
        return "&7aky project:serve &9<port> &b[--logs]" \
               "\n&9--logs: &7Advanced server logs (default: false)"

    @staticmethod
    def execute(_command):

        logs = True if '--logs' in _command.args else False

        php_version = System.getPHPVersion()
        if php_version != '7.4':
            err(f"Please change your PHP version to 7.4 (current: PHP v{php_version})")
            return

        os.chdir(join(Wordpress.ROOT_FOLDER, 'web'))
        SERVER_PORT = _command.args[0] if len(_command.args) != 0 else 3000
        try:
            SERVER_PORT = int(SERVER_PORT)
        except Exception as e:
            if SERVER_PORT != '--logs':
                err('Please provide a valid port')
            SERVER_PORT = 3000

        sysout('Starting development server...', new_line=True, reset=False)
        # print('current dir : ' + os.getcwd())
        System.startServer(SERVER_PORT, logs)
