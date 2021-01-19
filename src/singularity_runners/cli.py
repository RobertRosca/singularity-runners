import argparse

from . import github, gitlab


def subparser(parser: argparse.ArgumentParser):
    subparser = parser.add_subparsers(dest='provider', required=True)

    github.subparser(subparser.add_parser('github'))
    subparser.add_parser('gitlab')

    return parser

def cli():
    parser = subparser(argparse.ArgumentParser(add_help=False))

    args, unknown = parser.parse_known_args()

    if args.command is None:
        parser._actions[0].choices[args.provider].print_help()
        return 0

    #  Second pass to correctly parse args that apply to all methods
    args, unknown = parser.parse_known_args(unknown, args)


if __name__ == "__main__":
    exit(cli())
