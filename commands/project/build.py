import os, subprocess
from classes.wordpress import Wordpress
from classes.system import System
from _global import *
from modules.loader import Loader
import time
from os.path import join


class build_cmd:

    @staticmethod
    def description():
        return "build assets"

    @staticmethod
    def execute(_command):
        # sysout(f'Building projects assets...', type="info")
        start_time = time.time()
        loader = Loader('Building project assets', 'Project assets built successfully in %time% s', '&9').start(new_line=True)
        # if System.execute('yarn build', type='raw') != 0:
        #     System.clearTerminal()
        #     loader.stop(custom_message='Unable to build assets, try running "yarn build" for error logs', custom_color='&c', new_line=True)
        #     exit()
        System.yarnBuild(Wordpress.THEME_FOLDER)
        if not os.path.exists(join(Wordpress.THEME_FOLDER, 'dist')):
            err('Unable to build assets, try running "cd web/app/themes/akyos-sage $_$_ yarn build" for error logs', start_of_line=True)
        # System.clearTerminal()
        loader.suspend()
        sysout('Project assets built successfully in ' + str(round((time.time() - start_time), 2)), type='success', start_of_line=True)

