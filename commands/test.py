import subprocess
from os.path import join
import _global
from _global import *
from classes.config import Config
from classes.system import System
import mysql.connector as conn
from classes.component import Component
from classes.wordpress import Wordpress
from modules.colors import color as c
import html


class test_cmd:

    @staticmethod
    def env():
        return DEVELOPMENT_ENV

    @staticmethod
    def description():
        return "&6Debug command for testing purposes\n"

    @staticmethod
    def execute(_command):

        pass

        # pres = Config.get('PRESETS')
        # pres["DB_HOST"] = "host.docker.internal" if pres["DB_HOST"] == '%HOST%' else pres["DB_HOST"]
        # try:
        #     if pres['DB_PASSWORD'] == '':
        #         conn.connect(host=pres['DB_HOST'], user=pres['DB_USER'])
        #     else:
        #         conn.connect(host=pres['DB_HOST'], user=pres['DB_USER'], password=pres['DB_PASSWORD'])
        #     sysout(f'&a+&7 Connected to database\n', "success")
        # except Exception as e:
        #     sysout(f'Could not connect to database ({e})\n', type="error")

        # sysout(f'php wp-cli.phar eval {SCRIPT}')
        # run = subprocess.run([f'php', 'wp-cli.phar', 'eval', 'echo get_page_by_path("accueil")->ID;'], capture_output=True)
        # print(run.stdout.decode('utf-8'))
        # php_version = Wordpress.cli('eval echo(phpversion());', quiet=False, debug=True, output=True)
        # print(php_version)
        # if System.getHostOS() == 'Darwin':
        #     run = subprocess.run(['php -v'], capture_output=True, shell=True, executable='/bin/zsh', check=True)
        #     print(run.stdout.decode('utf-8'))
        # output = System.run('php -v', output=True, quiet=True, debug=True)

        # print("subprocess.run(['php', 'wp-cli.phar', '--info'], capture_output=True)")
        # run = subprocess.run(['php', 'wp-cli.phar', '--info'], capture_output=True)
        # print(run.stdout.decode('utf-8'))

        # SCRIPT = 'echo(get_page_by_path("accueil")->ID);'

        # print("wp_cli_info = Wordpress.cli('--info', output=True, debug=True)")
        # wp_cli_info = Wordpress.cli('eval ' + SCRIPT, output=True, debug=True)
        # print(wp_cli_info)

        # _infos = Wordpress.getPluginInfos('poll-maker')
        # print(_infos['name'])
        # print(_infos['version'])

        # COMPONENT = Component.fetchFromID(340)
        # COMPONENT.install()

        # path = join(os.getcwd(), '.git')
        # sysout('Path: ' + path)
        # System.gitRmtree(path)
        # sysout('Removed .git folder')
