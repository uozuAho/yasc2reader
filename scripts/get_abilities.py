import os
import sys
from xml.etree import ElementTree


def main():
    balancedir = sys.argv[1]
    to_csv(balancedir)


def print_abilities(dir):
    for a in sorted(list(get_ability_set(dir)), key=lambda x: (x.ability_number, x.index)):
        print a


def to_csv(data_dir, csv_path):
    with open(csv_path, 'w') as outfile:
        for a in sorted(list(get_ability_set(data_dir)), key=lambda x: (x.ability_number, x.index)):
            outfile.write("{},{},{}\n".format(a.ability_number, a.index, a.name))


def get_ability_set(dir):
    abilities = set([])
    for a in get_abilities(dir):
        if a in abilities:
            # raise Exception('Duplicate ability found: ' + str(a))
            pass
        else:
            abilities.add(a)
    return abilities


class Ability:
    def __init__(self, name, ability_number, index=None):
        self.name = name
        self.ability_number = ability_number
        self.index = index

    def __str__(self):
        return '({}, {}): {}'.format(self.ability_number, self.index, self.name)

    def __eq__(self, other):
        return self.name == other.name and self.ability_number == other.ability_number and self.index == other.index

    def __hash__(self):
        return hash(self.name) + hash(self.ability_number) + hash(self.index)


def get_abilities(dir):
    """ Return all abilities found in the given dir. May contain duplicates. """
    for i in os.listdir(dir):
        if i.endswith(".xml"):
            filename = i.split('.')[0]
            xml = ElementTree.parse(open(os.path.join(dir, i), 'r'))
            for ability in xml.iter('ability'):
                ability_number = int(ability.attrib.get('index', -1))
                name = ability.attrib['id']
                yield Ability(name, ability_number)
            for builds in xml.iter('builds'):
                for unit in builds.iter('unit'):
                    if 'ability' in unit.attrib:
                        ability_number = int(unit.attrib['ability'])
                        name = filename + ' builds ' + unit.attrib['id']
                        index = int(unit.attrib['index'])
                        yield Ability(name, ability_number, index)
            for trains in xml.iter('trains'):
                for unit in trains.iter('unit'):
                    if 'ability' in unit.attrib:
                        ability_number = int(unit.attrib['ability'])
                        name = filename + ' trains ' + unit.attrib['id']
                        index = int(unit.attrib['index'])
                        yield Ability(name, ability_number, index)
            for researches in xml.iter('researches'):
                for upgrade in researches.iter('upgrade'):
                    if 'ability' in upgrade.attrib:
                        ability_number = int(upgrade.attrib['ability'])
                        name = filename + ' researches ' + upgrade.attrib['id']
                        index = int(upgrade.attrib['index'])
                        yield Ability(name, ability_number, index)


if __name__ == '__main__':
    main()
