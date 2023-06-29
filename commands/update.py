import subprocess
from os.path import join
import _global
from _global import *
from modules.colors import color as c
from classes.updater import Updater
import html


class update_cmd:

    @staticmethod
    def description():
        return "&6Update the cli to the latest version\n"

    @staticmethod
    def execute(_command):
        new_update = Updater.check(no_logs=True)
        if new_update:
            Updater.update()
