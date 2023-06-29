import os
from os.path import join

from _global import *
from classes.wordpress import Wordpress
from classes.system import System


def getProjectName(INITIAL_FOLDERS):
    NEW_FOLDERS = os.scandir(PROJECT_PATH)
    for folder in NEW_FOLDERS:
        if folder not in INITIAL_FOLDERS:
            return folder.name
    err('Unable to find new project folder, please check if project has been successfully cloned')


class install_cmd():

    @staticmethod
    def description():
        return "install project dependencies"

    @staticmethod
    def execute(_command):

        FOLDER = os.scandir(PROJECT_PATH)

        GITHUB_URL = _command.args[0] if len(_command.args) > 0 else sysin('Github project URL')
        sysout(f'Cloning project from {GITHUB_URL}')
        if System.execute(f'git clone {GITHUB_URL}', type='raw') != 0:
            err('Unable to clone project, try running "git clone <url>" manually for more infos')

        PROJECT_NAME = getProjectName(FOLDER)

        Wordpress.ROOT_FOLDER = join(PROJECT_PATH, PROJECT_NAME)
        Wordpress.THEME_FOLDER = join(Wordpress.ROOT_FOLDER, 'web', 'app', 'themes', 'akyos-sage')

        os.chdir(Wordpress.ROOT_FOLDER)
        sysout('Installing Bedrock dependencies...')
        if System.execute('composer install', type='raw') != 0:
            if System.execute('composer install --ignore-platform-reqs', type='raw') != 0:
                err('Unable to install bedrock dependencies')

        os.chdir(Wordpress.THEME_FOLDER)
        sysout('Installing Akyos theme dependencies...')
        if System.execute('composer install', type='raw') != 0:
            if System.execute('composer install --ignore-platform-reqs', type='raw') != 0:
                err('Unable to install sage dependencies')

        sysout('Installing Nodes modules')
        if System.execute('yarn install', type='raw') != 0:
            err('Unable to install nodes modules')

        sysout('Dependencies installed successfully !', type='success')