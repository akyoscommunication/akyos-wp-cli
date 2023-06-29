import os
from classes.wordpress import Wordpress
from classes.system import System
from classes.config import Config
from classes.component import Component
from _global import *
from commands.doctor import doctor_cmd
from modules.loader import Loader
from os.path import join
from modules.file import *
import shutil
import _global
from dotenv import *
from commands.database.replace import dbimport_cmd
from time import sleep


def generateSalts():
    salts = []
    for _ in range(8):
        salts.append(System.generateRandomString(length=64))
    return salts


class createproject_cmd:
    LOGS = False

    ERRORS = {
        'General': False,
        'Setup': False,
        'Dotenv': False,
        'Database': False,
        'Wordpress': False,
        'Files': False,
        'Plugins': False,
        'Theme': False,
        'Pages': False,
        'Configuration': False,
        'Gitlab': False,
        'Finish': False
    }

    @staticmethod
    def description():
        return "create a new sage project"

    @staticmethod
    def usage():
        return "&7aky project:create &9<project_name> &b[-l]" \
               "\n&9-l, --logs: &7Show advanced logs, good for debugging"

    @staticmethod
    def group():
        return UNDEFINED

    @staticmethod
    def execute(_command):

        # ========================== GENERAL SETUP ========================== #

        if '--logs' in _command.args or '-l' in _command.args:
            createproject_cmd.LOGS = True
            sysout('Logs enabled !\n', type='info')

        if len(_command.args) == 0:
            projectName = sysin('Enter the name of the project')  # get & check project name
        else:
            projectName = _command.args[0]

        if not projectName:
            err('Project name is required')
        if os.path.exists(projectName):
            err(f'Project "{projectName}" already exists')

        loader = Loader(message='Creating project...').start()
        if System.execute(f'composer create-project roots/bedrock {projectName}') != 0:  # try to create bedrock project
            System.clearTerminal()
            err('Unable to create project, try running "composer create-project roots/bedrock <project_name>" manually for more infos')

        loader.infos('Removing web/wp...')
        os.chdir(join(PROJECT_PATH, projectName))  # cd into project dir
        Wordpress.ROOT_FOLDER = join(PROJECT_PATH, projectName)
        shutil.rmtree(join(PROJECT_PATH, projectName, 'web', 'wp'), ignore_errors=True)  # remove web/wp dir

        # ========================== WORDPRESS SETUP ========================== #
        loader.infos('Downloading Wordpress...')
        Wordpress.cli('core download --locale=fr_FR --force --skip-content', quiet=True)  # download wordpress
        loader.print('&aWordpress downloaded successfully !')

        loader.infos('Cloning Akyos resources...')
        # if System.execute(
        #         'git clone https://gitlab.com/akyos-wp/ressources-wp.git akyos_res') != 0:  # download akyos ressources
        #     System.clearTerminal()
        #     err('Unable to download akyos ressources, try running "git clone'
        #         'https://gitlab.com/akyos-wp/ressources-wp.git akyos_res" for error logs')

        if not System.gitCloneWithAuth('akyos-wp/ressources-wp', 'akyos_res'):  # download akyos ressources
            err('Unable to clone akyos-wp/ressources-wp, please check your gitlab token in config/config.json')

        loader.print('&aAkyos resources cloned successfully !')

        loader.infos('Copying config files...')
        PROJECT = join(PROJECT_PATH, projectName)
        RESOURCES = join(PROJECT, 'akyos_res')
        shutil.copytree(join(RESOURCES, 'config'), join(PROJECT, 'config'), dirs_exist_ok=True)  # copy config

        loader.print('&aResources copied successfully !\n')

        # ========================== CONFIGURE .ENV ========================== #

        loader.suspend()

        DOTENV = join(PROJECT, '.env')

        DB_NAME = sysin('Enter the name of the database (leave blank for default)')  # get database name
        DB_NAME = DB_NAME if DB_NAME else projectName.lower()

        DB_USER = sysin('Enter the username of the database (leave blank for default)')  # get database username
        DB_USER = DB_USER if len(DB_USER) != 0 else Config.get('PRESETS')['DB_USER']

        DB_PASSWORD = sysin('Enter the password of the database (leave blank for default or type "e" if empty)')  # get database password
        # DB_PASSWORD = DB_PASSWORD if len(DB_PASSWORD) != 0 else Config.get('PRESETS')['DB_PASSWORD']
        DB_PASSWORD = '' if DB_PASSWORD == 'e' else (DB_PASSWORD if len(DB_PASSWORD) != 0 else Config.get('PRESETS')['DB_PASSWORD'])

        DB_HOST = sysin('Enter the host of the database (leave blank for default)')  # get database host
        DB_HOST = DB_HOST if len(DB_HOST) != 0 else Config.get('PRESETS')['DB_HOST']

        SITE_URL = sysin('Enter the url of the site (leave blank for default)')  # get site url
        SITE_URL = SITE_URL if len(SITE_URL) != 0 else Config.get('PRESETS')['SITE_URL']

        DB_PREFIX = sysin('Enter the prefix of the database (leave blank for default)')  # get database prefix
        DB_PREFIX = DB_PREFIX if len(DB_PREFIX) != 0 else projectName[:3].lower() + '_'

        SALTS = generateSalts()

        loader.resume()
        loader.infos('Configuring .env...')

        Wordpress.setEnv(DOTENV, {
            'DB_NAME': DB_NAME,
            'DB_USER': DB_USER,
            'DB_HOST': DB_HOST,
            'DB_PASSWORD': DB_PASSWORD,
            'DB_PREFIX': DB_PREFIX,
            'WP_HOME': SITE_URL,
            'WP_ENV': 'development',
            'WP_SITEURL': "${WP_HOME}/wp",
            'ACF_PRO_KEY': Config.get('ACF_PRO_KEY'),
            'AUTH_KEY': SALTS[0],
            'SECURE_AUTH_KEY': SALTS[1],
            'LOGGED_IN_KEY': SALTS[2],
            'NONCE_KEY': SALTS[3],
            'AUTH_SALT': SALTS[4],
            'SECURE_AUTH_SALT': SALTS[5],
            'LOGGED_IN_SALT': SALTS[6],
            'NONCE_SALT': SALTS[7],
        })  # set env

        loader.print('&aDotenv created successfully !', new_line=True)

        # ========================== CREATE DATABASE ========================== #

        loader.infos('Creating database...')

        db_passwd = '' if (DB_PASSWORD == 'e' or DB_PASSWORD == '') else f'-p{DB_PASSWORD} '

        dbimport_cmd.createDatabase({
            'DB_NAME': DB_NAME,
            'DB_USER': DB_USER,
            'DB_HOST': DB_HOST,
        }, db_passwd)  # create database

        loader.print('&aDatabase created successfully !\n')

        # ========================== SETUP WORDPRESS ========================== #

        loader.suspend()

        SITE_NAME = sysin('Enter the name of the site')  # get site name
        ADMIN_USERNAME = 'admin_' + SITE_NAME[:3].lower()  # generate admin username
        PASSWORD = System.generateRandomString(length=16)  # generate password

        ADMIN_EMAIL = sysin('Enter the email of the admin (leave blank for default)')  # get admin email
        ADMIN_EMAIL = ADMIN_EMAIL if len(ADMIN_EMAIL) != 0 else Config.get('PRESETS')['ADMIN_EMAIL']

        COMMAND = f'core install --url={SITE_URL} --title={SITE_NAME} --admin_user={ADMIN_USERNAME} ' \
                  f'--admin_password={PASSWORD} --admin_email={ADMIN_EMAIL}'

        print('\n')
        loader.infos('Installing WordPress...')
        loader.resume()

        Wordpress.cli(COMMAND, quiet=True)  # install wordpress
        Wordpress.cli('core update', quiet=True)  # update wordpress

        loader.print(f'&aWordpress installed successfully ! &7(&9v{Wordpress.getWPVersion()}&7)')

        # ========================== ADDITIONAL FILES ========================== #

        File(join(PROJECT, '.htaccess'), path_type=ABS) \
            .copyContent(join(RESOURCES, 'htaccess', '.htaccess'), path_type=ABS).save()

        File(join(PROJECT, 'composer.json'), path_type=ABS) \
            .copyContent(assets(['templates', 'composer.json']), path_type=ABS).save(force=True)

        loader.print('&aAdditional files created successfully !')

        # sysin('\nPress enter to continue...')

        # ========================== PLUGINS ========================== #

        # loader.infos('Installing ACF Pro...')
        #
        # if System.execute('composer require composer/installers:^1.1') != 0:
        #     err('Unable to install composer/installers, try running "composer require composer/installers:^1.1" for error logs')
        #
        # if System.execute('composer config repositories.acf-installer composer '
        #                   'https://pivvenit.github.io/acf-composer-bridge/composer/v3/wordpress-plugin/ '
        #                   '--no-interaction') != 0:  # add ACF Pro repository to composer
        #     if createproject_cmd.LOGS:
        #         sysout('Unable to install ACF Pro, try running "composer config repositories.repo-name composer '
        #                'https://pivvenit.github.io/acf-composer-bridge/composer/v3/wordpress-plugin/ --no-interaction" for '
        #                'more infos', type='error')
        #
        # if System.execute(
        #         'composer config allow-plugins.pivvenit/acf-pro-installer true --no-interaction') != 0:  # allow repo to install ACF Pro
        #     err('Unable to install ACF Pro, try running "composer config allow-plugins.pivvenit/acf-pro-installer '
        #         'true --no-interaction for more infos')
        #
        # if System.execute(
        #         'composer require advanced-custom-fields/advanced-custom-fields-pro --no-interaction') != 0:  # install ACF Pro
        #     err('Unable to install advanced custom fields, try running "composer require '
        #         'advanced-custom-fields/advanced-custom-fields-pro" for error logs')
        #
        # if System.execute('composer update --no-interaction') != 0:  # update composer
        #     err('Unable to update composer, try running "composer update" for error logs')
        #
        # loader.suspend()
        # loader.print('&aACF Pro installed successfully !')

        # ========================== WPMU-DEV ========================== #

        loader.infos('Installing composer dependencies...')
        # loader.resume()

        # if os is windows: auth.json goes to project root else to .composer/auth.json
        auth_json_dir = PROJECT

        if System.getHostOS() != 'Windows':
            auth_json_dir = join(PROJECT, '.composer')
            Directory(auth_json_dir, path_type=ABS).create()

        # Directory(join(PROJECT, '.composer'), path_type=ABS).create()  # create .composer directory
        File(join(auth_json_dir, 'auth.json'), path_type=ABS) \
            .copyContent(assets(['templates', 'auth.json']), path_type=ABS) \
            .replaceContent({
            '%API_KEY%': Config.get('WPMU_DEV_API_KEY'),
        }).save()  # create auth.json file (contains WPMU DEV Key)

        # if System.execute('composer config repositories.wpmudev composer https://wpmudev.com/ --no-interaction') != 0:
        #     err('Unable to install wpmu-dev, try running "composer config repositories.wpmudev composer '
        #         'https://wpmudev.com/ --no-interaction" for error logs')
        #
        # WPMU_PLUGINS = ['wp-defender', 'wp-smush-pro', 'wp-hummingbird', 'wpmu-dev-dashboard', 'ultimate-branding',
        #                 'forminator-pro', 'smartcrawl-wordpress-seo']
        # for plugin in WPMU_PLUGINS:
        #     loader.infos(f'Installing wpmudev/{plugin}...')
        #     if System.execute(f'composer require wpmudev/{plugin} --no-interaction') != 0:
        #         err(f'Unable to install {plugin}, try running "composer require wpmudev/{plugin}" for error logs')

        if System.execute('composer update --no-interaction') != 0:
            err('Unable to update composer, try running "composer update" for error logs')

        loader.suspend()

        _plugins = []
        PLUGINS = {
            'polylang': join(RESOURCES, 'plugins', 'polylang-pro.zip'),
        }

        while confirm('Do you want to install additional plugins ?'):  # ask if user wants to install plugins
            PLUGIN = sysin('Enter the name of the plugin')  # get plugin name
            _found = True
            if PLUGIN in PLUGINS:  # if plugin in resources
                Wordpress.cli(f'plugin install {PLUGINS[PLUGIN]}', quiet=True)

            elif Wordpress.pluginExist(PLUGIN):  # if plugin exist in wp database
                Wordpress.cli(f'plugin install {PLUGIN}', quiet=True)

            else:  # else throw error
                _found = False
                sysout(f'Plugin &7"{PLUGIN}" &cnot found', type='error')

            if _found:
                _plugins.append(PLUGIN)  # add plugin to list
                sysout(f'&a{PLUGIN} installed successfully !\n')

        Wordpress.cli('plugin activate --all', quiet=True)  # activate all plugins

        if len(_plugins) > 0:
            print('\n')
            loader.print(f'&aPlugins installed successfully ! (&9{len(_plugins)}&a)')
            for plugin in _plugins:
                plugin_infos = Wordpress.getPluginInfos(plugin)
                plugin_name = plugin_infos['name']
                plugin_version = plugin_infos['version']
                loader.print(f'&9→ {plugin_name} &7| v&9{plugin_version}')
        else:
            loader.print('&7Plugins installation skipped !')

        print('\n')
        loader.infos('Configuring WordPress...')
        loader.resume()

        # ========================== MU-PLUGINS ========================== #

        File(join(PROJECT, 'web', 'app', 'mu-plugins', 'custom-post-type.php'), path_type=ABS) \
            .copyContent(join(RESOURCES, 'mu-plugins', 'custom-post-type.php'), path_type=ABS).save()

        File(join(PROJECT, 'web', 'app', 'mu-plugins', 'custom-taxonomy.php'), path_type=ABS) \
            .copyContent(join(RESOURCES, 'mu-plugins', 'custom-taxonomy.php'), path_type=ABS).save()

        loader.print('&aMu-plugins installed successfully !')

        # ========================== THEME ========================== #

        loader.infos('Installing &9Akyos &7theme...')
        # if System.execute("git clone https://gitlab.com/akyos-wp/akyos-sage.git " + join(RESOURCES, 'akyos-sage')) != 0:
        #     System.clearTerminal()
        #     err('Unable to clone theme, try running "git clone https://gitlab.com/akyos-wp/akyos-sage.git" for error '
        #         'logs')
        if not System.gitCloneWithAuth('akyos-wp/akyos-sage', join(RESOURCES, 'akyos-sage')):  # download akyos theme
            err('Unable to clone akyos-wp/akyos-sage, please check your gitlab token in config/config.json')

        CLONED_THEME = join(RESOURCES, 'akyos-sage')  # get cloned theme path
        System.rmtree(join(CLONED_THEME, '.git'))  # remove .git directory | catch permission error (fuck windows)
        shutil.copytree(CLONED_THEME, join(PROJECT, 'web', 'app', 'themes', 'akyos-sage'))  # copy theme
        Wordpress.cli(f'theme activate akyos-sage/resources', quiet=True)  # activate theme
        os.chdir(join(PROJECT, 'web', 'app', 'themes', 'akyos-sage'))  # change directory

        if System.execute('composer install --no-interaction --ignore-platform-reqs') != 0:  # install theme
            System.clearTerminal()
            err('Unable to install theme, try running "composer install" for error logs')

        loader.print('&aTheme installed successfully !')

        # ======================= BUILD ASSETS ====================== #

        loader.infos('Installing node_modules... (this may take a while)')
        System.yarnInstall(os.getcwd())
        if not os.path.exists(join(PROJECT, 'web', 'app', 'themes', 'akyos-sage', 'node_modules')):  # install node_modules using yarn
            err('Unable to install node_modules, try running "yarn install" for error logs')

        loader.print('&aNode_modules installed successfully !')
        loader.infos('Building assets...')
        # if System.execute('yarn build') != 0:  # build assets using yarn
        #     err('Unable to build assets, try running "yarn build" for error logs')

        # use os.system to run yarn build because yarn build dont retrun exit code 0 on finish
        # note that can't check if yarn build finish successfully or not because of os.system
        # also yarn build return 1 on error but return nothing on success so we can't check if yarn build has finish
        # so all we can do it run yarn build with os.system and after check if dist folder exist or not
        System.yarnBuild(os.getcwd())
        if not os.path.exists(join(PROJECT, 'web', 'app', 'themes', 'akyos-sage', 'dist')):
            err('Unable to build assets, try running "yarn build" for error logs')

        loader.print('&aAssets built successfully !')

        os.chdir(PROJECT)  # change directory

        # ========================== PAGES ========================== #

        loader.infos('Creating pages / menus...')

        Wordpress.cli('post delete 1', quiet=True)  # delete page 1
        Wordpress.cli('post delete 2', quiet=True)  # delete page 2
        Wordpress.cli('menu create Menu%_Principal', replace=True, quiet=True)  # create menu
        Wordpress.cli('menu create Menu%_Footer', replace=True, quiet=True)  # create menu
        Wordpress.cli('menu create Menu%_Copyright', replace=True, quiet=True)  # create menu
        Wordpress.cli('menu location assign menu-principal primary_navigation', quiet=True)  # assign menu to location
        Wordpress.cli('post create --post_type=page --post_title=Accueil --post_status=publish', quiet=True)

        print('\n')
        loader.suspend()

        _continue = confirm('Do you want to create additional pages')  # Add additional pages
        while _continue:
            PAGE_NAME = sysin('Enter the name of the page').replace(' ', '%_')
            Wordpress.cli(f'post create --post_type=page --post_title={PAGE_NAME} --post_status=publish', quiet=True, replace=True)
            if not confirm('Do you want to create additional pages'):
                _continue = False

        HOME_PAGE_ID = Wordpress.cli('eval echo(get_page_by_path("accueil")->ID);', output=True)  # get home page id
        Wordpress.cli(f'option update show_on_front {HOME_PAGE_ID}', quiet=True)  # set static page instead of post list
        Wordpress.cli(f'option update page_on_front {HOME_PAGE_ID}', quiet=True)  # set home page id

        sysout('Pages and menus created successfully ! \n', type='success')

        # ========================== CONFIGURATIONS ========================== #

        SITE_DESCRIPTION = sysin('Enter the site description (leave blank for default)').replace(' ', '%_')
        Wordpress.cli(f'option update blogdescription "{SITE_DESCRIPTION}"', quiet=True)  # set site description

        Wordpress.cli('option update blog_public 0', quiet=True)  # no public access
        Wordpress.cli('option update gzipcompression 1', quiet=True)  # gzip compression
        Wordpress.cli('option update default_comment_status "closed"', quiet=True)  # comments closed
        Wordpress.cli('rewrite structure "%postname%/"', quiet=True)  # rewrite structure
        Wordpress.cli('rewrite flush', quiet=True)  # flush rewrite rules
        Wordpress.cli('option update category_base categorie', quiet=True)  # set category base

        LOGIN_URL = sysin('Enter the login page URL (leave blank for default)')
        if len(LOGIN_URL) == 0:
            LOGIN_URL = ADMIN_USERNAME
        Wordpress.cli(f'option update login_url "{LOGIN_URL}"', quiet=True)  # set login URL

        sysout('Configurations updated successfully !', type='success')

        # ========================== COMPONENTS ========================== #

        _continue = confirm('Do you want to import &9Akyos component&7')  # Add components
        while _continue:
            COMPONENT_ID = sysin('Enter component ID')

            loader.infos('Installing component &9#' + COMPONENT_ID + '&7...')
            loader.resume()
            COMPONENT = Component.fetchFromID(COMPONENT_ID)
            loader.suspend()

            if str(type(COMPONENT)) == "<class 'list'>":
                sysout(f'Error while fetching component &7#{COMPONENT_ID} \n&7[ &9> &7] {COMPONENT[1]}\n', type='error')
                continue

            COMPONENT.install(PROJECT)
            sysout(f'Component &9{COMPONENT.name}&a imported successfully !', type='success')
            if not confirm('Do you want to import &9Akyos components&7'):
                _continue = False

        # ========================== GITLAB ========================== #

        _github_repo = True

        if not confirm('Do you want to create a GitLab repository'):
            sysout('GitLab repository creation skipped !', type='info')
            _github_repo = False
        else:
            sysout('Creating GitLab repository...', type='info')
            #  create gitlab repository from api
            System.createGitlabRepository(projectName)

            if System.execute('git init') != 0:
                System.clearTerminal()
                err('Unable to initialize git, try running "git init" for error logs')

            if System.execute(f'git remote add origin https://gitlab.com/akyos-wp/{projectName}.git') != 0:
                System.clearTerminal()
                err(f'Unable to add remote, try running "git remote add origin https://gitlab.com/akyos-wp/{projectName}.git" '
                    f'for error logs')

            if System.execute('git add .') != 0:
                System.clearTerminal()
                err('Unable to add files, try running "git add ." for error logs')

            if System.execute('git commit -m "Initial commit"') != 0:
                System.clearTerminal()
                err('Unable to commit files, try running "git commit -m "Initial commit" for error logs')

            if System.execute('git push -u origin master') != 0:
                System.clearTerminal()
                err('Unable to push files, try running "git push -u origin master" for error logs')

            sysout('GitLab repository created successfully !', type='success')

        # ========================== DONE ========================== #

        System.rmtree(RESOURCES)  # remove resources folder

        print('\n' + c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━&7[ &9Setup Finished &7]&9━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        print('\n' + c('&a→ Project created successfully !'))
        print(c(f'&7→ You can start the server using &9"aky project:serve"'))
        print(c(f'&7→ It\'s recommended to save the password in a secure place !'))
        if _github_repo:
            print(c('&7You can access your project at &9https://gitlab.com/akyos-wp/' + projectName))
        print('\n' + c('&9Website Informations &7→'))
        print('\n' + c('&9 Name &7→ &9' + SITE_NAME))
        print(c('&9 URL &7→ &9' + SITE_URL))
        print(c(f'&9 Admin URL &7→ &9{SITE_URL}/{LOGIN_URL}'))
        print(c('&9 Admin &7→ &9' + ADMIN_USERNAME))
        print(c('&9 Email &7→ &9' + ADMIN_EMAIL))
        print(c('&9 Password &7→ &9' + PASSWORD))
        print(c('&9 Database &7→ &9' + DB_NAME))
        print(c('&9 Prefix &7→ &9' + DB_PREFIX))
        print(c('&9 Wordpress &7→ v&9' + Wordpress.getWPVersion() + ' &7(&9latest&7)'))
        print('\n' + c('&9━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
