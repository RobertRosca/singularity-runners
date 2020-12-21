import argparse
import os
from pathlib import Path
from typing import List

def subparser(parser: argparse.ArgumentParser):
    return parser

def start(
    runner_home: Path,
    runner_dir: Path,
    unknown: List = None,
    dry_run: bool = False,
):
    if unknown is None:
        unknown = []

    if not runner_dir.is_absolute():
        runner_dir = runner_home / runner_dir

    script = runner_dir/'run.sh'
    script_args =['run.sh'] + unknown

    if dry_run:
        print(script, " ".join(script_args[1:]))
        return 0

    print("Running: ", script, " ".join(script_args[1:]))

    if not script.is_file():
        raise FileNotFoundError(
            f"{script} not found, have you configured the runner?"
        )

    return os.execv(script, script_args)
