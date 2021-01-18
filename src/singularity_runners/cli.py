import argparse
from typing import Optional

from . import github, gitlab


def subparser(parser: argparse.ArgumentParser):
    subparser = parser.add_subparsers(dest='command')

    github.subparser(subparser.add_parser('github'))
    # gitlab.subparser(subparser.add_parser('gitlab'))

    return parser

def cli():
    parser = subparser(argparse.ArgumentParser(add_help=False))

    print(parser.__dir__())

    args, unknown = parser.parse_known_args()
    print(f"{args=}, {unknown=}")
    #  Second pass to correctly parse args that apply to all methods
    args, unknown = parser.parse_known_args(unknown, args)
    print(f"{args=}, {unknown=}")

    args_dict = vars(args).copy()
    args_dict.pop('command')

    print(args.command)

    parser.print_help()
    print(parser)
    return 0


if __name__ == "__main__":
    exit(cli())
