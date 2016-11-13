import argparse
from yasc2reader import yasc2replay


def main():
    args = get_arg_parser().parse_args()
    replay = yasc2replay.load(args.replay_file)
    print replay
    all_events = list(replay.get_game_events())
    # all_events = list(replay.get_tracker_events()) + list(replay.get_game_events())
    for event in sorted(all_events, key=lambda e: e.gameloop):
        print event

def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('replay_file', help='.SC2Replay file to load')
    return parser


if __name__ == '__main__':
    main()
