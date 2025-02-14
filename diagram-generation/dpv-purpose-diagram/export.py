#!/usr/bin/env python3

import csv

# Google Export link
GOOGLE_EXPORT_LINK = (
    'https://docs.google.com/spreadsheets/d/'
    '%s/gviz/tq?tqx=out:csv&sheet=%s')

# The document *must* be publicly viewable (minimum permissions)
# The document ID is found within the URL
# working copy
# DPV_DOCUMENT_ID = '1ppLJDWCIyU4VhaqerQpVaNv2uKmr742O3YVy-NE3Gk8'
# primary / main 
DPV_DOCUMENT_ID = '11bjy424zwC_j4bj9pnhmmI8o7RgrJfX4NgsZ31iR3Wo'

DPV_SHEETS = (
    ## DPV
    # 'BaseOntology',
    # 'PersonalDataCategory',
    # 'Purpose',
    # 'Processing',
    'TechnicalOrganisationalMeasure',
    # 'Entities',
    # 'Consent',
    ## DPV-GDPR
    # 'GDPR_LegalBasis',
    # 'GDPR_LegalRights',
    )

from urllib import request


def download_csv(document_id, sheet_name, save_path='./'):
    '''Download the sheet and save to given path'''
    url = GOOGLE_EXPORT_LINK % (document_id, sheet_name)
    print(f'Downloading {sheet_name}...', end='')
    request.urlretrieve(url, f'{save_path}/{sheet_name}.csv')
    print('DONE')


from collections import namedtuple
DPV_Class = namedtuple('DPV_Class', [
    'term', 'rdfs_label', 'dct_description', 'rdfs_subclassof', 
    'rdfs_seealso', 'relation', 'rdfs_comment', 'rdfs_isdefinedby', 
    'dct_created', 'dct_modified', 'sw_termstatus', 'dct_creator', 
    'resolution'])

import csv 


def extract_terms_from_csv(filepath, Class):
    '''extracts data from file.csv and creates instances of Class
    returns list of Class instances'''
    # this is a hack to get parseable number of fields from CSV
    # it relies on the internal data structure of a namedtuple
    attributes = Class.__dict__
    attributes = len(attributes['_fields'])
    with open(filepath) as fd:
        csvreader = csv.reader(fd)
        next(csvreader)
        terms = []
        for row in csvreader:
            # skip empty rows
            if not row[0].strip():
                continue
            # extract required amount of terms, ignore any field after that
            row = [term.strip() for term in row[:attributes]]
            # create instance of required class
            terms.append(Class(*row))

    return terms


def generate_diagram(concepts):
    dot = []
    terms = {}
    for node, parent, status in concepts:
            if not node:
                node = "Thing"
            if not parent:
                parent = "Thing"
            node = node.replace("dpv:", "")
            parent = parent.replace("dpv:", "")
            parents = parent.split(',')
            for parent in parents:
                dot.append(f'"{parent}" -> "{node}" ;\n')
            if status == "accepted":
                color = "aquamarine"
            elif status == "proposed":
                color = "lightblue"
            elif status == "changed":
                color = "gold"
            else:
                color = "gray"
            if node not in terms:
                terms[node] = f'{node} [color={color}, style=filled] ;\n'
    with open('graph.dot', 'w') as fd:
        fd.write('digraph G { rankdir = LR ;')
        for node in terms.values():
            fd.write(node)
        for line in dot:
            fd.write(line)
        fd.write('}')


if __name__ == '__main__':
    import sys
    for param in sys.argv:
        if 'download' in param:
            print('downloading CSV file')
            for sheet in DPV_SHEETS:
                download_csv(DPV_DOCUMENT_ID, sheet)

    terms = []
    for sheet in DPV_SHEETS:
        terms += extract_terms_from_csv(f'{sheet}.csv', DPV_Class)
    generate_diagram((n.term, n.rdfs_subclassof, n.sw_termstatus) for n in terms)
    print(terms)