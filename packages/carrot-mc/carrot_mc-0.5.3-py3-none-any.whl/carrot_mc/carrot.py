import os
import json
import hashlib
from argparse import Namespace
from collections import namedtuple
from queue import Queue

from carrot_mc.model import CarrotModel, InstalledModModel, BaseModModel, InstalledModStatusModel
from carrot_mc.meta import VERSION


MODS_FILE_NAME = 'mods.json'


FetchRequest = namedtuple('FetchRequest', ['mod_key', 'mc_version', 'channel', 'dependency'])
DownloadRequest = namedtuple('DownloadRequest', ['mod_info', 'dependency'])
InstallRequest = namedtuple('InstallRequest', ['mod_info', 'dependency'])


class CarrotService:
    def __init__(self, backend_service, installation_manager, printer):
        self.backend = backend_service
        self.installer = installation_manager
        self.printer = printer
    
    def read_carrot(self):
        if os.path.exists(MODS_FILE_NAME):
            with open(MODS_FILE_NAME, 'r') as cf:
                data = json.loads(cf.read())
                carrot = CarrotModel.from_dict(data)
                return carrot

    def save_carrot(self, carrot: CarrotModel):
        carrot.carrot_version = VERSION
        with open(MODS_FILE_NAME, 'w+') as cf:
            data = carrot.to_dict()
            cf.write(json.dumps(data, indent=4))
    
    def initialized(self):
        carrot = self.read_carrot()
        return carrot is not None

    def initialize(self, data: dict):
        config = CarrotModel.from_dict(data)
        d = config.to_dict()

        with open(MODS_FILE_NAME, 'w+') as cf:
            cf.write(json.dumps(d, indent=True))

    def get_status(self):
        carrot = self.read_carrot()

        if not carrot:
            return None

        mod_statuses = []

        for mod in carrot.mods:
            mod_status = InstalledModStatusModel.from_dict(mod.to_dict())

            actual_file_name = None
            if os.path.exists(mod.file.file_name):
                actual_file_name = mod.file.file_name
                mod_status.disabled = False
                mod_status.file_missing = False
            elif os.path.exists(mod.file.file_name + '.disabled'):
                actual_file_name = mod.file.file_name + '.disabled'
                mod_status.disabled = True
                mod_status.file_missing = False
            else:
                mod_status.disabled = True
                mod_status.file_missing = True

            if not mod_status.file_missing:
                file_contents = open(actual_file_name, 'rb').read()

                md5 = hashlib.md5()
                md5.update(file_contents)

                mod_status.actual_file_md5 = md5.hexdigest()

            mod_statuses.append(mod_status)

        carrot.mods = mod_statuses

        return carrot

    def install(self, args):
        carrot = self.read_carrot()
        if not carrot:
            self.printer.handle('error no_repo')
            return

        if args.channel:
            channel = args.channel
        else:
            channel = carrot.channel

        if len(args.mod_key) > 1:
            for mod_key in args.mod_key:
                self.installer.queue_fetch(FetchRequest(
                    mod_key=mod_key,
                    mc_version=carrot.mc_version,
                    channel=channel,
                    dependency=False
                ))

        else:
            mod_key = args.mod_key[0]
            mods = self.backend.search(mod_key=mod_key, mc_version=carrot.mc_version)

            if not mods:
                self.printer.handle('error no_mod_key_match')
                return

            exact_match = find_mod_by_key(mods, mod_key)

            if exact_match:
                self.printer.handle('info', 'Found exact match')

                self.installer.queue_fetch(FetchRequest(
                    mod_key=mod_key,
                    mc_version=carrot.mc_version,
                    channel=channel,
                    dependency=False
                ))

            else:
                self.printer.handle('match list', Namespace(mod_key=mod_key, mods=mods))
                return

        self.installer.run(carrot, args)

        self.save_carrot(carrot)

    def update(self, args):
        carrot = self.read_carrot()
        if not carrot:
            self.printer.handle('error no_repo')
            return

        if args.mod_key:
            local_mod = find_mod_by_key(carrot.mods, args.mod_key)

            if not local_mod:
                self.printer.handle('error mod_not_installed', Namespace(mod_key=args.mod_key))
                return

            if args.channel:
                channel = args.channel
            else:
                channel = local_mod.file.release_type

            self.installer.queue_fetch(FetchRequest(
                mod_key=args.mod_key,
                mc_version=carrot.mc_version,
                channel=channel,
                dependency=local_mod.dependency
            ))

        else:
            if not carrot.mods:
                self.printer.handle('error no_mods_installed')
                return

            for mod in carrot.mods:
                if args.channel:
                    channel = args.channel
                else:
                    channel = mod.file.release_type

                if not mod.dependency:
                    self.installer.queue_fetch(FetchRequest(
                        mod_key=mod.key,
                        mc_version=carrot.mc_version,
                        channel=channel,
                        dependency=False
                    ))
                    # TODO: How to purge dependencies that are no longer valid?

        self.installer.run(carrot, args)
        self.save_carrot(carrot)

    def enable(self, args):
        # TODO: Dependency handling
        carrot = self.read_carrot()
        if not carrot:
            self.printer.handle('error no_repo')
            return

        for mod_key in args.mod_key:
            local_mod = find_mod_by_key(carrot.mods, mod_key)

            if not local_mod:
                self.printer.handle('error mod_not_installed', Namespace(mod_key=mod_key))
                continue

            if not os.path.exists(local_mod.file.file_name + '.disabled'):
                if os.path.exists(local_mod.file.file_name):
                    self.printer.handle('warn mod_already_enabled', Namespace(mod=local_mod))
                    continue

                self.printer.handle('error mod_file_missing', Namespace(mod=local_mod))
                continue

            os.replace(local_mod.file.file_name + '.disabled', local_mod.file.file_name)

            self.printer.handle('mod_enabled', Namespace(mod=local_mod))

    def disable(self, args):
        # TODO: Lots of code sharing with enable()
        carrot = self.read_carrot()
        if not carrot:
            self.printer.handle('error no_repo')
            return

        for mod_key in args.mod_key:
            local_mod = find_mod_by_key(carrot.mods, mod_key)

            if not local_mod:
                self.printer.handle('error mod_not_installed', Namespace(mod_key=mod_key))
                continue

            if not os.path.exists(local_mod.file.file_name):
                if os.path.exists(local_mod.file.file_name + '.disabled'):
                    self.printer.handle('warn mod_already_disabled', Namespace(mod=local_mod))
                    continue

                self.printer.handle('error mod_file_missing', Namespace(mod=local_mod))
                continue

            os.replace(local_mod.file.file_name, local_mod.file.file_name + '.disabled')

            self.printer.handle('mod_disabled', Namespace(mod=local_mod))

    def search(self, args):
        return self.backend.search(**vars(args))


class InstallationManager:
    def __init__(self, backend_service, printer):
        self.backend = backend_service
        self.printer = printer

        self.fetch_q = Queue()
        self.download_q = Queue()
        self.install_q = Queue()

    def queue_fetch(self, request: FetchRequest):
        self.fetch_q.put(item=request)

    def queue_download(self, request: DownloadRequest):
        self.download_q.put(item=request)

    def queue_install(self, request: InstallRequest):
        self.install_q.put(item=request)

    def run(self, carrot: CarrotModel, args):
        while not self.fetch_q.empty():
            req = self.fetch_q.get()
            self.do_fetch(req, carrot, args)

        self.printer.handle('info all_mod_check_complete')

        self._download_hist = set()

        while not self.download_q.empty():
            req = self.download_q.get()
            self.do_download(req, carrot, args)

        self.printer.handle('info all_mod_fetch_complete')

        self._install_hist = set()

        installed_list = []
        while not self.install_q.empty():
            req = self.install_q.get()
            installed_list.append(req.mod_info.key)
            self.do_install(req, carrot, args)

        self.printer.handle('info all_mod_install_complete', { 'installed_list': installed_list })

    def do_fetch(self, req: FetchRequest, carrot: CarrotModel, args):
        mod_info = self.backend.get_mod_info(req.mod_key)

        if not mod_info.key:
            self.printer.handle('error mod_key_not_found', Namespace(mod_key=req.mod_key))
            return

        self.printer.handle('info mod_resolved', Namespace(mod_key=str(req.mod_key), mod=mod_info))

        mod_info.file = self.backend.get_newest_file_info(req.mod_key, req.mc_version, req.channel)

        current_mod = find_mod_by_key(carrot.mods, mod_info.key)

        if not mod_info.file:
            self.printer.handle('warn no_files_in_channel', Namespace(mod=mod_info))

            proceed = False

        elif not current_mod:
            proceed = True

        elif current_mod.file.id < mod_info.file.id:
            if args.upgrade:
                self.printer.handle('info will_upgrade_mod', Namespace(mod=mod_info))

                proceed = True

            else:
                self.printer.handle('warn upgrade_not_allowed', Namespace(mod=mod_info, dependency=req.dependency))

                proceed = False

        elif current_mod.file.id == mod_info.file.id:
            self.printer.handle('warn already_newest_version', Namespace(mod=mod_info))

            proceed = False

        else:
            if args.downgrade:
                self.printer.handle('info will_downgrade_mod', Namespace(mod=mod_info))

                proceed = True
            else:
                self.printer.handle('warn downgrade_not_allowed', Namespace(mod=mod_info))

                proceed = False

        if proceed:
            self.printer.handle('info will_download_mod', Namespace(mod=mod_info))

            self.download_q.put(DownloadRequest(
                mod_info=mod_info,
                dependency=req.dependency
            ))

            self.install_q.put(InstallRequest(
                mod_info=mod_info,
                dependency=req.dependency
            ))

            if mod_info.file.mod_dependencies:
                self.printer.handle('info dependencies_detected', Namespace(deps=mod_info.file.mod_dependencies))

                for dep in mod_info.file.mod_dependencies:
                    self.queue_fetch(FetchRequest(
                        mod_key=dep,
                        mc_version=req.mc_version,
                        channel=req.channel,
                        dependency=True
                    ))

    def do_download(self, req: DownloadRequest, carrot: CarrotModel, args):
        if req.mod_info.file.file_name in self._download_hist:
            return

        self.printer.handle('info downloading_file', Namespace(file=req.mod_info.file))

        file_contents = self.backend.download_file(req.mod_info.file.download_url)
        self.put_file_in_cache(file_contents, req.mod_info.file.file_name)
        self._download_hist.add(req.mod_info.file.file_name)

    def do_install(self, req: InstallRequest, carrot: CarrotModel, args):
        if req.mod_info.file.file_name in self._install_hist:
            return

        current_mod = find_mod_by_key(carrot.mods, req.mod_info.key)
        new_mod = InstalledModModel.from_dict(req.mod_info.to_dict())
        new_mod.dependency = req.dependency

        if not current_mod:
            self.printer.handle('info installing_mod', Namespace(mod=req.mod_info, new_mod=True))

            carrot.mods.append(new_mod)

            self.move_file_from_cache_to_content(new_mod.file.file_name)

        else:
            self.printer.handle('info installing_mod', Namespace(mod=req.mod_info, new_mod=False))

            # Prevent a user-installed mod from becoming a dependency
            if not current_mod.dependency and new_mod.dependency:
                new_mod.dependency = False

            replace_mod_by_key(carrot.mods, req.mod_info.key, new_mod)

            enabled = self.delete_file(current_mod.file.file_name)

            self.printer.handle('info updating_file', Namespace(file=current_mod.file, enabled=enabled))

            self.move_file_from_cache_to_content(req.mod_info.file.file_name, enabled)

        self._install_hist.add(req.mod_info.file.file_name)

        self.printer.handle('info mod_install_complete', Namespace(mod=new_mod))

    def put_file_in_cache(self, content: bytes, file_name: str):
        if not os.path.exists('.carrot_cache'):
            os.mkdir('.carrot_cache')

        with open('.carrot_cache/' + file_name, 'wb+') as f:
            f.write(content)

    def delete_file(self, file_name: str):
        if os.path.exists(file_name):
            os.remove(file_name)
            return True
            
        elif os.path.exists(file_name + '.disabled'):
            os.remove(file_name + '.disabled')
            return False
        
        # If file is missing, assume it's meant to be installed and enabled
        return True

    def move_file_from_cache_to_content(self, file_name: str, enabled: bool = True):
        target_file_name = file_name
        if not enabled:
            target_file_name += '.disabled'
        
        os.rename('.carrot_cache/' + file_name, target_file_name)


def find_mod_by_key(mods: list, mod_key: str):
    try:
        return next((m for m in mods if m.key == mod_key))
    except StopIteration:
        return None

def replace_mod_by_key(mods: list, mod_key: str, replacement: BaseModModel):
    for i, mod in enumerate(mods):
        if mod.key == mod_key:
            mods[i] = replacement
            return