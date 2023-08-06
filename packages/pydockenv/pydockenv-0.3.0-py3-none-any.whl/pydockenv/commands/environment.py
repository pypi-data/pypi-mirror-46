import json
import os

import click

import docker
from docker.types import Mount

from pydockenv import definitions
from pydockenv.client import Client


class StateConfig:

    _instance = None

    def __init__(self, envs_conf_path, conf_file_dir):
        self._envs_conf_path = envs_conf_path
        self._conf_file_dir = conf_file_dir
        self._conf = self.get_conf()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(definitions.ENVS_CONF_PATH,
                                definitions.CONF_FILE_DIR)

        return cls._instance

    @classmethod
    def get_current_env(cls):
        return os.environ.get('PYDOCKENV')

    def get_conf(self):
        if not self._envs_conf_path.exists():
            return {}

        with open(str(self._envs_conf_path)) as fin:
            return json.load(fin)

    def get_env_conf(self, env_name):
        return self._conf.get(env_name, {})

    def update_conf(self, conf_update):
        self._conf.update(conf_update)

        os.makedirs(str(self._conf_file_dir), exist_ok=True)
        with open(str(self._envs_conf_path), 'w') as fout:
            return json.dump(self._conf, fout)

    def remove_from_conf(self, key):
        self._conf.pop(key, None)

        os.makedirs(str(self._conf_file_dir), exist_ok=True)
        with open(str(self._envs_conf_path), 'w') as fout:
            return json.dump(self._conf, fout)


def create(name, project_dir, version):
    version = version or 'latest'
    click.echo(f'Creating environment {name} with python version {version}...')
    image_name = f'python:{version}'

    client = Client.get_instance()
    try:
        image = client.images.get(image_name)
    except docker.errors.ImageNotFound:
        click.echo(f'Image {image_name} not found, pulling...')
        image = client.images.pull('python', tag=version)

    create_network(name)
    create_env(image, name, project_dir)

    click.echo(f'Environment {name} with python version {version} created!')


def status():
    current_env = StateConfig.get_current_env()
    if not current_env:
        click.echo('No active environment')
    else:
        click.echo(f'Active environment: {current_env}')


def activate(name):
    click.echo('Activating environment...')
    try:
        container = Client.get_instance().containers.get(
            definitions.CONTAINERS_PREFIX + name)
    except docker.errors.NotFound:
        click.echo(f'Environment {name} not found, exiting...')
    else:
        container.start()
        click.echo('Environment activated!')


def deactivate():
    click.echo('Deactivating current environment...')
    current_env = StateConfig.get_current_env()
    try:
        container = Client.get_instance().containers.get(
            definitions.CONTAINERS_PREFIX + current_env)
    except docker.errors.ImageNotFound:
        click.echo(f'Environment {current_env} not found, exiting...')
    else:
        container.stop()
        click.echo('Environment deactivated!')


def remove(name):
    click.echo(f'Removing environment {name}...')
    try:
        container = Client.get_instance().containers.get(
            definitions.CONTAINERS_PREFIX + name)
    except docker.errors.NotFound:
        click.echo(f'Environment {name} not found, exiting...')
        raise

    kwargs = {
        'force': True,
    }
    container.remove(**kwargs)
    delete_network(name)
    StateConfig.get_instance().remove_from_conf(
        definitions.CONTAINERS_PREFIX + name)
    click.echo(f'Environment {name} removed!')


def list_environments():
    click.echo(f'Listing environments...')
    kwargs = {
        'all': True,
    }
    containers = Client.get_instance().containers.list(kwargs)

    current_env = StateConfig.get_current_env()
    envs = []
    for c in containers:
        if not c.name.startswith(definitions.CONTAINERS_PREFIX):
            continue

        env_name = c.name[len(definitions.CONTAINERS_PREFIX):]
        prefix = '* ' if env_name == current_env else '  '
        envs.append(f'{prefix}{env_name}')

    click.echo('\n'.join(envs))
    click.echo(f'Environments listed!')


def create_network(env_name):
    network_name = definitions.CONTAINERS_PREFIX + env_name + '_network'
    Client.get_instance().networks.create(network_name, check_duplicate=True)


def delete_network(env_name):
    network_name = definitions.CONTAINERS_PREFIX + env_name + '_network'
    try:
        network = Client.get_instance().networks.get(network_name)
    except docker.errors.ImageNotFound:
        click.echo(f'Network {network_name} not found, exiting...')
        raise

    for c in network.containers:
        network.disconnect(c)

    network.remove()


def create_env(image, name, project_dir):
    workdir = os.path.abspath(project_dir)
    mounts = [
        Mount('/usr/src', workdir, type='bind')
    ]
    kwargs = {
        'command': '/bin/sh',
        'stdin_open': True,
        'name': definitions.CONTAINERS_PREFIX + name,
        'mounts': mounts,
        'network': definitions.CONTAINERS_PREFIX + name + '_network',
    }
    Client.get_instance().containers.create(image, **kwargs)

    StateConfig.get_instance().update_conf(
        {definitions.CONTAINERS_PREFIX + name: {'workdir': workdir}})
