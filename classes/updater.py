from _global import *
from classes.config import Config
import requests
import urllib.parse


class Updater:

    @staticmethod
    def check(no_logs=False):

        headers = {
            'PRIVATE-TOKEN': Config.get('GITLAB_TOKEN')
        }
        encoded_file = urllib.parse.quote('_global.py')
        url = F"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/files/{encoded_file}/raw"

        response = requests.get(url, headers=headers)
        
        try:
            version = response.text.split('VERSION = ')[1].split('\n')[0].replace("'", '')

            if response.status_code == 200:
                if version != VERSION:
                    if not no_logs:
                        sysout(f'&aNew version available! &7(&9v{VERSION} → &9v{version}&7)')
                        sysout('&7Please run &9"aky update"&7 to update to latest version.')
                        exit()
                    return True
                return False
            else:
                sysout('&cFailed to check for updates.')
                return False

        except Exception as e:
            sysout('&cFailed to check for updates.')
            return False

    @staticmethod
    def update():
        # save current configuration
        configuration = Config.readConfiguration()

        # pull latest version
        if System.execute(f'git pull') != 0:
            err('Failed to update.')
        sysout('&aSuccessfully updated to latest version.')

        # restore configuration w/ new values
        _configuration = Config.readConfiguration()
        for key in _configuration:
            if key not in configuration:
                configuration[key] = _configuration[key]

        if not Config.writeConfiguration(configuration):
            err('Failed to update configuration.')

        sysout('&aSuccessfully updated configuration.')

