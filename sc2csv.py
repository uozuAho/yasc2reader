import argparse

import tocsv_summary
import tocsv
from yasc2reader import yasc2replay


def main():
    args = get_arg_parser().parse_args()


def get_arg_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='command to run')
    summarise_parser = subparsers.add_parser('summarise', help='summarise one or more replays into a single csv')
    single_parser = subparsers.add_parser('single', help='extract a single replay to csv')
    tocsv_summary.add_args(summarise_parser)
    tocsv.add_args(single_parser)
    return parser


if __name__ == '__main__':
    main()
