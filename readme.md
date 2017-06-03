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

## Raw s2protocol output

Blizzard's s2protocol outputs data in python format. To get all data from a
replay, run

    python yasc2reader/s2protocol/s2protocol.py --gameevents --messageevents \
    --trackerevents --attributeevents --header --details --initdata --stats \
    my_replay.SC2Replay > my_replay.py

## Csv output (single replay)

    python sc2csv.py single my_replay.SC2Replay my_replay.csv

## Csv summary output (1 or more replays, 1 replay per line)

    python sc2csv.py summarise "my/replays/*.SC2Replay" my_replays.csv


Run `python sc2csv.py -h` for more usage info.


# todo
- validate extracted data against scelight analysis
- document how to use stuff in scripts/ It's something like
    + use the sc2 map editor to extact some files somewhere
    + run the scripts, pointing to the extracted files
    + the scripts generate extra data such as unit names, abilities etc.
      that can be used when reading replays
    + I think this is how yasc2reader/data/abilities_47484.csv & units was generated