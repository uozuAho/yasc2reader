# Yet another Starcraft 2 replay reader

A thin layer on top of Blizzard's s2protocol, aimed at easing data extraction.

Started after trying the following:

- [s2protocol](https://github.com/Blizzard/s2protocol)
    + Too low level to extract meaningful data
- [sc2reader](https://github.com/ggtracker/sc2reader)
    + Doesn't read all events, tests failing, being abandoned?
- [scelight](https://github.com/icza/scelight)
    + Seems to be the most up-to-date, but way too complex for simple data
      extraction

# Usage

## Output replay summaries to csv (1 row per replay)

`python tocsv_summary.py "my/replay/path/*.SC2Replay" replays.csv`

## Output single replay to csv

`python tocsv.py my_replay.SC2Replay my_replay.csv`

Run with -h option to see more usage info.


# todo
- validate extracted data against scelight analysis