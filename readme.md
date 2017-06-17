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


--------------------------------------------------------------------------------
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


--------------------------------------------------------------------------------
# Extracting game data

Starcraft 2 replay files don't contain unit & ability names. This data can be
extracted by using the Starcraft 2 map editor, and imported for use by
yasc2reader:

- open SC2 map editor
- note the build number from Help -> About Starcraft 2 Editor...
    + Version: Major.Minor.Revision (Build)
- select File -> Export Balance Data
- choose the appropriate expansion, and directory to export to (export dir)
- run

    python scripts/update_data.py <export dir> <build number> yasc2reader/data

This should add the csv files abilities_<build number> and units_<build number>
to yasc2reader/data.


--------------------------------------------------------------------------------
# todo
- validate extracted data against scelight analysis
