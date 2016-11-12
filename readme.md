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