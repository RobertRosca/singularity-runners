import argparse
import sys

from . import github, gitlab


def subparser(parser: argparse.ArgumentParser):
    subparser = parser.add_subparsers(dest='provider', required=True)

    github.subparser(subparser.add_parser('github'))
    gitlab.subparser(subparser.add_parser('gitlab'))

    return parser

def main():
    parser = subparser(argparse.ArgumentParser(add_help=False))

    args, _ = parser.parse_known_args()

    selected_parser = parser._actions[0].choices[args.provider]

    if args.command is None:
        selected_parser.print_help()
        return 0

    # Pop the provider off argv, should be dropped beforepassing on to github or
    # gitlab
    sys.argv.pop(1)
    if args.provider == 'github':
        return github.cli.main(selected_parser)
    elif args.provider == 'gitlab':
        return gitlab.cli.main(selected_parser)

if __name__ == "__main__":
    exit(main())
