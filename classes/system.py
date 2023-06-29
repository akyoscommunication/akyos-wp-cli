import platform
import subprocess
from time import sleep
import requests
import mysql.connector as conn

from _global import *
import os
import tempfile
import random
import string
import json
import sys
import socket
from classes.config import Config


class STATUS:
    STARTING = 'starting'
    RUNNING = 'running'
    STOPPED = 'stopped'


class System:

    @staticmethod
    def run(command, output=False, quiet=True, replace=True, debug=False):

        command = 'cmd /c ' + command if System.getHostOS() == 'Windows' else command

        _command = []
        for args in command.split(' '):
            if replace:
                _command.append(args.replace('%_', ' '))
            else:
                _command.append(args)
        if debug:
            sysout(_command, type='debug')

        if output:
            return subprocess.run(_command, capture_output=True)
        elif quiet:
            return subprocess.run(_command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        else:
            return subprocess.run(_command)

    @staticmethod
    def execute(command, type='noshell', debug=False, replace=True, stdout=False, shell=False):

        command = 'cmd /c ' + command if System.getHostOS() == 'Windows' else command

        _command = []
        for args in command.split(' '):
            if replace:
                _command.append(args.replace('%_', ' '))
            else:
                _command.append(args)
        if debug:
            sysout(_command, type='debug')

        if type == 'noshell':
            _stdout = subprocess.PIPE if stdout is False else open(stdout, 'w')
            process = subprocess.Popen(_command, stdout=_stdout, stderr=subprocess.PIPE, shell=shell)
            while process.poll() is None:
                sleep(0.1)
            return process.poll()

        if type == 'raw':
            # print(f'subprocess.Popen({_command}, stdout=subprocess.PIPE, universal_newlines=True, shell={shell})')
            process = subprocess.Popen(_command, stdout=subprocess.PIPE, universal_newlines=True, shell=shell)
            while True:
                # print('polling...' + str(process.poll()))
                if process.poll() is not None:
                    return process.poll()
                sleep(0.1)

    @staticmethod
    def startServer(SERVER_PORT, logs=False):
        command = f'php -a -S 127.0.0.1:{SERVER_PORT}'
        _command = command.split(' ')
        process = subprocess.Popen(_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # output = process.communicate()[0]
        # exitCode = process.returncode
        #
        # if exitCode == 0:
        #     return output
        # else:
        #     raise Exception(command, exitCode, output)

        status = STATUS.STARTING
        while status == STATUS.STARTING:
            log = process.stdout.readline().strip()
            if log == '':
                continue

            if 'Failed to listen' in log:
                err('Unable to start development server : port already in use')
            if 'started' in log:
                sysout(f'Server started successfully (http://127.0.0.1:{SERVER_PORT})', type='success')
                print('')
                status = STATUS.RUNNING
            else:
                err(f'Unable to start development server : {log}')

        while True:
            try:
                server_log = process.stdout.readline()
                if server_log == '' and process.poll() is not None:
                    break

                server_log = server_log.strip()
                server_log = server_log.split('127.0.0.1')
                del server_log[0]
                server_log = ' '.join(server_log)[1:]

                is_info_message = True if 'accepted' in server_log.lower() else (True if 'closing' in server_log.lower() else False)
                if is_info_message and not logs:
                    continue

                color = '&a' if 'accepted' in server_log.lower() else ('&c' if 'closing' in server_log.lower() else '&9')
                color = '&c' if 'error' in server_log.lower() or 'no such file or directory' in server_log.lower() else color

                if color != '&c':
                    server_log = server_log.replace('POST', '&7POST' + color)
                    server_log = server_log.replace('GET', '&aGET ' + color)

                sysout(color + '127.0.0.1:' + server_log, color=color)

                sys.stdout.flush()
            except KeyboardInterrupt:
                process.kill()
                print('')
                sysout('&cServer stopped', type='info', new_line=True, color='&c')
                break
        #
        # while True:
        #     stdout = sys.stdout
        #     try:
        #         stdout.flush()
        #     except Exception as e:
        #         pass
        #     sleep(0.1)

            # if stdout is not None:
            #     line = stdout.readline().strip()
            #     if line == '':
            #         continue
            #     sysout(line)
            # print('stdout is none')
            # sleep(0.1)

        # while status == STATUS.RUNNING:
        #     try:
        #         stdout, stderr = process.communicate()
        #         print(stdout, stderr)
        #         if stdout == '':
        #             continue
        #     except KeyboardInterrupt as e:
        #         process.kill()
        #         print('')
        #         sysout('PHP Server stopped', type='info', start_of_line=True)
        #         status = STATUS.STOPPED
        #         break

    @staticmethod
    def clearTerminal():
        command = {
            'Windows': 'cls',
            'Linux': 'clear',
            'Darwin': 'clear'
        }
        os.system(command[System.getHostOS()])

    @staticmethod
    def getHostOS():
        return platform.system()

    @staticmethod
    def getHostUserFolder():
        try:
            return os.path.expanduser('~')
        except Exception as e:
            return ''

    @staticmethod
    def getTempDir():
        try:
            return tempfile.gettempdir()
        except Exception as e:
            return ''

    @staticmethod
    def generateRandomString(length):
        return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))\
               .replace(' ', '_').replace('&', '_').replace('"', '_').replace("'", '_').replace('`', '_')\
               .replace('(', '_').replace('$', '_').replace('%', '_')

    @staticmethod
    def output(_output):
        return _output.stdout.decode('utf-8')

    @staticmethod
    def createGitlabRepository(projectName):
        HEADER = 'Content-Type:application/json'
        BASE_URL = 'https://gitlab.com/api/v4/projects?private_token=' + Config.get('GITLAB_TOKEN')
        REPOSITORY_URL = BASE_URL + '&name=' + projectName
        REPOSITORY_CREATE_URL = REPOSITORY_URL + '&visibility=private'
        REPOSITORY_CREATE_RESPONSE = System.run(f'curl -X POST -H "{HEADER}" "{REPOSITORY_CREATE_URL}"', output=True)
        if REPOSITORY_CREATE_RESPONSE.returncode != 0:
            err(f'Unable to create repository "{projectName}"')
        else:
            sysout(f'Repository "{projectName}" created successfully', type='success')
            return json.loads(System.output(REPOSITORY_CREATE_RESPONSE))['ssh_url_to_repo']

    @staticmethod
    def methodExist(_class, method):
        try:
            _method = getattr(_class, method)
            return True
        except AttributeError:
            return False

    @staticmethod
    def hasDeleteFilePermission(file_path):
        file_dirname = os.path.dirname(file_path)  # get the directory name of file_path

        if os.access(file_dirname, os.W_OK | os.X_OK):  # if folder containing file_path has write, execute permission
            try:  # if file_path can be opened for write
                file = open(file_path, 'w')  # Attention: This will delete all the content from the file
                file.close()
                return True  # file_path is a file and has write permission and is not locked
            except OSError:  # if file_path can't be opened for write
                pass  # file_path is not a file, or don't has write permission or is locked

        return False

    @staticmethod
    def getPHPVersion():
        php_version_output = System.output(System.run('php -v', output=True))
        php_full_version = php_version_output.split('PHP ')[1].split(' ')[0].split('.')
        php_version = php_full_version[0] + '.' + php_full_version[1]
        return php_version

    @staticmethod
    def isInstalled(binary, version_command='-v'):
        try:
            if System.run(binary + ' ' + version_command, output=True).returncode == 0:
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def isReachable(url):
        try:
            requests.get(url)
            return True
        except Exception as e:
            return False

    @staticmethod
    def yarnBuild(build_path):
        command = 'yarn build > /dev/null 2>&1' if System.getHostOS() != 'Windows' else 'yarn build > NUL 2>&1'
        actual_directory = os.getcwd()
        os.chdir(build_path)
        os.system(command)
        os.chdir(actual_directory)

    @staticmethod
    def yarnInstall(build_path):
        command = 'yarn install > /dev/null 2>&1' if System.getHostOS() != 'Windows' else 'yarn install > NUL 2>&1'
        actual_directory = os.getcwd()
        os.chdir(build_path)
        os.system(command)
        os.chdir(actual_directory)

    @staticmethod
    def gitCloneWithAuth(repository, destination=False):
        """repository = akyos-wp/ressources-wp"""
        auth_url = f'https://gitlab-ci-token:{Config.get("GITLAB_TOKEN")}@gitlab.com/{repository}.git'
        destination = '' if not destination else ' ' + str(destination)
        # print('\n\n\n' + f'git clone {auth_url}{destination}' + '\n\n\n')
        if System.execute(f'git clone {auth_url}{destination}') == 0:
            return True
        return False

    @staticmethod
    def rmtreeHandler(func, path, exc_info):
        """
            Error handler for ``shutil.rmtree``.

            If the error is due to an access error (read only file)
            it attempts to add write permission and then retries.

            If the error is for another reason it re-raises the error.

            Usage : ``shutil.rmtree(path, onerror=System.rmtreeHandler)``
        """
        import stat

        # Is the error an access error?
        if not os.access(path, os.W_OK):
            # Try to change the file permissions
            try:
                os.chmod(path, stat.S_IWUSR)
                func(path)
            # Error raised when permission denied
            except PermissionError as e:
                sysout(f'Unable to delete {path} this is most likely due to a permission error', type='error')
        else:
            sysout(f'Unable to delete {path} this is most likely due to a permission error', type='error')


    @staticmethod
    def rmtree(path):
        import shutil, git

        try:
            shutil.rmtree(path)
        except PermissionError as e:
            try:
                git.rmtree(path)
            except PermissionError as e:
                sysout(f'Unable to delete {path} this is most likely due to a permission error', type='error')

    @staticmethod
    def isMySQLConnectionCorrect():
        pres = Config.get('PRESETS')
        # pres["DB_HOST"] = System.getHostIP() if pres["DB_HOST"] == '%HOST%' else pres["DB_HOST"]
        try:
            if pres['DB_PASSWORD'] == '':
                conn.connect(host=pres['DB_HOST'], user=pres['DB_USER'])
            else:
                conn.connect(host=pres['DB_HOST'], user=pres['DB_USER'], password=pres['DB_PASSWORD'])
            return True
        except Exception as e:
            return False

    # @staticmethod
    # def getHostIP():
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     try:
    #         sock.connect(("8.8.8.8", 80))
    #         ip_address = sock.getsockname()[0]
    #         return ip_address
    #     finally:
    #         sock.close()

