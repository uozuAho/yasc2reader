"""
    As much as possible, don't couple this to the rest of this library. This script
    should be able to output whatever s2protocol throws at it without issue.
    Additional data such as ability names etc. must all be optional.
"""


import csv
import glob
import multiprocessing as mp
import Queue

import yasc2replay


class ReplaySummariser:
    """Extract summarised replay data into a flattened csv file, for eg. loading into R

    Args:
        - input_pattern (str): filepath pattern to glob input files
    """
    def __init__(self, input_pattern):
        self.input_pattern = input_pattern
        self.replay_paths = self._get_replay_paths()
        try:
            self.num_cpus = mp.cpu_count()
        except:
            self.num_cpus = 4

    def write(self, path):
        if len(self.replay_paths) == 0:
            return
        print 'summarising {} replays'.format(len(self.replay_paths))
        cols, rows = self._get_all_data()
        with open(path, 'wb') as csvfile:
            out = csv.DictWriter(csvfile, cols)
            out.writeheader()
            for row in rows:
                out.writerow(row)

    def _get_all_data(self):
        """ Returns cols, rows """
        paths = mp.Queue()
        rowq = mp.Queue()
        for path in self.replay_paths:
            paths.put(path)
        for i in range(self.num_cpus):
            p = mp.Process(target=self._get_data_worker, args=(paths, rowq))
            p.start()
        cols = set([])
        rows = []
        for i in range(len(self.replay_paths)):
            row = rowq.get()
            cols = cols.union(set(row.keys()))
            rows.append(row)
            print i
        return list(cols), rows

    def _get_data_worker(self, replay_paths, rows):
        """
        Params:
            replay_paths: queue of replay paths
            rows:         queue of {row}
        """
        try:
            while True:
                path = replay_paths.get(timeout=1)
                summary = ReplaySummary(path)
                rows.put(summary.get_row())
        except Queue.Empty:
            pass

    def _get_replay_paths(self):
        return glob.glob(self.input_pattern)


class ReplaySummary:
    def __init__(self, replay_path):
        self.replay_path = replay_path
        self.unit_counter = UnitCounter()
        self.last_event_grabber = LastEventsGrabber()

    def get_row(self):
        replay = yasc2replay.load(self.replay_path)
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
        self._process_tracker_events(replay.get_tracker_events())
        rowdata.update(self._tracker_stats_events_to_row_data(self.last_event_grabber.last_events))
        rowdata.update(self._unit_counts_to_row_data(self.unit_counter.counts))
        return rowdata

    def _process_tracker_events(self, events):
        for event in events:
            self.unit_counter.process_event(event)
            self.last_event_grabber.process_event(event)

    def _get_winner_id(self, replay):
        """ Returns the index of the winning player """
        for i, player in enumerate(replay.players):
            if player.won:
                return i

    def _tracker_stats_events_to_row_data(self, events):
        data = {}
        for tracker_player_id, event in events.items():
            player_id = self._tracker_player_id_to_replay_player_id(tracker_player_id)
            for stat, value in event.data['m_stats'].items():
                data['p{}.{}'.format(player_id, stat)] = value
        return data

    def _unit_counts_to_row_data(self, counts):
        data = {}
        for tracker_player_id, unit_counts in counts.items():
            player_id = self._tracker_player_id_to_replay_player_id(tracker_player_id)
            for unit, count in unit_counts.items():
                data['p{}.totals.{}'.format(player_id, unit)] = count
        return data

    def _tracker_player_id_to_replay_player_id(self, tracker_id):
        return tracker_id - 1


class TrackerEventProcessor(object):
    def process_event(self, event):
        pass

class LastEventsGrabber(TrackerEventProcessor):
    def __init__(self):
        self.last_events = {}

    def process_event(self, event):
        if event.data['_event'] == 'NNet.Replay.Tracker.SPlayerStatsEvent':
            player_id = event.data['m_playerId']
            self.last_events[player_id] = event

class UnitCounter(TrackerEventProcessor):
    def __init__(self):
        self.counts = {}

    def process_event(self, event):
        if event.data['_event'] == 'NNet.Replay.Tracker.SUnitBornEvent':
            # NOTE: player ids start at 1, player 0 creates minerals etc.s
            player_id = event.data['m_controlPlayerId']
            if player_id == 0:
                return
            if player_id not in self.counts:
                self.counts[player_id] = {}
            unit = event.data['m_unitTypeName']
            # Not sure why these don't get counted together...dunno what they are anyway
            if unit.startswith("Beacon"):
                return
            if unit in self.counts[player_id]:
                self.counts[player_id][unit] += 1
            else:
                self.counts[player_id][unit] = 1
