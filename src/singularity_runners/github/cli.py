import argparse
from pathlib import Path
from typing import Optional

from . import configure, start


def subparser(parser: argparse.ArgumentParser):
    subparser = parser.add_subparsers(dest='command')

    parser.add_argument(
        '--runner-home',
        type=Path,
        default='/home/github-runner',
        help="""Path used for the runners home directory, leave as the default if
        using the container or, change if you want to test locally outside the
        container (e.g. './test/github-runner/'), by default
        '/home/github-runner'""",
        required=False,
    )

    parser.add_argument(
        '--runner-dir',
        type=Path,
        default='./actions-runner',
        help="""Runner directory inside the runner home, this is where the local
        runner and tools will be stored, by default './actions-runner'""",
        required=False,
    )

    parser.add_argument(
        '--dry-run',
        action="store_true",
        help="Prints the commands that would be ran, without taking any actions",
        required=False,
    )

    configure.subparser(subparser.add_parser('configure'))
    start.subparser(subparser.add_parser('start'))

    return parser

def cli(parser: Optional[argparse.ArgumentParser] = None):
    if parser is None:
        parser = argparse.ArgumentParser()

    parser = subparser(parser)

    args, unknown = parser.parse_known_args()
    #  Second pass to correctly parse args that apply to all methods
    args, unknown = parser.parse_known_args(unknown, args)

    args_dict = vars(args).copy()
    args_dict.pop('command')

    if args.command == 'configure':
        configure.configure(**args_dict, unknown=unknown)
    elif args.command == 'start':
        start.start(**args_dict, unknown=unknown)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    exit(cli())
