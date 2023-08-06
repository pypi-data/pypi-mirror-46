import os
import subprocess
from contextlib import contextmanager
from itertools import chain

import click

import docker

from pydockenv import definitions
from pydockenv.client import Client
from pydockenv.commands.environment import StateConfig


class Executor:

    @classmethod
    def execute(cls, *args, **kwargs):
        client = Client.get_instance()
        current_env = StateConfig.get_current_env()
        try:
            container = client.containers.get(
                definitions.CONTAINERS_PREFIX + current_env)
        except docker.errors.ImageNotFound:
            click.echo(f'Container {current_env} not found, exiting...')
            raise

        # This cannot be done with docker python sdk
        host_base_wd = StateConfig.get_instance().get_env_conf(
            definitions.CONTAINERS_PREFIX + current_env)['workdir']
        current_wd = os.getcwd()
        if not current_wd.startswith(host_base_wd):
            raise RuntimeError(
                f'Cannot run commands outside of {host_base_wd}')

        relative_wd = current_wd[len(host_base_wd):]
        guest_wd = f'/usr/src{relative_wd}'

        env_vars = cls._build_env_vars(kwargs.get('env_vars'))
        with cls._with_mapped_ports(container, kwargs.get('ports')):
            args = (
                ['docker', 'exec', '-w', guest_wd, '-i', '-t'] +
                env_vars +
                [(definitions.CONTAINERS_PREFIX + current_env)] +
                list(args)
            )

            subprocess.check_call(args)

    @classmethod
    def _build_env_vars(cls, env_vars):
        if env_vars:
            return list(chain.from_iterable([
                ['-e', f'{k}={v}']for k, v in env_vars.items()
            ]))

        return []

    @classmethod
    @contextmanager
    def _with_mapped_ports(cls, container, ports):
        if ports:
            port_mappers_containers_names = cls._run_port_mapper(
                container, ports)
        else:
            port_mappers_containers_names = []

        yield

        for container_name in port_mappers_containers_names:
            container = Client.get_instance().containers.get(container_name)
            container.stop()

    @classmethod
    def _run_port_mapper(cls, container, ports):
        network_name = f'{container.name}_network'
        guest_ip = container.attrs['NetworkSettings']['Networks'][
            network_name]['IPAddress']
        containers_names = []
        for port in ports:
            # TODO: Use a single container for all port mappings instead of
            # spinning a container for each port
            name = f'{container.name}_port_mapper_{port}'
            cmd = f'TCP-LISTEN:1234,fork TCP-CONNECT:{guest_ip}:{port}'
            kwargs = {
                'command': cmd,
                'ports': {'1234': f'{port}/tcp'},
                'name': name,
                'detach': True,
                'auto_remove': True,
                'network': network_name,
            }

            Client.get_instance().containers.run('alpine/socat', **kwargs)
            containers_names.append(name)

        return containers_names
