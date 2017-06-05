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
        self.ability = None
        self.ability_link = None
        self.ability_index = None
        if 'm_abil' in data and data['m_abil'] is not None:
            link = data['m_abil']['m_abilLink']
            index = data['m_abil']['m_abilCmdIndex']
            self.ability_link = link
            self.ability_index = index

    def __str__(self):
        ability_str = self.ability.name if self.ability is not None else 'unknown'
        return "{}: {}: ability ({},{}): {}".format(
            self.gameloop, self.player, self.ability_link, self.ability_index, ability_str)
