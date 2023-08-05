from posixpath import join
from typing import Set, Dict
from dataclasses import dataclass
from json import dumps as jdumps, load as jload

from fabric import Connection
from patchwork import files as pw_files

from bigga.contrib.fabtools.user import home_directory
from bigga.contrib.patchwork.packages import update_index

BIGGA_JSON = '.bigga.json'


class DataClassMixin(object):

    def dumps(self, **kwargs) -> str:
        return jdumps(self, default=lambda o: o.__dict__, **kwargs)

    @staticmethod
    def load(data: Dict):
        raise NotImplementedError('Please implement load()')


@dataclass
class Service(DataClassMixin):
    name: str
    framework: str
    args: Dict[str, str]

    @staticmethod
    def load(data: Dict):
        return Service(**data)


@dataclass
class Host(DataClassMixin):
    services: Set[str]
    service_args: Dict[str, str]

    ip: str = ''
    env: str = ''
    user: str = ''
    port: int = 0

    @staticmethod
    def load(data: Dict, env):
        return Host(env=env, **data)

    @property
    def _cxn(self):
        return Connection(self.ip, user=self.user, port=self.port)

    def run(self, *args, **kwargs):
        self._cxn.run(*args, **kwargs)

    @property
    def ssh_dir(self):
        return join(home_directory(self._cxn), '.ssh')

    def ensure_ssh_dir(self):
        return pw_files.directory(self._cxn, self.ssh_dir, mode='700')

    def update_index(self):
        return update_index(self._cxn)


@dataclass
class Bigga(DataClassMixin):
    name: str
    version: str
    language: str
    description: str
    hosts: Dict[str, Set[Host]]
    services: Set[Service]

    @staticmethod
    def load(data: Dict):
        hosts = {}
        for env, _hosts in data["hosts"].items():
            hosts[env] = [Host.load(host, env) for host in _hosts]
        data['hosts'] = hosts
        data['services'] = [
            Service.load(service) for service in data['services']]
        return Bigga(**data)


def read_bigga():
    data = jload(open(BIGGA_JSON))
    return Bigga.load(data)
