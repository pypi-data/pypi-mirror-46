import json
from pathlib import Path

import docker

client = docker.from_env()
conf_file_dir = Path(str(Path.home()), '.pydockenv')
status_file_path = Path(str(conf_file_dir), 'status.json')


class StatusHandler:

    def get_current_status(cls):
        if not status_file_path.exists():
            return {}

        with open(str(status_file_path)) as fin:
            return json.load(fin)

    def get_current_env(cls):
        pass
