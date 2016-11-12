import sys
import get_abilities
import get_units

YASC2_DATA_DIR = '../yasc2reader/data'

sc2data_dir = sys.argv[1]
sc2_build = sys.argv[2]

get_abilities.to_csv(sc2data_dir, YASC2_DATA_DIR + '/abilities_{}.csv'.format(sc2_build))
get_units.to_csv(sc2data_dir, YASC2_DATA_DIR + '/units_{}.csv'.format(sc2_build))
