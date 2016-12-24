#!/bin/bash
python -m cProfile -s tottime tocsv_summary.py \
"../replays/2016-11-19-gold-1v1-19/*.SC2Replay" "gold-1v1-19.csv" > profile.txt