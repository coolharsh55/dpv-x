#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Extracts Namespaces from CSV and builds RDFLib objects'''

import csv
from rdflib import Namespace

import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

###################### serializations 
# in the form of extention: rdflib name
RDF_SERIALIZATIONS = {
    'rdf': 'xml', 
    'ttl': 'turtle', 
    'n3': 'n3',
    'jsonld': 'json-ld'
    }


###################### vocab term statuses
VOCAB_TERM_ACCEPT = ('accepted', 'changed', 'modified')
VOCAB_TERM_REJECT = ('deprecated', 'removed')


###################### namespaces
NAMESPACE_CSV = (
	'vocab_csv/Namespaces.csv',
	'vocab_csv/Namespaces_Other.csv',
	)
NAMESPACES = {}
for csvfile in NAMESPACE_CSV:
	DEBUG(f'Extracting namespaces from {csvfile}')
	with open(csvfile, 'r') as fd:
		csvreader = csv.reader(fd)
		next(csvreader)
		for row in csvreader:
			prefix, iri = row[0], row[1]
			variable = prefix.upper().replace('-', '_')
			namespace = Namespace(iri)
			globals()[variable] = namespace
			NAMESPACES[prefix] = namespace
			DEBUG(f'{variable} namespace with IRI {iri}')