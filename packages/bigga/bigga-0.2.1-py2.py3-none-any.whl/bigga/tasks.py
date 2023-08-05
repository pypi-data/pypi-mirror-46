import logging
from posixpath import join
from urllib.parse import quote

import requests
from invoke import task

from bigga.bigga import read_bigga
from bigga.contrib.patchwork.packages import packages

SSH_USERS = []  # TODO: move this to .bigga.json
bigga = read_bigga()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def vagrant(c):
    config = {}
    output = c.run('vagrant ssh-config')
    __import__('ipdb').set_trace()
    for line in output.splitlines()[1:]:
        key, value = line.strip().split(' ', 1)
        config[key] = value
    print(config)
    # extra_args = _settings_dict(config)


def _settings_dict(config):
    settings = {}

    user = config['User']
    hostname = config['HostName']
    port = config['Port']

    # Build host string
    host_string = "%s@%s:%s" % (user, hostname, port)

    settings['user'] = user
    settings['hosts'] = [host_string]
    settings['host_string'] = host_string

    # Strip leading and trailing double quotes introduced by vagrant 1.1
    settings['key_filename'] = config['IdentityFile'].strip('"')

    settings['forward_agent'] = (config.get('ForwardAgent', 'no') == 'yes')
    settings['disable_known_hosts'] = True

    return settings


@task
def echo(c, env):  # , app, env):
    for host in bigga.hosts[env]:
        host.run('echo foo')


@task
def sync_auth_keys(c, env):
    # Add multiple public keys to the user's authorized SSH keys from GitHub.
    for host in bigga.hosts[env]:
        authorized_keys_filename = join(host.ssh_dir, 'authorized_keys')
        host.update_index()
        host.run('cat /dev/null > %s' % quote(authorized_keys_filename))
        logger.info('Fetching public keys from GitHub')
        for gh_user in SSH_USERS:
            r = requests.get('https://api.github.com/users/%s/keys' % gh_user)
            for key in r.json():
                host.run('echo %s >> %s' % (
                    quote(key['key']), quote(authorized_keys_filename)))


@task
def setup(c, env):
    for host in bigga.hosts[env]:
        packages(host.run, ["neovim", "python-pip"])
