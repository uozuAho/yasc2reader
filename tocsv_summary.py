"""
    Extract summarised replay data into a flattened csv file, for eg. loading into R

    As much as possible, don't couple this to the rest of this library. This script
    should be able to output whatever s2protocol throws at it without issue.
    Additional data such as ability names etc. must all be optional.
"""


import argparse
import csv
import glob
from yasc2reader import yasc2replay


def main():
    args = get_arg_parser().parse_args()
    writer = ReplaySummariser(args)
    print 'summarising {} replays'.format(len(writer.replay_paths))
    writer.write(args.output_file)

def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_pattern', help='pattern of replay files to load, eg. mydir/*.SC2Replay')
    parser.add_argument('output_file', help='path to write csv data to')
    return parser


class ReplaySummariser:
    def __init__(self, args):
        self.args = args
        self.replay_paths = self._get_replay_paths()

    def write(self, path):
        if len(self.replay_paths) == 0:
            return
        with open(path, 'wb') as csvfile:
            out = csv.DictWriter(csvfile, self._get_columns())
            out.writeheader()
            i = 1
            for row in self._get_rows():
                print i
                out.writerow(row)
                i += 1

    def _get_columns(self):
        if len(self.replay_paths) > 0:
            summary = ReplaySummary(self.replay_paths[0])
            return summary.get_row().keys()

    def _get_rows(self):
        for path in self.replay_paths:
            summary = ReplaySummary(path)
            yield summary.get_row()

    def _get_replay_paths(self):
        return glob.glob(self.args.input_pattern)


class ReplaySummary:
    def __init__(self, replay_path):
        self.replay_path = replay_path

    def get_row(self):
        replay = yasc2replay.load(self.replay_path, include_game_data=False)
        winner_id = self._get_winner_id(replay)
        rowdata = {
            'p0.name': replay.players[0].name,
            'p0.race': replay.players[0].race,
            'p1.name': replay.players[1].name,
            'p1.race': replay.players[1].race,
            'map': replay.map_name,
            'winner_id': winner_id,
            'winner_name': replay.players[winner_id].name,
            'gameloops': replay.replay_length_gameloops
        }
        last_stat_events = self._get_last_tracker_stats_events(replay)
        rowdata.update(self._tracker_stats_events_to_row_data(last_stat_events))
        return rowdata

    def _get_winner_id(self, replay):
        """ Returns the index of the winning player """
        for i, player in enumerate(replay.players):
            if player.won:
                return i

    def _tracker_stats_events_to_row_data(self, events):
        data = {}
        for player_id, event in events.items():
            for stat, value in event.data['m_stats'].items():
                data['p{}.{}'.format(player_id, stat)] = value
        return data

    def _get_last_tracker_stats_events(self, replay):
        # last tracker stats event per player
        last_events = {}
        for event in replay.get_tracker_events():
            if event.data['_event'] == 'NNet.Replay.Tracker.SPlayerStatsEvent':
                player_id = event.data['m_playerId']
                last_events[player_id] = event
        return last_events


if __name__ == '__main__':
    main()
