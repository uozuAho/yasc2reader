""" sc2csv

    Extract Starcraft 2 replays to csv files.

    usage: python sc2csv.py [command] [args]

    run `python sc2csv.py -h` for more help
"""


import argparse

from tocsv_summary import ReplaySummariser
from tocsv import CsvWriter
from yasc2reader import yasc2replay


def main():
    args = get_arg_parser().parse_args()
    args.func(args)


def get_arg_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='command to run')

    single_reader = SingleReader()
    single_parser = subparsers.add_parser('single', help='extract a single replay to csv')
    single_reader.add_args(single_parser)
    single_parser.set_defaults(func=single_reader.run)

    summariser = Summariser()
    summarise_parser = subparsers.add_parser('summarise', help='summarise one or more replays into a single csv')
    summariser.add_args(summarise_parser)
    summarise_parser.set_defaults(func=summariser.run)
    
    return parser


class SingleReader:
    def add_args(self, parser):
        parser.add_argument('replay_file', help='.SC2Replay file to load')
        parser.add_argument('output_file', help='path to write csv data to')
        parser.add_argument('--load-abilities', action='store_true', 
            help='include additional ability information')
        action = parser.add_mutually_exclusive_group()
        action.add_argument('--include-events', nargs='+',
            help='event types to include in output. Can use fnmatch patterns.',
            default=["NNet.Game.SCmdEvent", 
                    "NNet.Replay.Tracker.SUnitBornEvent",
                    "NNet.Replay.Tracker.SPlayerStatsEvent",
                    "NNet.Replay.Tracker.SUnitDiedEvent"])
        action.add_argument('--exclude-events', nargs='+',
            help='event types to exclude from output. Can use fnmatch patterns.')

    def run(self, args):
        replay = yasc2replay.load(args.replay_file, include_game_data=False)
        writer = CsvWriter(replay, args.load_abilities, args.include_events or [], args.exclude_events or [])
        writer.write(args.output_file)


class Summariser:
    def add_args(self, parser):
        parser.add_argument('input_pattern', help='Pattern of replay files to load, eg. "mydir/*.SC2Replay"')
        parser.add_argument('output_file', help='path to write csv data to')

    def run(self, args):
        writer = ReplaySummariser(args)
        writer.write(args.output_file)


if __name__ == '__main__':
    main()
