import argparse

from yasc2reader import yasc2replay


def main():
    args = get_arg_parser().parse_args()
    args.func(args)


def get_arg_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='command to run')

    summary = SummaryCommand()
    summary_parser = subparsers.add_parser('summary', help='print replay summary')
    summary.add_args(summary_parser)
    summary_parser.set_defaults(func=summary.run)

    return parser


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
        h, m, s = GameTime(replay.replay_length_gameloops).game_hms()
        gametime = '{}:{:02d}:{:02d}'.format(h, m, s)
        players = ', '.join(str(p) for p in replay.players)
        msg = '{}, {} win, game time: {}, map: {}, players: {}, version: {}'.format(
            whoVwho, winner.race[0], gametime, replay.map_name, players, replay.version
        )
        print msg


class GameTime:
    def __init__(self, gameloops):
        self.gameloops = gameloops
        self.gameloops_per_s = 16

    def game_hms(self):
        return self.seconds_to_hms(self.get_game_seconds())

    def real_hms(self, gamespeed=4):
        raise NotImplementedError

    def get_game_seconds(self):
        return self.gameloops / self.gameloops_per_s

    def seconds_to_hms(self, total_seconds):
        hours = total_seconds / 3600 
        minutes = (total_seconds % 3600) / 60
        seconds = (total_seconds % 60)
        return hours, minutes, seconds


if __name__ == '__main__':
    main()
