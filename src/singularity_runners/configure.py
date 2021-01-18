import argparse
import os
import platform
import tarfile
import urllib.request
from pathlib import Path
from typing import List


def subparser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--runner-version',
        default='2.275.1',
        help="""Version of the runner to use, check
        https://github.com/actions/runner/releases to find the latest version""",
        required=False,
    )

    parser.add_argument(
        '--runner-arch',
        default='x64',
        help="Architecture target of the runner to download",
        required=False,
    )

    parser.add_argument(
        '--url',
        help="""URL for the repository the runner will be used for, `url` and
        `token` values can be found on GitHub when setting up your own runner:
        Settings -> Actions -> Self-hosted runners -> Add runner""",
        required=True,
    )

    parser.add_argument(
        '--token',
        help="""Token for the repository the runner will be used for, `url` and
        `token` values can be found on GitHub when setting up your own runner:
        Settings -> Actions -> Self-hosted runners -> Add runner""",
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
        '--labels',
        default='singularity',
        help="Additional labels to add to the runner, by default 'singularity'",
        required=False,
    )

    return parser


def configure(
    runner_home: Path,
    runner_dir: Path,
    url: str,
    token: str,
    runner_name: str = f"{platform.node()}-singularity",
    runner_version: str = '2.275.1',
    runner_arch: str = 'x64',
    labels: str = "singularity",
    dry_run: bool = False,
    unknown: List = None,
):
    if unknown is None:
        unknown = []

    if not runner_dir.is_absolute():
        runner_dir = runner_home / runner_dir

    runner_package_url = f'https://github.com/actions/runner/releases/download/v{runner_version}/actions-runner-linux-{runner_arch}-{runner_version}.tar.gz'
    runner_package = runner_dir / Path(runner_package_url).name

    if not dry_run:
        runner_dir.mkdir(exist_ok=True)

        if not runner_package.is_file():
            urllib.request.urlretrieve(runner_package_url, runner_package)

        with tarfile.open(runner_package) as f:
            f.extractall(runner_dir)

    script = runner_dir / 'config.sh'
    script_args = [
        'config.sh',
        '--unattended',
        '--url',
        url,
        '--token',
        token,
        '--labels',
        labels,
        '--name',
        runner_name,
    ] + unknown

    if dry_run:
        print(script, " ".join(script_args[1:]))
        return 0

    print("Running: ", script, " ".join(script_args[1:]))

    os.execv(script, script_args)
