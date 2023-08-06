import os
import sys
import argparse

from . import utils
from . import linting


def get_cli_parser():
    parser = argparse.ArgumentParser(description='Copyright linter')

    parser.add_argument(
        '--workdir',
        type=str,
        default=os.getcwd(),
        help='Work directory',
    )

    return parser


def main():
    try:
        cli = get_cli_parser()
        workdir = cli.parse_args().workdir
        config = utils.load_config(workdir)
        linting.lint_project(workdir, config)
    except Exception as e:
        sys.exit(e)


if __name__ == '__main__':
    main()
