from _global import *
import os

from classes.component import Component
from classes.wordpress import Wordpress
from modules.file import File, Directory, ABS
from os.path import join


class create_cmd:

    @staticmethod
    def description():
        return "create a new component"

    @staticmethod
    def execute(_command):

        if len(_command.args) == 0:
            COMPONENT_NAME = sysin('Enter component name [ex: title]', True)
        else:
            COMPONENT_NAME = _command.args[0]

        if Wordpress.componentExist(COMPONENT_NAME):
            sysout(f'A component with name "{COMPONENT_NAME}" already exist', type='error')
            exit()

        COMPONENT_DESCRIPTION = sysin('Enter component description [optional]', True)
        COMPONENT_PATH = os.path.abspath(os.path.join(COMPONENTS_PATH, COMPONENT_NAME))

        Directory(COMPONENT_PATH, path_type=ABS).create(move=True)

        File(f"{COMPONENT_NAME.lower()}.blade.php").save()

        File(Component.formatName(COMPONENT_NAME) + ".php") \
            .copyContent('assets/templates/component-template.php') \
            .replaceContent({
            '%blockname%': Component.formatName(COMPONENT_NAME),
            '%name%': COMPONENT_NAME.lower(),
            '%description%': COMPONENT_DESCRIPTION.replace("'", "\\'"),
            '%view%': COMPONENT_NAME.lower(),
            '%rootDir%': COMPONENT_NAME,
            '%title%': COMPONENT_NAME
        }).save()

        File(join(Wordpress.SCSS_PATH, f'_{COMPONENT_NAME.lower()}.scss'), path_type=ABS).save()

        COMPONENT = Component()
        COMPONENT.name = COMPONENT_NAME
        COMPONENT.style['name'] = '_' + COMPONENT_NAME.lower() + '.scss'

        Wordpress.addBlockConfigJSEntry(COMPONENT, join(COMPONENTS_PATH, COMPONENT_NAME))

        sysout(f'Component "{COMPONENT_NAME}" created successfully !', type='success', new_line=True)
