import os
dir_path = os.path.dirname(os.path.realpath(__file__))


def main():
    abils = get_abilities(47484)
    print 'yo'


def get_abilities(build_version):
    path = get_abilities_file_path(build_version)
    if path is None:
        raise Exception('abilities file for build version {} not found'.format(build_version))
    else:
        return Abilities(get_abilities_from_file(path))

def get_abilities_file_path(build_version):
    filename = 'abilities_{}.csv'.format(build_version)
    if filename in os.listdir(dir_path):
        return os.path.join(dir_path, filename)

def get_abilities_from_file(path):
    with open(path) as infile:
        for line in infile:
            link, index, name = line.split(',')
            yield Ability(link, index, name)

class Abilities:
    def __init__(self, abilities):
        # dict of dict: {link: {index: [ability]}}
        self.abilities = {}
        for a in abilities:
            if a.link not in self.abilities:
                self.abilities[a.link] = {a.index: [a]}
            else:
                link_bucket = self.abilities[a.link]
                if a.index not in link_bucket:
                    link_bucket[a.index] = [a]
                else:
                    link_bucket[a.index] += [a]

    def get_abilities(self, link, index):
        if link not in self.abilities:
            raise IndexError("no link: " + str(link))
        links = self.abilities[link]
        if index not in links:
            raise IndexError("link {} has no index {}".format(link, index))
        return self.abilities[link][index]

    def single(self, link, index):
        """ Get single ability with link and index.
        
        Exceptions:
            IndexError if link or index don't exist
            Exception if number of abilities with same link & index != 1
        """
        abilities = self.get_abilities(link, index)
        if len(abilities) != 1:
            raise Exception('number of abilities(link: {}, index: {}) != 1'.format(link, index))
        return abilities[0]

    def single_or_none(self, link, index):
        abilities = self.get_abilities(link, index)
        if len(abilities) == 0:
            return None
        if len(abilities) == 1:
            return abilities[0]
        raise Exception('number of abilities(link: {}, index: {}) > 1'.format(link, index))

    def first(self, link, index):
        return self.abilities[link][index][0]

    def first_or_none(self, link, index):
        abilities = self.get_abilities(link, index)
        if len(abilities) == 0:
            return None
        return abilities[0]


class Ability:
    def __init__(self, link, index, name):
        self.link = int(link)
        self.index = int(index) if index != 'None' else 0
        self.name = name.strip()


if __name__ == '__main__':
    main()