def create_game_event(data, players):
    if data['_event'] == 'NNet.Game.SCmdEvent':
        return CmdEvent(data, players)
    else:
        return GameEvent(data, players)

class GameEvent(object):
    def __init__(self, data, players):
        self.data = data
        self.type = data['_event']
        self.gameloop = data['_gameloop']
        player_id = data['_userid']['m_userId']
        self.player = players[player_id] if player_id < len(players) else None

    def __str__(self):
        return "{}: {}: {}".format(self.gameloop, self.player, self.type)

class CmdEvent(GameEvent):
    def __init__(self, data, players):
        super(CmdEvent, self).__init__(data, players)
        self.ability_link = None
        self.ability_index = None
        if 'm_abil' in data and data['m_abil'] is not None:
            self.ability_link = data['m_abil']['m_abilLink']
            self.ability_index = data['m_abil']['m_abilCmdIndex']

    def __str__(self):
        return "{}: {}: ability ({},{})".format(
            self.gameloop, self.player, self.ability_link, self.ability_index)