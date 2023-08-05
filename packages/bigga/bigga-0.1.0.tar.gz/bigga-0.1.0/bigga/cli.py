from invoke import Collection, Program
from invoke.config import Config, merge_dicts

from bigga import tasks

__VERSION__ = '0.1.0'


class TesterConfig(Config):

    prefix = 'rscli'

    @staticmethod
    def global_defaults():
        their_defaults = Config.global_defaults()
        my_defaults = {
            'run': {
                'echo': True,
            },
        }
        return merge_dicts(their_defaults, my_defaults)


program = Program(
    version=__VERSION__,
    config_class=TesterConfig,
    namespace=Collection.from_module(tasks)
)
