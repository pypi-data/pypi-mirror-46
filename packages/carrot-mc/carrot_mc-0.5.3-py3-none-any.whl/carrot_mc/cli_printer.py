from carrot_mc.colors import Colorizer as clr

class CliEventPrinter:
    def handle(self, event: str, payload=None):
        method_name = 'handle_' + event.replace(' ', '_')
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(payload)

    def handle_info(self, payload):
        print(payload)

    def handle_info_mod_resolved(self, payload):
        print(f'{clr.mod_key(payload.mod_key)} resolved as {clr.mod_name(payload.mod.name)}')

    def handle_info_all_mod_check_complete(self, payload):
        print('Mod check phase complete. Proceeding to download...')

    def handle_info_will_upgrade_mod(self, payload):
        print('Mod already installed, found new version and will upgrade because it\'s allowed.')

    def handle_info_will_downgrade_mod(self, payload):
        print('Mod already installed, found older version and will downgrade because it\'s allowed.')

    def handle_info_dependencies_detected(self, payload):
        print('Detected dependencies:', payload.deps)

    def handle_info_downloading_file(self, payload):
        print(f'Downloading file {clr.file_name(payload.file.file_name)} from {clr.url(payload.file.download_url)}...')

    def handle_info_all_mod_fetch_complete(self, payload):
        print('Download phase complete. Proceeding to installation...')

    def handle_info_installing_mod(self, payload):
        if payload.new_mod:
            print(f'Installing mod {clr.mod_name(payload.mod.name)} with file {clr.file_name(payload.mod.file.file_name)}...')
        else:
            print(f'Updating mod {clr.mod_name(payload.mod.name)}...')

    def handle_info_updating_file(self, payload):
        if payload.enabled:
            print(f'Installing new file {clr.file_name(payload.file.file_name)}...')
        else:
            print(f'Installing new file {clr.file_name(payload.file.file_name + ".disabled")} because current file was also {clr.file_name(".disabled")}...')

    def handle_info_all_mod_install_complete(self, payload):
        print('Installation phase complete.')

    def handle_match_list(self, payload):
        print(f'No mod found in top downloaded mods matching exactly the key "{clr.mod_key(payload.mod_key)}". These are the top downloaded matches:')
        for mod in payload.mods:
            print(f'[{clr.mod_key(mod.key)}] {clr.mod_name(mod.name)} by {clr.mod_owner(mod.owner)}')
            print(f'\t{clr.mod_blurb(mod.blurb)}')
            if mod.categories:
                print('\t' + ', '.join([f'{clr.mod_category(c)}' for c in mod.categories]))

    def handle_mod_enabled(self, payload):
        print(f'Mod {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} enabled.')

    def handle_mod_disabled(self, payload):
        print(f'Mod {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} disabled.')

    def handle_warn_no_files_in_channel(self, payload):
        print('Mod has no files in the chosen channel. Skipping.')

    def handle_warn_upgrade_not_allowed(self, payload):
        print(f'A newer file was found but upgrades are disabled by default. Use the {clr.cli("--upgrade")} option if this should be allowed.')
        if payload.dependency:
            print(f'\n{clr.emph("NOTE")}: Because this is a dependency, it will {clr.emph("not")} be re-checked if you re-run last install command. Use "{clr.cli("carrot update " + payload.mod.key)}" to do it explicitly.')

    def handle_warn_downgrade_not_allowed(self, payload):
        print(f'An older file was found but downgrades are disabled by default. Use the {clr.cli("--downgrade")} option if this was intended.')

    def handle_warn_already_newest_version(self, payload):
        print('Mod already at newest version for selected channel.')

    def handle_warn_mod_already_enabled(self, payload):
        print(f'Mod {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} is already enabled.')

    def handle_warn_mod_already_disabled(self, payload):
        print(f'Mod {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} is already disabled.')

    def handle_error_no_repo(self, payload):
        print(clr.error(f'Mod repo not initialized. Use "{clr.cli("carrot init")}".'))

    def handle_error_mod_key_not_found(self, payload):
        print(clr.error('Mod key not found:'), clr.mod_key(payload.mod_key))

    def handle_error_no_mod_key_match(self, payload):
        print(f'No matches found, please verify mod key specified or use "{clr.cli("carrot search")}" to find a mod to install.')

    def handle_error_mod_not_installed(self, payload):
        print(f'No mod matching exactly the key "{clr.mod_key(payload.mod_key)}" is currently installed.')

    def handle_error_no_mods_installed(self, payload):
        print(f'No mods are installed. Use "{clr.cli("carrot install")}" to install some.')

    def handle_error_mod_file_missing(self, payload):
        print(f'Mod file for {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} is {clr.error("missing")}.')