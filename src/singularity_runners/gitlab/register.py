import argparse
import os
import platform
from pathlib import Path
from typing import List


def subparser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--url',
        help="""URL for the repository the runner will be used for, `url` and
        `token`, values can be found on GitLab when setting up your own runner:
        Settings -> CI/CD -> Set up a specific Runner manually""",
        required=True,
    )

    parser.add_argument(
        '--registration-token',
        help="""URL for the repository the runner will be used for, `url` and
        `token`, values can be found on GitLab when setting up your own runner:
        Settings -> CI/CD -> Set up a specific Runner manually""",
        required=True,
    )

    parser.add_argument(
        '--runner-name',
        default=f'{platform.node()}-singularity',
        help="""Name for the runner, by default it is the machine name with a
        '-singularity' suffix added to the end""",
        required=False,
    )

    parser.add_argument(
        '--executor',
        default='shell',
        help="""Executor to use with the runner, by default `shell`""",
        required=False,
    )

    parser.add_argument(
        '--tag-list',
        default='singularity',
        help="List of comma separated tags to add to the runner, by default 'singularity'",
        required=False,
    )

    return parser


def main(
    runner_home: Path,
    url: str,
    registration_token: str,
    runner_config_dir: str = '.gitlab-runner',
    runner_name: str = f"{platform.node()}-singularity",
    executor: str = 'shell',
    tag_list: str = "singularity,",
    dry_run: bool = False,
    unknown: List = None,
):
    if unknown is None:
        unknown = []

    command = 'gitlab-runner'
    command_args = [
        'gitlab-runner',
        'register',
        '--non-interactive',
        '-c',
        str(runner_home / runner_config_dir / 'config.toml'),
        '--url',
        url,
        '--registration-token',
        registration_token,
        '--executor',
        executor,
        # '--tag-list',  # For some reason adding a tags breaks the registration
        # tag_list,
        '--name',
        runner_name,
    ] + unknown

    if dry_run:
        print(command, " ".join(command_args[1:]))
        return 0

    print("Running: ", command, " ".join(command_args[1:]))

    os.execv(command, command_args)
