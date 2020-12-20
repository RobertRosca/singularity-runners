#!/usr/bin/env python3
import argparse
import os
import platform
import tarfile
import urllib.request
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument(
    '--runner-home',
    default='/home/github-runner',
    help="""Path used for the runners home directory, leave as the default if
    using the container or, change if you want to test locally outside the
    container (e.g. './test/github-runner/'), by default
    '/home/github-runner'""",
    required=False,
)

parser.add_argument(
    '--runner-dir',
    default='./actions-runner',
    help="""Runner directory inside the runner home, this is where the local
    runner and tools will be stored, by default './actions-runner'""",
    required=False,
)

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

parser.add_argument(
    '--dry-run',
    action="store_true",
    help="Prints the commands that would be ran, without taking any actions",
    required=False,
)

args, unknown = parser.parse_known_args()

runner_home = Path(args.runner_home)
runner_dir = Path(args.runner_dir)
if not runner_dir.is_absolute():
    runner_dir = runner_home / runner_dir

runner_package_url = f'https://github.com/actions/runner/releases/download/v{args.runner_version}/actions-runner-linux-{args.runner_arch}-{args.runner_version}.tar.gz'
runner_package = runner_dir/Path(runner_package_url).name

url = args.url
token = args.token

if not args.dry_run:
    runner_dir.mkdir(exist_ok=True)

    if not runner_package.is_file():
        urllib.request.urlretrieve(runner_package_url, runner_package)

    with tarfile.open(runner_package) as f:
        f.extractall(runner_dir)

script = runner_dir/'config.sh'
script_args = [
    'config.sh',
    '--unattended',
    '--url', url,
    '--token', token,
    '--labels', args.labels,
    '--name', args.runner_name
] + unknown

print("Running: ", script, " ".join(script_args[1:]))

if args.dry_run:
    exit(0)

os.execv(script, script_args)
