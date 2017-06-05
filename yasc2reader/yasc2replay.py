from s2protocol.mpyq import mpyq
from s2protocol import s2protocol as s2p
from s2protocol import protocol15405

import gameevents
import trackerevents
from data import abilities


def load(path):
    return Replay(path)


class Replay:
    def __init__(self, path):
        self.path = path
        self.archive = mpyq.MPQArchive(path)
        self.reader = self._get_replay_reader()
        # Version
        self.version = None
        # str
        self.map_name = None
        # int
        self.replay_length_gameloops = None
        # list of [Player]
        self.players = []
        self._init_data()

    def get_tracker_events(self):
        contents = self.archive.read_file('replay.tracker.events')
        for event in self.reader.decode_replay_tracker_events(contents):
            yield trackerevents.create_tracker_event(event, self.players)

    def get_game_events(self):
        contents = self.archive.read_file('replay.game.events')
        for event in self.reader.decode_replay_game_events(contents):
            yield gameevents.create_game_event(event, self.players)

    def _get_replay_reader(self):
        # Read the protocol header, this can be read with any protocol
        contents = self.archive.header['user_data_header']['content']
        header = protocol15405.decode_replay_header(contents)
        # The header's baseBuild determines which protocol to use
        baseBuild = header['m_version']['m_baseBuild']
        protocol_name = 'protocol%s' % (baseBuild,)
        module = __import__('s2protocol', globals(), locals(), [protocol_name], -1)
        return getattr(module, protocol_name)

    def _init_data(self):
        # ---------------------------------------
        # read header
        # version
        contents = self.archive.header['user_data_header']['content']
        header = self.reader.decode_replay_header(contents)
        self.version = Version(header['m_version'])
        self.replay_length_gameloops = header['m_elapsedGameLoops']
        # ---------------------------------------
        # read details
        # players
        contents = self.archive.read_file('replay.details')
        details = self.reader.decode_replay_details(contents)
        for player in details['m_playerList']:
            self.players += [Player(player)]
        self.map_name = details['m_title']

    def __str__(self):
        return 'Replay version {}, map: {}, players: {}'.format(
            self.version, self.map_name, ','.join(str(p) for p in self.players))


class Player:
    def __init__(self, data):
        self.data = data
        self.name = data['m_name']
        self.race = data['m_race']
        self.won = True if data['m_result'] == 1 else False

    def __str__(self):
        return '{} ({})'.format(self.name, self.race)


class Version:
    def __init__(self, header):
        self.base_build = header['m_baseBuild']
        self.build = header['m_build']
        self.flags = header['m_flags']
        self.major = header['m_major']
        self.minor = header['m_minor']
        self.revision = header['m_revision']

    def __str__(self):
        return '{}.{}.{}.{}'.format(self.major, self.minor, self.revision, self.build)
