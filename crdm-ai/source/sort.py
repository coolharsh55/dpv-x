import csv
from collections import namedtuple

with open('query_results.csv') as fd:
    reader = csv.reader(fd)
    Row = namedtuple('Row', next(reader))
    data = {}
    for row in map(Row._make, reader):
        data[row.label.strip()] = Row(
            row.concept.strip(),
            row.label.strip(),
            row.parent.strip())

with open('list1.txt') as fd:
    concepts = [line.strip() for line in fd.readlines()]

with open('../normalised.csv', 'w') as fd:
    writer = csv.writer(fd)
    for concept in concepts:
        try:
            assert concept in data
        except AssertionError as e:
            print(concept)
            raise e
        writer.writerow(data[concept])
    
