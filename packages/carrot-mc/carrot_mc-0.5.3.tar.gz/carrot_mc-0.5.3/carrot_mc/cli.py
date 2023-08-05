from argparse import ArgumentParser, SUPPRESS

from carrot_mc.backend import BackendService
from carrot_mc.carrot import CarrotService, InstallationManager
from carrot_mc.cli_printer import CliEventPrinter
from carrot_mc.colors import Colorizer as clr

def main():
    commands = [
        StatusCommand(),
        ListCommand(),
        InstallCommand(),
        InitCommand(),
        UpdateCommand(),
        EnableCommand(),
        DisableCommand(),
        WebGuiCommand()
    ]

    ap = ArgumentParser(prog='carrot')

    subparsers = ap.add_subparsers()

    for cmd in commands:
        cmd.register_help(subparsers)

    args = ap.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        ap.print_help()


class Command(object):
    cli_printer = CliEventPrinter()
    backend_service = BackendService()
    installation_manager = InstallationManager(backend_service, cli_printer)
    carrot_service = CarrotService(backend_service, installation_manager, cli_printer)

    def register_help(self, subparsers):
        raise NotImplementedError()

    def handle_args(self, args):
        raise NotImplementedError()


class StatusCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'status',
            help='Display a summary of current mod directory'
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        if self.carrot_service.initialized():
            carrot = self.carrot_service.get_status()

            dep_count = 0
            disabled_count = 0
            missing_file_err = []
            bad_md5_err = []

            for mod in carrot.mods:
                if mod.dependency:
                    dep_count += 1

                if mod.disabled:
                    disabled_count += 1

                if mod.file_missing:
                    missing_file_err.append(mod)
                else:
                    if mod.actual_file_md5 != mod.file.file_md5:
                        bad_md5_err.append(mod)

            print(f'Mods installed: {len(carrot.mods)}')

            if dep_count:
                print(f'of which dependencies: {dep_count}')

            if disabled_count > 0:
                print(f'Disabled mod(s): {disabled_count}')

            if len(missing_file_err) + len(bad_md5_err) == 0:
                print('All mod files seem to be in order.')
            else:
                if missing_file_err:
                    print(f'{len(missing_file_err)} mod(s) have missing files:')
                    for mod in missing_file_err:
                        print(f'\t{clr.mod_name(mod.name)}: missing file {clr.file_name(mod.file.file_name)}')

                if bad_md5_err:
                    print(f'{len(bad_md5_err)} mod(s) have possibly corrupted files:')
                    for mod in bad_md5_err:
                        actual_file_name = mod.file.file_name
                        if mod.disabled:
                            actual_file_name += '.disabled'
                        print(f'\t{clr.mod_name(mod.name)}: file {clr.file_name(actual_file_name)} has hash {clr.file_hash(mod.actual_file_md5)} instead of {clr.file_hash(mod.file.file_md5)}')

        else:
            print(clr.error('This directory does not appear to be a valid mod repo.'))


class ListCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'list',
            help='List mods installed in current directory'
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        if self.carrot_service.initialized():
            carrot = self.carrot_service.get_status()
            
            for mod in carrot.mods:
                print(f'{clr.mod_name(mod.name)} by {clr.mod_owner(mod.owner)},', end=' ')
                
                if not mod.file_missing:
                    print(f'file {clr.file_name(mod.file.file_name)}', end='')
                    
                    if mod.disabled:
                        print(clr.file_name(".disabled"), end='')
                    
                    print(' - ', end='')
                    
                    if mod.actual_file_md5 == mod.file.file_md5:
                        if not mod.disabled:
                            print(clr.ok('OK'))
                        else:
                            print(clr.warn('DISABLED'))
                    else:
                        print(clr.error('CORRUPTED'))
                
                else:
                    print(clr.error('FILE MISSING'))
                    
        else:
            print(clr.error('This directory does not appear to be a valid mod repo.'))



class InitCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'init',
            help='Initialize a mod repo in current directory.'
        )

        parser.add_argument(
            '--name',
            help='Name of this repo/modpack'
        )

        parser.add_argument(
            '--mc_version',
            help='Minecraft version',
            required=True
        )

        parser.add_argument(
            '--channel',
            help='Mod release channel',
            choices=['Alpha', 'Beta', 'Release'],
            default='Beta'
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        if self.carrot_service.initialized():
            print('ERROR! This directory is already a mod repo.')
        else:
            self.carrot_service.initialize(vars(args))
            print('Repo initialized.')


class InstallCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'install',
            help='Install a mod and its dependencies'
        )

        parser.add_argument(
            'mod_key',
            help='"Key" id of a mod *exactly* as used in e.g. CurseForge URLs. '
                 'If no mod matches exactly, a list of possible matches will be displayed.',
            nargs='+'
        )

        parser.add_argument(
            '--channel',
            help='Specify channel (Alpha/Beta/Release) to use when installing. '
                 'Overrides settings from mods.json.',
            choices=['Alpha', 'Beta', 'Release'],
            default=None
        )

        parser.add_argument(
            '--upgrade',
            help='Specify that upgrading mods to newer versions is allowed. '
                 'By default when a mod or dependency is already installed and a new version is found '
                 'during installation, it will be skipped for safety reasons.',
            nargs='?',
            const=True
        )

        parser.add_argument(
            '--downgrade',
            help='Specify that a downgrade to an older version is allowed. '
                 'This can happen e.g. if you explicitly request a Release channel but '
                 'already have a newer Beta file installed.',
            nargs='?',
            const=True
        )

        parser.set_defaults(func=self.handle_args)
    
    def handle_args(self, args):
        self.carrot_service.install(args)


class UpdateCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'update',
            help='Update a currently-installed mod (and its dependencies) or all mods to newer/older version and/or different channel.'
        )

        parser.add_argument(
            'mod_key',
            help='"Key" id of a mod to update (along with its dependencies).',
            nargs='?',
            default=None
        )

        parser.add_argument(
            '--channel',
            help='Specify target channel (Alpha/Beta/Release) to use when updating. '
                 'Overrides settings from mods.json.',
            choices=['Alpha', 'Beta', 'Release'],
            default=None
        )

        # Hidden "option" for compatibility in the installer logic
        parser.add_argument(
            '--upgrade',
            help=SUPPRESS,
            nargs='?',
            default=True
        )

        parser.add_argument(
            '--downgrade',
            help='Specify that downgrades to an older version are allowed. '
                 'This can happen e.g. if you explicitly request a Release channel but '
                 'already have newer versions of mods from the Beta channel installed.',
            nargs='?',
            const=True
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        self.carrot_service.update(args)


class EnableCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'enable',
            help='Enable a mod (by removing its ".disabled" file name suffix).'
        )

        parser.add_argument(
            'mod_key',
            help='"Key" id of a mod to enable.',
            nargs='+',
            default=None
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        self.carrot_service.enable(args)


class DisableCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'disable',
            help='Disable a mod (by appending ".disabled" to its file name).'
        )

        parser.add_argument(
            'mod_key',
            help='"Key" id of a mod to disable.',
            nargs='+',
            default=None
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        self.carrot_service.disable(args)


class WebGuiCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'web-gui',
            help='Start an interactive web GUI interface for managing mods.'
        )

        parser.add_argument(
            '--port',
            help='TCP port on which the built-in webserver will listen for connections. Default: 8877',
            default=8877
        )

        parser.add_argument(
            '--host',
            help='Host on which the built-in webserver will listen for connections. '
                 'Default: localhost/127.0.0.1 (This means it will not be accessible from other computers (RECOMMENDED)). '
                 'Change to 0.0.0.0 to listen on all available network interfaces '
                 '(REMEMBER: there is no authentication, so everyone who opens the page will be able to manage your modpack)',
            default='localhost'
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        print(f'Starting Web GUI on http://{args.host}:{args.port} - open this address in your browser')

        from carrot_mc.web_gui.app import run_socket_app
        run_socket_app(args)


if __name__ == '__main__':
    main()