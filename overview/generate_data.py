#!/usr/bin/env python3

import csv
import json

nodes = {}
iris = {'START': ''}

with open('iris.csv', 'r') as fd:
    reader = csv.reader(fd)
    next(reader)
    for row in reader:
        label, iri = row
        iris[label] = iri

with open('parents.csv', 'r') as fd:
    reader = csv.reader(fd)
    next(reader)
    nodes = {s[0]: [] for s in reader}
    parents = [s for s in nodes]
    nodes['START'] = parents

# print(parents)
with open('children.csv', 'r') as fd:
    reader = csv.reader(fd)
    next(reader)
    for row in reader:
        parent, child = row
        # print(parent, child)
        if parent not in nodes:
            nodes[parent] = []
        if child not in nodes:
            nodes[child] = []
        nodes[parent].append(child)

# for key in nodes:
#     print(key, len(nodes[key]))

export = []

def get_children(key):
    data = {"name": f'<a href="{iris[key]}">{key}</a>'}
    data_family = []
    children = nodes[key]
    print(key, children)
    for child in children:
        data_family.append(get_children(child))
    if data_family:
        data_family = sorted(data_family, key=lambda x:x['name'])
        data["children"] = data_family
    # print(data)
    return data

children = get_children('START')
with open('data.json', 'w') as fd:
    json.dump(children["children"], fd)
