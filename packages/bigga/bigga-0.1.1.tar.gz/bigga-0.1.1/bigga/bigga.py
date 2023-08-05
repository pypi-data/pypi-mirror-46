from typing import Set, Dict
from json import dumps as jdumps, load as jload
from dataclasses import dataclass


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
    user: str = ''
    port: int = 0

    @staticmethod
    def load(data: Dict):
        return Host(**data)


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
            hosts[env] = [Host.load(host) for host in _hosts]
        data['hosts'] = hosts
        data['services'] = [
            Service.load(service) for service in data['services']]
        return Bigga(**data)


def get_bigga(bigga_file='.bigga.json'):
    data = jload(open(bigga_file))
    return Bigga.load(data)
