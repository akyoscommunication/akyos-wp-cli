import requests

import _global
from _global import *
from classes.system import System
from modules.file import *
import os
from os.path import join
from dotenv import load_dotenv
import html


class Wordpress:
    BLOCK_CONFIG_JS = os.path.abspath(os.path.join(THEME_PATH, 'resources', 'assets', 'build', 'blocks.config.js'))
    BLOCK_CONFIG_JS_TEMPLATE = assets(['templates', 'template-block.config.js'])
    SCSS_PATH = os.path.join(ASSETS_PATH, 'css', 'utils', 'components')
    ROOT_FOLDER = PROJECT_PATH
    THEME_FOLDER = THEME_PATH

    @staticmethod
    def getWordpressInstallation():
        # _dotenv = join(Wordpress.ROOT_FOLDER, '.env')
        app_folder = join(Wordpress.ROOT_FOLDER, 'web', 'app')
        if os.path.exists(app_folder):
            if os.path.exists(join(app_folder, 'themes', 'akyos-sage')):
                return SAGE
            return BEDROCK
        _wp_config = join(Wordpress.ROOT_FOLDER, 'wp-config.php')
        if os.path.exists(_wp_config):
            return WORDPRESS
        return UNDEFINED

    @staticmethod
    def addBlockConfigJSEntry(COMPONENT, COMPONENT_PATH):
        FILE_START, FILE_END = File.cut(Wordpress.BLOCK_CONFIG_JS, 'const blocks', '];', path_type=ABS)
        FINAL_CONTENT = File(Wordpress.BLOCK_CONFIG_JS, path_type=ABS) \
            .empty() \
            .copyContent(Wordpress.BLOCK_CONFIG_JS_TEMPLATE, path_type=ABS) \
            .replaceContent({
            '%componentName%': COMPONENT.name.lower(),
            '%componentSass%': COMPONENT.style['name'],
            '%componentPath%': COMPONENT_PATH.split('/')[-1]
        }).obj_content()
        File(Wordpress.BLOCK_CONFIG_JS, path_type=ABS).setContent(FILE_START + FINAL_CONTENT + FILE_END).save(
            force=True)

    @staticmethod
    def componentExist(COMPONENT_NAME):
        return os.path.exists(join(COMPONENTS_PATH, COMPONENT_NAME))

    @staticmethod
    def parseWPConfig():
        _parsed = {}
        keys = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']
        _wp_config = join(Wordpress.ROOT_FOLDER, 'wp-config.php')
        wp_content = File(_wp_config, path_type=ABS).content()
        for line in wp_content.split('\n'):
            if 'define' not in line:
                continue
            value = line.split('(')[1].split(')')[0].split(',')
            key = value[0].replace('\'', '')
            if key in keys:
                _parsed[key] = value[1].replace('\'', '')
        return _parsed

    @staticmethod
    def getWPVersion():

        if Wordpress.getWordpressInstallation() == SAGE or Wordpress.getWordpressInstallation() == BEDROCK:
            _wp_version = join(Wordpress.ROOT_FOLDER, 'web', 'wp', 'wp-includes', 'version.php')
        else:
            _wp_version = join(Wordpress.ROOT_FOLDER, 'wp-includes', 'version.php')

        _wp_content = File(_wp_version, path_type=ABS).content()
        for line in _wp_content.split('\n'):
            if 'wp_version' not in line:
                continue
            if '@global' in line:
                continue
            return line.split("'")[1]

        err('Unable to find WordPress version')

    @staticmethod
    def getDatabaseCredentials():

        if Wordpress.getWordpressInstallation() == UNDEFINED:
            err('Wordpress installation not found')

        if Wordpress.getWordpressInstallation() == SAGE or Wordpress.getWordpressInstallation() == BEDROCK:
            load_dotenv(join(Wordpress.ROOT_FOLDER, '.env'))
            DB_USER = os.getenv('DB_USER')
            DB_NAME = os.getenv('DB_NAME')
            DB_PASSWORD = os.getenv('DB_PASSWORD')
            DB_HOST = os.getenv('DB_HOST') if os.getenv('DB_HOST') is not None else '127.0.0.1'

        if Wordpress.getWordpressInstallation() == WORDPRESS:
            _wp_config = Wordpress.parseWPConfig()
            DB_USER = _wp_config['DB_USER']
            DB_NAME = _wp_config['DB_NAME']
            DB_PASSWORD = _wp_config['DB_PASSWORD']
            DB_HOST = _wp_config['DB_HOST'] if _wp_config['DB_HOST'] is not None else '127.0.0.1'

        return {
            'DB_USER': DB_USER,
            'DB_NAME': DB_NAME,
            'DB_PASSWORD': DB_PASSWORD,
            'DB_HOST': System.getHostIP()
        }

    @staticmethod
    def setEnv(env, values):
        _dotenv = env
        if os.path.exists(_dotenv):
            content = ''
            for value in values:
                content += '{}={}\n'.format(value, values[value])
            File(_dotenv, path_type=ABS).setContent(content).save(force=True)
        else:
            err('Unable to find .env file')

    @staticmethod
    def pluginExist(PLUGIN_NAME):
        req = requests.get('https://api.wordpress.org/plugins/info/1.0/' + PLUGIN_NAME)
        if req.status_code == 200:
            return True
        return False

    @staticmethod
    def getPluginInfos(PLUGIN_NAME):
        req = requests.get(f'https://api.wordpress.org/plugins/info/1.0/{PLUGIN_NAME}.json')
        if req.status_code == 200:
            _infos = req.json()
            for info in _infos.keys():
                if type(_infos[info]) is str:
                    _infos[info] = html.unescape(_infos[info])
            return _infos
        return None

    @staticmethod
    def installWPCLI(quiet=False):
        COMMAND = 'curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar'

        if os.path.exists(join(Wordpress.ROOT_FOLDER, 'wp-cli.phar')):
            if not quiet:
                sysout('WP-CLI already installed')
            return

        if System.execute(COMMAND) != 0:
            err('Unable to install WP-CLI')

        if System.getHostOS() in ['Linux', 'Darwin']:
            System.execute('chmod +x wp-cli.phar')
        if not quiet:
            sysout('WP-CLI installed successfully', type='success')

    @staticmethod
    def cli(_command, quiet=False, debug=False, output=False, replace=False):
        Wordpress.installWPCLI(quiet=True)
        COMMAND = (_global.WP_CLI_QUIET if quiet else _global.WP_CLI) + ' ' + _command + (' --quiet' if quiet else '')
        # COMMAND = COMMAND + ' --quiet' if quiet else COMMAND
        if output:
            return System.output(System.run(COMMAND, debug=debug, output=True, quiet=quiet))
        cmd_stdout = System.output(System.run(COMMAND, quiet=quiet, debug=debug, replace=replace, output=True))
        return 0 if 'success' in cmd_stdout.lower() else 1
