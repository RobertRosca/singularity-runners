#!/usr/bin/env python3
import argparse
import os
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

args, unknown = parser.parse_known_args()

runner_home = Path(args.runner_home)
runner_dir = Path(args.runner_dir)
if not runner_dir.is_absolute():
    runner_dir = runner_home / runner_dir

script = runner_dir/'run.sh'
script_args =['run.sh'] + unknown

print("Running: ", script, " ".join(script_args[1:]))

if not script.is_file():
    raise FileNotFoundError(
        f"{script} not found, have you configured the runner?"
    )

os.execv(script, script_args)
