from classes.system import System
from _global import *


class push_cmd():

    @staticmethod
    def description():
        return "commit and push to git\n"

    @staticmethod
    def execute(_command):

        if len(_command.args) == 0:
            COMMIT_MESSAGE = sysin('Enter commit message [ex: "fix: style"]', True).replace(' ', '%_')
        else:
            COMMIT_MESSAGE = _command.args[0]

        if System.execute('git add -A') != 0:
            err('Unable to add files to git, try running "git add -A" for more logs')

        commit_code = System.execute(f'git commit -m {COMMIT_MESSAGE}', type='raw')
        if commit_code != 0:
            if commit_code == 1:
                sysout('Unable to create commit, your branch is already up to date', new_line=True)
                exit()
            else:
                err('Unable to create commit, try running "git commit -m {message}" for more logs')

        if System.execute('git push') != 0:
            user_input = ''
            while user_input not in ['y', 'Y', 'n', 'N']:
                print(user_input)
                user_input = sysin('Unable to push to git, retry using --force ? [y/n]')

            if user_input in ['y', 'Y']:
                if System.execute('git push -f') != 0:
                    err('Unable to push files to git, try running "git push" for more logs')
            else:
                sysout('Changes not pushed to git, try running "git push" manually for more logs')
                exit()
