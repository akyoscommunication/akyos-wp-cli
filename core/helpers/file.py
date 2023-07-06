import os

exists = os.path.exists

EXEC = 0  # current execution dir
SCRIPT = 1  # original script dir
ABS = 2  # absolute path


class File:

    def __init__(self, fullpath, path_type=EXEC, content=False):

        self._content = content

        if path_type == SCRIPT:
            self.path = os.path.abspath(os.path.join(__file__, '../../app', '..'))
        if path_type == EXEC:
            self.path = os.path.abspath(os.getcwd())
        if path_type == ABS:
            self.path = fullpath

        if path_type != ABS:
            for _dir in fullpath.split('/'):
                self.path = os.path.abspath(os.path.join(self.path, _dir))

    def save(self, force=False, log=False) -> None:
        if not exists(self.path) or force:
            with open(self.path, 'w') as file:
                if self._content != False:
                    file.write(self._content)
                file.close()
            if log:
                print('File written in ' + self.path)

    def content(self) -> str:
        content = ""
        with open(self.path, 'r') as file:
            for line in file.readlines():
                content += line
            file.close()
        return content

    def obj_content(self):
        return self._content

    def setContent(self, content):
        self._content = content
        return self

    def copyContent(self, path, path_type=SCRIPT):
        file_obj = File(path, path_type)
        self._content = file_obj.content()
        return self

    def empty(self):
        self._content = ''
        return self

    def replaceContent(self, arguments):
        for args in arguments.keys():
            self._content = self._content.replace(args, arguments[args])
        return self

    def erase(self) -> None:
        self._content = False
        self.create(force=True)

    @staticmethod
    def cut(path, string_start, string_end, path_type=SCRIPT):
        FILE_CONTENT = File(path, path_type).content()
        FILE_CONTENT = FILE_CONTENT[FILE_CONTENT.find(string_start):]
        FILE_CONTENT = FILE_CONTENT[:FILE_CONTENT.find(string_end)]
        CURSOR = len(FILE_CONTENT)

        # cut file at closing tag of const block
        FILE_CONTENT = File(path, path_type).content()
        FILE_START = FILE_CONTENT[:CURSOR + FILE_CONTENT.find(string_start)]
        FILE_END = FILE_CONTENT[CURSOR + FILE_CONTENT.find(string_start):]
        return FILE_START, FILE_END


class Directory:

    def __init__(self, fullpath, path_type=EXEC):

        if path_type == SCRIPT:
            self.path = os.path.abspath(os.path.join(__file__, '../../app'))
        if path_type == EXEC:
            self.path = os.path.abspath(os.getcwd())
        if path_type == ABS:
            self.path = fullpath

        if path_type != ABS:
            for dir in fullpath.split('/'):
                self.path = os.path.abspath(os.path.join(self.path, dir))

    def create(self, move=False, log=False):
        if not exists(self.path):
            os.makedirs(self.path)
            if log:
                print('Directory created at ' + self.path)
        if move:
            os.chdir(self.path)
