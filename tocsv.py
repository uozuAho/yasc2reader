"""
    Extract replay data into a flattened csv file, for eg. loading into R

    As much as possible, don't couple this to the rest of this library. This script
    should be able to output whatever s2protocol throws at it without issue.
    Additional data such as ability names etc. must all be optional.
"""


import argparse
import csv
from fnmatch import fnmatch
from yasc2reader import yasc2replay


def main():
    args = get_arg_parser().parse_args()
    replay = yasc2replay.load(args.replay_file)
    to_csv(replay, args.output_file, args.exclude_events, args.load_abilities)

def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('replay_file', help='.SC2Replay file to load')
    parser.add_argument('output_file', help='path to write csv data to')
    parser.add_argument('--load-abilities', action='store_true', help='include additional ability information')
    parser.add_argument('--exclude-events', nargs='+', help='event types to exclude from output. Can use fnmatch patterns.')
    return parser

def to_csv(replay, path, exclude_events=[], include_abilities=False):
    rowfact = CsvRowFactory(replay, exclude_events, include_abilities)
    with open(path, 'wb') as csvfile:
        out = csv.DictWriter(csvfile, rowfact.get_fieldnames())
        out.writeheader()
        for row in rowfact.get_all_rows():
            out.writerow(row)

class CsvRowFactory:
    def __init__(self, replay, exclude_events=[], include_abilities=False):
        self.replay = replay
        self.exclude_events = exclude_events
        # todo: decouple this from replay. Just want replay for its version info
        self.abilities = replay.game_data.abilities if include_abilities else None

    def get_fieldnames(self):
        names = set([])
        for row in self.get_all_rows():
            names.update(row.keys())
        return list(names)

    def get_all_rows(self):
        for e in self.replay.get_tracker_events():
            if self._can_output_event(e.data):
                flat = flatten(e.data)
                yield flat
        for e in self.replay.get_game_events():
            if self._can_output_event(e.data):
                if self.abilities is not None:
                    self._add_abilities(e.data)
                flat = flatten(e.data)
                yield flat
    
    def _add_abilities(self, data):
        abil = data.get('m_abil', None)
        if abil is not None:
            link = abil['m_abilLink']
            index = abil['m_abilCmdIndex']
            # first may return a misleading name, but can be helpful
            data['ability_name'] = self.abilities.first(link, index).name

    def _can_output_event(self, event):
        for pattern in self.exclude_events:
            if fnmatch(event['_event'], pattern):
                return False
        return True


def flatten(dict_or_list, parent_key='', separator=':'):
    ret = {}
    if isinstance(dict_or_list, dict):
        for k,v in dict_or_list.items():
            new_key = parent_key + separator + str(k) if parent_key else str(k)
            if isinstance(v, (dict, list)):
                # TODO: error on duplicate key
                ret.update(flatten(v, new_key, separator))
            else:
                ret[new_key] = v
    if isinstance(dict_or_list, list):
        for i,v in enumerate(dict_or_list):
            new_key = parent_key + separator + str(i) if parent_key else str(i)
            if isinstance(v, (dict, list)):
                # TODO: error on duplicate key
                ret.update(flatten(v, new_key, separator))
            else:
                ret[new_key] = v
    return ret


if __name__ == '__main__':
    main()
