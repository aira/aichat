#!/usr/bin/env python
""" Docker Compose utilities """
import json
import subprocess
import tempfile


def ecs_from_dc(dc_path):
    """Reads a docker-compose file to return an ECS task definition.

    Args:
      dc_path (str): Path to the docker-compose file.

    Returns:
      str: ecs_task_definition
    """
    with open(dc_path, 'r') as dc_file, tempfile.TemporaryFile('w+t') as tmp:
        subprocess.check_call(
            [
                '/usr/bin/env',
                'docker',
                'run',
                '--rm',
                '-i',
                'micahhausler/container-transform'
            ],
            stdin=dc_file,
            stdout=tmp,
        )
        tmp.seek(0)
        ecs_task_definition = json.load(tmp)
        return ecs_task_definition
