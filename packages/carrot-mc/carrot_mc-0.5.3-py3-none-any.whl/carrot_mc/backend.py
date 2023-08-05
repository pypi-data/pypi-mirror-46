import requests

from carrot_mc import meta
from carrot_mc.model import ModModel, ModFileModel

API_ENDPOINT = 'https://api.carrot-mc.xyz/prod/'


class BackendService:
    def metadata(self):
        r = requests.get(
            url=f'{API_ENDPOINT}metadata',
            headers=self._get_default_headers()
        )

        return r.json()['result']

    def search(
            self,
            mc_version: str,
            mod_key: str = None,
            mod_name: str = None,
            owner: str = None,
            page_size: int = 30,
            page_num: int = 1) -> list:
        url = f'{API_ENDPOINT}mods?mc_version={mc_version}&page_size={page_size}&page_num={page_num}'

        if mod_key:
            url += f'&mod_key={mod_key}'

        if mod_name:
            url += f'&mod_name={mod_name}'

        if owner:
            url += f'&owner={owner}'

        r = requests.get(
            url=url,
            headers=self._get_default_headers()
        )

        j = r.json()
        mods = [ModModel.from_dict(m) for m in j['result']]
        return mods

    def get_mod_info(self, mod_key: str) -> ModModel:
        r = requests.get(
            url=f'{API_ENDPOINT}mod/{mod_key}',
            headers=self._get_default_headers()
        )
        mod = ModModel.from_dict(r.json()['result'])
        return mod

    def get_newest_file_info(self, mod_key: str, mc_version: str, channel: str) -> ModFileModel:
        r = requests.get(
            url=f'{API_ENDPOINT}mod/{mod_key}/files?mc_version={mc_version}&channel={channel}&newest_only=1',
            headers=self._get_default_headers()
        )
        result = r.json()['result']
        if result:
            file = ModFileModel.from_dict(result[0])
            return file

    def download_file(self, download_url: str) -> bytes:
        r = requests.get(
            url=download_url,
            headers=self._get_default_headers()
        )
        result = r.content
        return result

    def _get_default_headers(self):
        return {
            'User-Agent': 'Carrot ' + meta.VERSION
        }