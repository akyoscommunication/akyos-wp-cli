class Command:

    _globals = ['help', 'doctor', 'test', 'update', 'project:create', 'project:install']
    _no_doctor = ['help', 'doctor', 'test', 'update']
    _no_updater = ['help', 'doctor', 'test', 'update']

    def __init__(self, arguments, _silent=False):
        self.command = ' '.join(arguments)
        if not self.check(arguments):
            exit()
        self.arg = arguments[0]
        self.args = arguments[1:]
        self.silent = _silent

    def check(self, arguments):

        WP_INSTALLATION = Wordpress.getWordpressInstallation()
        if len(self.command) == 0:
            print(c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━&7[ &9Akyos CLI &7]&9━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
            print(c('&9 Akyos CLI &7→ &7v&9' + _global.VERSION + ' &7(&9' + Config.get('APP_ENV') + '&7)'))
            if WP_INSTALLATION != UNDEFINED:
                print(c(f'&9 Wordpress &7(&9{Wordpress.getWordpressInstallation()}&7) &7→ &7v&9' + Wordpress.getWPVersion()))
            print(c('&9 → &7Type &9aky help &7to see a list of commands'))
            print(c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
            return False

        if arguments[0] not in self._no_updater:
            Updater.check()

        if WP_INSTALLATION == UNDEFINED and arguments[0] not in self._globals:
            sysout('Wordpress installation not found, please move to wordpress project folder.', type="error")
            return False

        return True

    def __str__(self) -> str:
        string = 'Command(\n'
        string += '   command : ' + self.command + '\n'
        string += '   arg : ' + str(self.arg) + '\n'
        string += '   args : ' + str(self.args) + '\n'
        string += ')'
        return string