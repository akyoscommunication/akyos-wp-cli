def assets(args):
    asset_path = os.path.join(SCRIPT_PATH, 'assets')
    for path in args:
        asset_path = os.path.abspath(os.path.join(asset_path, path))
    return asset_path


def sysin(message, new_line=False):
    line = '\n' if new_line else ''
    try:
        return input(line + c(f'&7[ &9> &7] {message} :\n[ &9> &7] &9', False))
    except KeyboardInterrupt as e:
        print('\033[F\033[K')
        sysout('&9Goodbye')
        print('')
        exit()


def sysout(message, new_line=False, type='default', reset=True, start_of_line=False, color=False):
    color_code = '&a' if type == 'success' else '&c' if type == 'error' else '&e' if type == 'warning' else '&9'
    message = '&a' + message if type == 'success' else '&c' + message if type == 'error' else '&e' + message if type == 'warning' else message
    line = '\n' if new_line else ('\033[F' if start_of_line else '')
    color_code = color if color else color_code
    print(line + c(f'&7[ {color_code}> &7] {message}', reset))


def err(message, start_of_line=False):
    sysout(message, type='error', start_of_line=start_of_line)
    exit()


def confirm(message, warning=False):
    _continue = ''
    message = ('&6WARNING : &7' + message if warning else message) + ' (y/n)'
    while _continue not in ['y', 'Y', 'n', 'N']:
        _continue = sysin(message, True)
    if _continue in ['n', 'N']:
        return False
    return True


def ex():
    print('')
    sysout('&9Goodbye')
    exit()