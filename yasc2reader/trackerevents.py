def create_tracker_event(data, players):
    if data['_event'] == 'NNet.Replay.Tracker.SUnitInitEvent':
        return UnitInitEvent(data, players)
    if data['_event'] == 'NNet.Replay.Tracker.SUnitBornEvent':
        return UnitBornEvent(data, players)
    else:
        return TrackerEvent(data, players)


class TrackerEvent(object):
    def __init__(self, data, players):
        self.data = data
        self.type = data['_event']
        self.gameloop = data['_gameloop']
        self.player = None
        if 'm_controlPlayerId' in data:
            player_id = data['m_controlPlayerId'] - 1
            self.player = players[player_id]

    def __str__(self):
        return '{}: {}: {}'.format(self.gameloop, self.player, self.type)


class UnitInitEvent(TrackerEvent):
    def __init__(self, data, players):
        super(UnitInitEvent, self).__init__(data, players)

    def __str__(self):
        return '{}: {}: unit init: {}'.format(self.gameloop, self.player, self.data['m_unitTypeName'])


class UnitBornEvent(TrackerEvent):
    def __init__(self, data, players):
        super(UnitBornEvent, self).__init__(data, players)

    def __str__(self):
        return '{}: {}: unit born: {}'.format(self.gameloop, self.player, self.data['m_unitTypeName'])
