class CommandManager:
    def __init__(self):
        self.commands = {}

    def register(self, command, fn):
        self.commands[command] = fn

    def exist(self, command):
        _type = str(type(command))
        if _type == "<class 'str'>":
            return command in self.commands.keys()
        elif _type == "<class 'app.core.commands.Command'>":
            return command.arg in self.commands.keys()

    def invoke(self, command):
        _COMMAND = self.get(command)
        _COMMAND.execute(command)

    def exec(self, command_name):
        """Execute command outside CLI lifecycle"""
        _command = Command([command_name])
        return self.commands[_command.arg].execute(_command)

    def get(self, command):
        """Get command object"""
        if self.exist(command):
            return self.commands[command.arg]
        return None

    @staticmethod
    def isDev(command):
        """Check if command is available only in dev environment"""
        _env = PRODUCTION_ENV
        try:
            _env = command.env()
        except AttributeError:
            pass
        return _env == DEVELOPMENT_ENV

    @staticmethod
    def registerCommands():
        pass
        # commandHandler = _global.HANDLER
        #
        # commandHandler.register('help', help_cmd)
        # commandHandler.register('doctor', doctor_cmd)
        # commandHandler.register('update', update_cmd)
        #
        # commandHandler.register('component:create', create_cmd)
        # commandHandler.register('component:import', import_cmd)
        # commandHandler.register('component:export', export_cmd)
        #
        # commandHandler.register('project:create', createproject_cmd)
        # commandHandler.register('project:install', install_cmd)
        # commandHandler.register('project:serve', serve_cmd)
        # commandHandler.register('project:build', build_cmd)
        # commandHandler.register('project:push', push_cmd)
        #
        # commandHandler.register('database:replace', replace_cmd)
        # commandHandler.register('database:import', dbimport_cmd)
        # commandHandler.register('database:dump', dump_cmd)
        #
        # commandHandler.register('test', test_cmd)