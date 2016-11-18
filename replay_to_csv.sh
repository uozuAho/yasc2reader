#!/bin/bash
python tocsv.py $1 $1.csv --load-abilities --include-events \
"NNet.Game.SCmdEvent" \
"NNet.Replay.Tracker.SUnitBornEvent" \
"NNet.Replay.Tracker.SPlayerStatsEvent" \
"NNet.Replay.Tracker.SUnitDiedEvent"