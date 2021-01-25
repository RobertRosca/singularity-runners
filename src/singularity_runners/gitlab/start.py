import argparse
import os
import shutil
from pathlib import Path
from typing import List


def subparser(parser: argparse.ArgumentParser):
    return parser


def main(
    runner_home: Path,
    runner_config_dir: str = '.gitlab-runner',
    unknown: List = None,
    dry_run: bool = False,
):
    if unknown is None:
        unknown = []

    command = 'gitlab-runner'
    command_args = [
        'gitlab-runner',
        'run',
        '-c',
        str(runner_home / runner_config_dir / 'config.toml'),
    ] + unknown

    if dry_run:
        print(command, " ".join(command_args[1:]))
        return 0

    print("Running: ", command, " ".join(command_args[1:]))

    if shutil.which(command) is None:
        raise FileNotFoundError(
            f"{command} not found, do you have gitlab-runner installed?"
        )

    return os.execvp(command, command_args)
