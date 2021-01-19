import argparse
from pathlib import Path
from typing import Optional

from . import register, start


def subparser(parser: argparse.ArgumentParser):
    subparser = parser.add_subparsers(dest='command')

    parser.add_argument(
        '--runner-home',
        type=Path,
        default='/home/gitlab-runner',
        help="""Path used for the runners home directory, leave as the default
        if using the container or, change if you want to test locally outside
        the container (e.g. './test/gitlab-runner/'), by default
        `/home/gitlab-runner`""",
        required=False,
    )

    parser.add_argument(
        '--runner-config-dir',
        type=Path,
        default='.gitlab-runner',
        help="""Runner directory inside the runner home, this is where the
        GitLab runner configuration file (`config.toml`) will be stored, by
        default `.gitlab-runner` under the runner home dir""",
        required=False,
    )

    parser.add_argument(
        '--dry-run',
        action="store_true",
        help="Prints the commands that would be ran, without taking any actions",
        required=False,
    )

    register.subparser(subparser.add_parser('register'))
    start.subparser(subparser.add_parser('start'))

    return parser

def main(parser: Optional[argparse.ArgumentParser] = None):
    if parser is None:
        parser = argparse.ArgumentParser()

    args, unknown = parser.parse_known_args()
    #  Second pass to correctly parse args that apply to all methods
    args, unknown = parser.parse_known_args(unknown, args)

    args_dict = vars(args).copy()
    args_dict.pop('command')

    if args.command == 'register':
        register.main(**args_dict, unknown=unknown)
    elif args.command == 'start':
        start.main(**args_dict, unknown=unknown)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    exit(main())
