#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Generate Jurisdictions RDF from CSV'''

CSV_FILEPATH = './countries.csv'

# serializations in the form of extention: rdflib name
RDF_SERIALIZATIONS = {
    'rdf': 'xml', 
    'ttl': 'turtle', 
    'n3': 'n3',
    'jsonld': 'json-ld'
    }

import csv
from collections import namedtuple

from rdflib import Graph, Namespace
from rdflib.compare import graph_diff
from rdflib.namespace import XSD
from rdflib import RDF, RDFS, OWL
from rdflib.term import Literal, URIRef, BNode

DCT = Namespace('http://purl.org/dc/terms/')
DPV = Namespace('http://www.w3.org/ns/dpv#')
DPV_GDPR = Namespace('http://www.w3.org/ns/dpv-gdpr#')
DPV_JURIS = Namespace('https://w3id.org/dpv/juris#')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
ODRL = Namespace('http://www.w3.org/ns/odrl/2/')
PROV = Namespace('http://www.w3.org/ns/prov#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SPL = Namespace('http://www.specialprivacy.eu/langs/usage-policy#')
SVD = Namespace('http://www.specialprivacy.eu/vocabs/data#')
SVDU = Namespace('http://www.specialprivacy.eu/vocabs/duration#')
SVL = Namespace('http://www.specialprivacy.eu/vocabs/locations#')
SVPR = Namespace('http://www.specialprivacy.eu/vocabs/processing#')
SVPU = Namespace('http://www.specialprivacy.eu/vocabs/purposes#')
SVR = Namespace('http://www.specialprivacy.eu/vocabs/recipients')
SW = Namespace('http://www.w3.org/2003/06/sw-vocab-status/ns#')
TIME = Namespace('http://www.w3.org/2006/time#')

# The dpv namespace is the default base for all terms
# Later, this is changed to write terms under DPV-GDPR namespace
BASE = DPV_JURIS

NAMESPACES = {
    'dct': DCT,
    'dpv': DPV,
    'dpv-gdpr': DPV_GDPR,
    'dpv-juris': DPV_JURIS,
    'foaf': FOAF,
    'odrl': ODRL,
    'owl': OWL,
    'prov': PROV,
    'rdf': RDF,
    'rdfs': RDFS,
    'skos': SKOS,
    'spl': SPL,
    'svd': SVD,
    'svdu': SVDU,
    'svl': SVL,
    'svpr': SVPR,
    'svpu': SVPU,
    'svr': SVR,
    'sw': SW,
    'time': TIME,
    'xsd': XSD,
}

JURISDICTION = namedtuple('JURISDICTION', (
    'IRI', 'Name', 'Type', 'ISO3166_alpha2', 'ISO3166_alpha3', 
    'EUMember', 'DPA', 'website'))

with open(CSV_FILEPATH, 'r') as fd:
    csv_reader = csv.reader(fd)
    next(csv_reader)
    data = [JURISDICTION(*row) for row in csv_reader]

graph = Graph()
for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)

for item in data:
    graph.add((BASE[f'{item.IRI}'], RDF.type, DPV.Country))
    graph.add((
        BASE[f'{item.IRI}'], RDFS.label, 
        Literal(item.Name, datatype=XSD.string)))
    graph.add((
        BASE[f'{item.IRI}'], BASE['iso3166_apha2'], 
        Literal(item.ISO3166_alpha2, datatype=XSD.string)))
    graph.add((
        BASE[f'{item.IRI}'], BASE['iso3166_apha3'], 
        Literal(item.ISO3166_alpha3, datatype=XSD.string)))

    if item.EUMember == 'FALSE': continue
    graph.add((
        BASE[f'{item.IRI}'], BASE.memberOf, BASE.EU))
    graph.add((
        BASE[f'{item.IRI}'], BASE.hasAuthority, 
        BASE[f'{item.ISO3166_alpha2}-DPA']))
    graph.add((
        BASE[f'{item.ISO3166_alpha2}-DPA'], RDF.type, 
        DPV.DataProtectionAuthority))
    graph.add((
        BASE[f'{item.ISO3166_alpha2}-DPA'], RDFS.label, 
        Literal(item.DPA, datatype=XSD.string)))
    graph.add((
        BASE[f'{item.ISO3166_alpha2}-DPA'], RDFS.seeAlso, 
        Literal(item.website, datatype=XSD.anyURI)))


for ext, format in RDF_SERIALIZATIONS.items():
    graph.serialize(f'juris.{ext}', format=format)