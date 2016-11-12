import os
import sys
from xml.etree import ElementTree


def main():
    balancedir = sys.argv[1]
    csv_path = sys.argv[2]
    to_csv(balancedir, csv_path)


def to_csv(balancedir, csv_path):
    with open(csv_path, 'w') as outfile:
        for i in os.listdir(balancedir):
            if i.endswith(".xml"):
                xml = ElementTree.parse(open(os.path.join(balancedir, i), 'r'))
                outfile.write("{},{}\n".format(xml.findall('meta')[0].attrib['index'], xml.getroot().attrib['id']))


if __name__ == '__main__':
    main()