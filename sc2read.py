import argparse

from yasc2reader import yasc2replay
from yasc2reader.gameevents import CmdEvent
from yasc2reader.data import abilities


def main():
    executor = CommandExecutor()
    executor.add_command(SummaryCommand(), 'summary', 'print one-line replay summary')
    executor.add_command(ListCommandsCommand(), 'commands', 'print all commands')
    executor.run()


class CommandExecutor:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._subparsers = self._parser.add_subparsers(help='command to run')

    def add_command(self, command, alias, help):
        subparser = self._subparsers.add_parser(alias, help=help)
        command.add_args(subparser)
        subparser.set_defaults(func=command.run)

    def run(self):
        args = self._parser.parse_args()
        args.func(args)


class SummaryCommand:
    def add_args(self, parser):
        parser.add_argument('replay_file', help='.SC2Replay file to load')

    def run(self, args):
        replay = yasc2replay.load(args.replay_file)
        # collect game data
        whoVwho = None
        if len(replay.players) == 2:
            whoVwho = '{}v{}'.format(*[p.race[0] for p in replay.players])
        # assumes one winner:
        winners = [player for player in replay.players if player.won]
        winner = winners[0]
        realtime = GameTime(replay.replay_length_gameloops).to_str(real_time=True)
        gametime = GameTime(replay.replay_length_gameloops).to_str(real_time=False)
        players = ', '.join(str(p) for p in replay.players)
        msg = '{}, {} win, time: {} (real) {} (game), map: {}, players: {}, version: {}'.format(
            whoVwho, winner.race[0], realtime, gametime, replay.map_name, players, replay.version
        )
        print msg


class ListCommandsCommand:
    def add_args(self, parser):
        parser.add_argument('replay_file', help='.SC2Replay file to load')

    def run(self, args):
        replay = yasc2replay.load(args.replay_file)
        abils = abilities.get_abilities(replay.version.build)
        for event in replay.get_game_events():
            if isinstance(event, CmdEvent):
                cmd_str = self.get_cmd_str(event, abils)
                if cmd_str:
                    print cmd_str

    def get_cmd_str(self, cmd, abils):
        if cmd.ability_link is not None:
            time = GameTime(cmd.gameloop).to_str(real_time=True)
            ability_str = self.get_ability_str(cmd, abils)
            if not ability_str:
                ability_str = 'ability {},{}'.format(cmd.ability_link, cmd.ability_index)
            return '{}: {}: {}'.format(time, cmd.player.race[0], ability_str)

    def get_ability_str(self, cmd, abils):
        if cmd.ability_link is None:
            return None

        abil = None
        amSure = True
        try:
            abil = abils.single_or_none(cmd.ability_link, cmd.ability_index)
        except:
            amSure = False
            abil = abils.first_or_none(cmd.ability_link, cmd.ability_index)

        if abil:
            return abil.name + ('' if amSure else ' (probably)')


class GameTime:
    def __init__(self, gameloops):
        self.gameloops = gameloops
        self.gameloops_per_s = 16

    def game_hms(self):
        return self.seconds_to_hms(self.get_game_seconds())

    def real_hms(self, gamespeed=4):
        return self.seconds_to_hms(self.get_real_seconds(gamespeed))

    def get_game_seconds(self):
        return self.gameloops / self.gameloops_per_s

    def get_real_seconds(self, gamespeed):
        # game speed factors found at http://wiki.teamliquid.net/starcraft2/Game_Speed
        factors = {0: 0.599, 1: 0.83, 2: 1, 3: 1.21, 4: 1.38}
        factor = factors[gamespeed]
        return int(self.get_game_seconds() / factor)

    def seconds_to_hms(self, total_seconds):
        hours = total_seconds / 3600
        minutes = (total_seconds % 3600) / 60
        seconds = (total_seconds % 60)
        return hours, minutes, seconds

    def to_str(self, real_time=False):
        h, m, s = self.real_hms() if real_time else self.game_hms()
        return '{}:{:02d}:{:02d}'.format(h, m, s)


if __name__ == '__main__':
    main()
