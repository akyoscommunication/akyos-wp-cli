import requests

from _global import *
from modules.file import File, Directory, ABS
from classes.wordpress import Wordpress
from classes.config import Config
from os.path import join


class Component:
    name = None

    block = {
        'name': None,
        'content': None
    }
    view = {
        'name': None,
        'content': None
    }
    style = {
        'name': None,
        'content': None
    }
    script = {
        'active': None,
        'name': None,
        'content': None
    }

    def __str__(self):
        return f'''Component(
        name : {self.name}
        block : {self.block}
        view : {self.view}
        style : {self.style}
        script : {self.script}
    )'''

    def install(self, _rootPath=''):

        if _rootPath != '':
            Wordpress.SCSS_PATH = join(_rootPath, 'web', 'app', 'themes', 'akyos-sage', 'resources', 'assets', 'css', 'utils', 'components')
            _COMPONENT_PATH = join(_rootPath, 'web', 'app', 'themes', 'akyos-sage', 'resources', 'views', 'components')
            Wordpress.BLOCK_CONFIG_JS = join(_rootPath, 'web', 'app', 'themes', 'akyos-sage', 'resources', 'assets', 'build', 'blocks.config.js')
        else:
            Wordpress.SCSS_PATH = join(ASSETS_PATH, 'css', 'utils', 'components')
            _COMPONENT_PATH = COMPONENTS_PATH

        COMPONENT_PATH = os.path.abspath(os.path.join(_COMPONENT_PATH, self.name))

        Directory(COMPONENT_PATH, path_type=ABS).create(move=True)
        File(f"{self.view['name']}").setContent(self.view['content']).save()
        File(f"{self.block['name']}").setContent(self.block['content']).save()
        File(join(Wordpress.SCSS_PATH, self.style['name']), path_type=ABS)\
            .setContent(self.style['content'])\
            .save()
        Wordpress.addBlockConfigJSEntry(self, COMPONENT_PATH)

    @staticmethod
    def formatName(COMPONENT_NAME):
        return COMPONENT_NAME + 'Block'

    @staticmethod
    def fetchFromID(ID):
        url = Config.get('COMPONENT_API_URL') + API_URL + f'/components/{ID}'
        req = requests.get(url).json()

        if 'code' in req and req['code'] == 500:
            return [False, req['message']]

        component = Component()
        component.name = req['name']
        component.view['name'] = req['view']['name']
        component.view['content'] = req['view']['content']
        component.block['name'] = req['block']['name']
        component.block['content'] = req['block']['content']
        component.style['name'] = req['style']['name']
        component.style['content'] = req['style']['content']

        if req['script']['has_script']:
            component.script['active'] = True
            component.script['name'] = req['script']['name']
            component.script['content'] = req['script']['content']
        else:
            component.script['active'] = False

        return component
