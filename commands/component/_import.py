from _global import *
import requests
from classes.component import Component
from classes.wordpress import Wordpress
from modules.file import File, Directory, ABS
from modules.loader import Loader
from os.path import join


# BLOCK_CONFIG_JS = os.path.abspath(os.path.join(THEME_PATH, 'resources', 'assets', 'build', 'blocks.config.js'))
# BLOCK_CONFIG_JS_TEMPLATE = assets(['templates', 'template-block.config.js'])
# SCSS_PATH = join(ASSETS_PATH, 'css', 'utils', 'components')


class import_cmd:

    @staticmethod
    def description():
        return "import an existing component"

    @staticmethod
    def execute(_command):

        if len(_command.args) == 0:
            COMPONENT_ID = sysin('Enter component ID')
        else:
            COMPONENT_ID = _command.args[0]

        print('')
        loader = Loader(f'Fetching component #{COMPONENT_ID}', color='&9').start()
        COMPONENT = Component.fetchFromID(COMPONENT_ID)

        if str(type(COMPONENT)) == "<class 'list'>":
            # print('\n\n\n' + 'err' + '\n\n\n')
            # loader.stop(custom_message=COMPONENT[1], custom_color='&c')
            loader.suspend(COMPONENT[1], color='&c')
            # sysout(COMPONENT[1], type='error', new_line=True)
            # loader.print(f'&c{COMPONENT[1]}', color='&c', new_line=True)
            exit()

        # print('\n\n\n' + 'ok' + '\n\n\n')
        COMPONENT.install()
        loader.suspend(f'&aComponent "{COMPONENT.name}" imported successfully !', color='&a')
        # loader.print('\n' + f'&aComponent "{COMPONENT.name}" imported successfully !', color='&a', new_line=True)
        # loader.stop(custom_color='&a', custom_message=f'Component "{COMPONENT.name}" imported successfully !')