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


class CsvWriter:
    def __init__(self, replay, args):
        self.replay = replay
        self.args = args
        # todo: decouple this from replay. Just want replay for its version info
        self.abilities = replay.game_data.abilities if args.load_abilities else None

    def write(self, path):
        with open(path, 'wb') as csvfile:
            out = csv.DictWriter(csvfile, self.get_fieldnames())
            out.writeheader()
            for row in self.get_all_rows():
                out.writerow(row)

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
        if self.args.include_events is not None:
            return self._is_event_included(event)
        else:
            return self._is_event_excluded(event)

    def _is_event_included(self, event):
        if self.args.include_events is None:
            return True
        else:
            for pattern in self.args.include_events:
                if fnmatch(event['_event'], pattern):
                    return True
            return False
        raise Exception("shouldn't get here")

    def _is_event_excluded(self, event):
        if self.args.exclude_events is None:
            return False
        else:
            for pattern in self.args.exclude_events:
                if fnmatch(event['_event'], pattern):
                    return True
            return False
        raise Exception("shouldn't get here")


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
