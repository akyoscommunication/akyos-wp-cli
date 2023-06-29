import _global
from _global import *
from modules.colors import color as c
from classes.config import Config
from classes.system import System
from modules.loader import Loader
import sys


class doctor_cmd:

    errors = []

    @staticmethod
    def description():
        return "Check if everything is working properly\n"

    @staticmethod
    def execute(_command):

        sysout(f'Running doctor - (Platform: {System.getHostOS()} - Python : {sys.version})\n\n', type="info")

        loader = Loader('Checking if everything is working properly', 'Everything is working properly').start()

        # php
        loader.infos('Checking if php is installed')
        php_installed = System.isInstalled('php')
        valid_php_version = ["8.0", "8.1", "8.2"]
        if php_installed:
            php_version = System.getPHPVersion()
            color = '&a' if php_version in valid_php_version else '&c'
            loader.print(f'\033[F[&a+&7] PHP is installed ({color}v{php_version}&7)\n')
            if php_version not in valid_php_version:
                loader.print(f'\033[F[&c-&7] PHP version is {php_version}, please '+ ('upgrade' if php_version < str(8.1) else 'downgrade') +' it to 8.x\n')
                doctor_cmd.errors.append(f'PHP version is {php_version}, but 8.x is required')
        else:
            loader.print('\033[F[&c-&7] PHP is not installed\n')
            doctor_cmd.errors.append('PHP is not installed')

        # composer
        loader.infos('Checking if composer is installed')
        composer_installed = System.isInstalled('composer', '--version')
        if composer_installed:
            loader.print('\033[F[&a+&7] Composer is installed\n')
        else:
            loader.print('\033[F[&c-&7] Composer is not installed\n')
            doctor_cmd.errors.append('Composer is not installed')

        # git
        loader.infos('Checking if git is installed')
        git_installed = System.isInstalled('git', '--version')
        if git_installed:
            loader.print('\033[F[&a+&7] Git is installed\n')
        else:
            loader.print('\033[F[&c-&7] Git is not installed\n')
            doctor_cmd.errors.append('Git is not installed')

        # yarn
        loader.infos('Checking if yarn is installed')
        yarn_installed = System.isInstalled('yarn')
        if yarn_installed:
            loader.print('\033[F[&a+&7] Yarn is installed\n')
        else:
            loader.print('\033[F[&c-&7] Yarn is not installed\n')
            doctor_cmd.errors.append('Yarn is not installed')

        # mysql & mysqladmin
        loader.infos('Checking if MySQL CLI is installed')
        mysql_installed = System.isInstalled('mysql', '--version')
        mysql_admin_installed = System.isInstalled('mysqladmin', '--version')
        if mysql_installed and mysql_admin_installed:
            loader.print('\033[F[&a+&7] MySQL CLI is installed\n')
        elif mysql_installed and not mysql_admin_installed:
            loader.print('\033[F[&c-&7] Unable to access mysqladmin, maybe you should reinstall MySQL\n')
            doctor_cmd.errors.append('Unable to access mysqladmin')
        else:
            loader.print('\033[F[&c-&7] MySQL CLI is not installed\n')
            doctor_cmd.errors.append('MySQL CLI is not installed')
            doctor_cmd.errors.append('Unable to access mysqladmin')

        # mysql connection
        loader.infos('Checking if MySQL credentials are correct')
        mysql_connection = System.isMySQLConnectionCorrect()
        if mysql_connection:
            loader.print('\033[F[&a+&7] MySQL credentials are correct\n')
        else:
            loader.print('\033[F[&c-&7] MySQL credentials are incorrect\n')
            doctor_cmd.errors.append('MySQL credentials are incorrect')

        # check if api is reachable
        loader.infos('Checking if component API is reachable')
        api_reachable = System.isReachable(Config.get('COMPONENT_API_URL'))
        if api_reachable:
            loader.print('\033[F[&a+&7] Component API is reachable\n')
        else:
            loader.print('\033[F[&c-&7] Component API is not reachable\n')
            doctor_cmd.errors.append('Component API is not reachable')

        # check if gitlab token is set
        loader.infos('Checking if Gitlab Token is set')
        gitlab_token_set = Config.get('GITLAB_TOKEN') != ''
        if gitlab_token_set:
            loader.print('\033[F[&a+&7] Gitlab Token is set\n')
        else:
            loader.print('\033[F[&c-&7] Gitlab Token is not set\n')
            doctor_cmd.errors.append('Gitlab Token is not set')

        # check if wpmu key is set
        loader.infos('Checking if WPMU DEV Key is set')
        wpmu_key_set = Config.get('WPMU_DEV_API_KEY') != ''
        if wpmu_key_set:
            loader.print('\033[F[&a+&7] WPMU DEV Key is set\n')
        else:
            loader.print('\033[F[&c-&7] WPMU DEV Key is not set\n')
            doctor_cmd.errors.append('WPMU DEV Key is not set')

        # check if acf pro key is set
        loader.infos('Checking if ACF Pro Key is set')
        acf_key_set = Config.get('ACF_PRO_KEY') != ''
        if acf_key_set:
            loader.print('\033[F[&a+&7] ACF Pro Key is set\n')
        else:
            loader.print('\033[F[&c-&7] ACF Pro Key is not set\n')
            doctor_cmd.errors.append('ACF Pro Key is not set')

        # check if user home folder is accessible
        loader.infos('Checking if $HOME is accessible')
        user_home_accessible = System.getHostUserFolder() != ''
        if user_home_accessible:
            loader.print(f'\033[F[&a+&7] $HOME is accessible (&9{System.getHostUserFolder()}&7)\n')
        else:
            loader.print('\033[F[&c-&7] $HOME is not accessible\n')
            doctor_cmd.errors.append('$HOME is not accessible')

        # check if temp folder is accessible
        loader.infos('Checking if Temp folder is accessible')
        temp_folder_accessible = System.getTempDir() != ''
        if temp_folder_accessible:
            loader.print(f'\033[F[&a+&7] Temp folder is accessible (&9{System.getTempDir()}&7)\n')
        else:
            loader.print('\033[F[&c-&7] Temp folder is not accessible\n')
            doctor_cmd.errors.append('Temp folder is not accessible')

        loader.suspend()
        if len(doctor_cmd.errors) > 0:
            sysout(f'Doctor found {len(doctor_cmd.errors)} errors, please fix them and try again' + 10 * ' ', type='error')
            for error in doctor_cmd.errors:
                print(c(' &c→ ' + error))
        else:
            sysout('&a Everything is working properly !' + 20 * ' ', type='success')

    @staticmethod
    def check():
        """
        Check if everything is working properly
        """
        errors = {
            'php': System.isInstalled('php') and System.getPHPVersion() in ["8.1", "8.2"],
            'composer': System.isInstalled('composer', '--version'),
            'git': System.isInstalled('git', '--version'),
            'yarn': System.isInstalled('yarn'),
            'mysql': System.isInstalled('mysql', '--version'),
            'mysqladmin': System.isInstalled('mysqladmin', '--version'),
            'mysql_connection': System.isMySQLConnectionCorrect(),
            'api': System.isReachable(Config.get('COMPONENT_API_URL')),
            'gitlab_token': Config.get('GITLAB_TOKEN') != '',
            'wpmu_key': Config.get('WPMU_DEV_API_KEY') != '',
            'acf_key': Config.get('ACF_PRO_KEY') != '',
            'user_home': System.getHostUserFolder() != '',
            'temp_folder': System.getTempDir() != ''
        }
        for key in errors.keys():
            if not errors[key]:
                return False
        return True
