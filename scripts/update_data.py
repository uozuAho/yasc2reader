import sys
import get_abilities
import get_units

sc2data_dir = sys.argv[1]
sc2_build = sys.argv[2]
output_dir = sys.argv[3]

get_abilities.to_csv(sc2data_dir, output_dir + '/abilities_{}.csv'.format(sc2_build))
get_units.to_csv(sc2data_dir, output_dir + '/units_{}.csv'.format(sc2_build))
