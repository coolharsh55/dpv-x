#!/usr/bin/env python3

import csv

import rdflib
from rdflib import Graph, Namespace
from rdflib.compare import graph_diff
from rdflib.namespace import XSD, SKOS
from rdflib import RDF, RDFS, OWL
from rdflib.term import Literal, URIRef, BNode

DCT = Namespace('http://purl.org/dc/terms/')
DPV = Namespace('http://w3id.org/dpv#')
JURIS = Namespace('http://w3id.org/dpv/dpv-juris#')
TIME = Namespace('https://www.w3.org/TR/owl-time/')

g = Graph()
g.load('onto.ttl', format='ttl')
g.namespace_manager.bind('dct', DCT)
g.namespace_manager.bind('dpv', DPV)
g.namespace_manager.bind('juris', JURIS)
g.namespace_manager.bind('time', TIME)
g.namespace_manager.bind('foaf', Namespace('http://xmlns.com/foaf/spec/'))

REGIONS = set()
COUNTRIES = set()

with open('UNSDM49.csv', 'r') as fd:
    data = csv.reader(fd)
    next(data)
    for row in data:
        # 8: country ; 9: M49 ; 10: Alpha2 ; 11: Alpha3
        alpha2 = row[10].strip()
        if alpha2:
            g.add((JURIS[f'{alpha2}'], RDF.type, DPV.Country))
            g.add((JURIS[f'{alpha2}'], JURIS.iso_alpha2, Literal(alpha2, datatype=XSD.string)))
            g.add((JURIS[f'{alpha2}'], JURIS.iso_alpha3, Literal(row[11].strip(), datatype=XSD.string)))
            COUNTRIES.add(alpha2)
        else:
            alpha2 = row[8].strip().replace(' ', '').replace('-', '')
            g.add((JURIS[f'{alpha2}'], RDF.type, DPV.Region))
        g.add((JURIS[f'{alpha2}'], JURIS.un_m49, Literal(row[9].strip(), datatype=XSD.integer)))
        g.add((JURIS[f'{alpha2}'], DCT.title, Literal(row[8], lang='en')))
        # 2: region
        region = row[3].strip().replace(' ', '').replace('-', '')
        if region:
            if region not in REGIONS:
                REGIONS.add(region)
                g.add((JURIS[f"{region}"], RDF.type, DPV.Region))
                g.add((JURIS[f"{region}"], DCT.title, Literal(region, lang='en')))
                g.add((JURIS[f"{region}"], JURIS.un_m49, Literal(row[2].strip(), datatype=XSD.integer)))
            # 4: sub-region
            subregion = row[5].strip().replace(' ', '').replace('-', '')
            if subregion:
                if subregion not in REGIONS:
                    REGIONS.add(subregion)
                    g.add((JURIS[f"{subregion}"], RDF.type, DPV.Region))
                    g.add((JURIS[f"{subregion}"], DCT.title, Literal(subregion, lang='en')))
                    g.add((JURIS[f"{subregion}"], JURIS.un_m49, Literal(row[4].strip(), datatype=XSD.integer)))
                    g.add((JURIS[f"{subregion}"], SKOS.broaderTransitive, JURIS[f'{region}']))
                    g.add((JURIS[f"{region}"], SKOS.narrowerTransitive, JURIS[f'{subregion}']))
                # 6: intermediate region
                intermregion = row[7].strip().replace(' ', '').replace('-', '')
                if intermregion:
                    if intermregion not in REGIONS:
                        REGIONS.add(intermregion)
                        g.add((JURIS[f"{intermregion}"], RDF.type, DPV.Region))
                        g.add((JURIS[f"{intermregion}"], DCT.title, Literal(intermregion, lang='en')))
                        g.add((JURIS[f"{intermregion}"], JURIS.un_m49, Literal(row[6].strip(), datatype=XSD.integer)))
                        g.add((JURIS[f"{intermregion}"], SKOS.broaderTransitive, JURIS[f'{subregion}']))
                        g.add((JURIS[f"{subregion}"], SKOS.narrowerTransitive, JURIS[f'{intermregion}']))
                    g.add((JURIS[f"{alpha2}"], SKOS.broaderTransitive, JURIS[f'{intermregion}']))
                    g.add((JURIS[f"{intermregion}"], SKOS.narrowerTransitive, JURIS[f'{alpha2}']))
                g.add((JURIS[f"{alpha2}"], SKOS.broaderTransitive, JURIS[f'{subregion}']))
                g.add((JURIS[f"{subregion}"], SKOS.narrowerTransitive, JURIS[f'{alpha2}']))
            g.add((JURIS[f"{alpha2}"], SKOS.broaderTransitive, JURIS[f'{region}']))
            g.add((JURIS[f"{region}"], SKOS.narrowerTransitive, JURIS[f'{alpha2}']))

import json
with open('iso.json', 'r') as fd:
    data = [x.values() for x in json.load(fd)]
    for en, fr, alpha2, alpha3, numeric in data:
        g.add((JURIS[f'{alpha2}'], JURIS.iso_numeric, Literal(numeric, datatype=XSD.integer)))
        if alpha2 not in COUNTRIES:
            g.add((JURIS[f'{alpha2}'], RDF.type, DPV.Country))
            g.add((JURIS[f'{alpha2}'], JURIS.iso_alpha2, Literal(alpha2, datatype=XSD.string)))
            g.add((JURIS[f'{alpha2}'], JURIS.iso_alpha3, Literal(alpha3, datatype=XSD.string)))
            g.add((JURIS[f'{alpha2}'], DCT.title, Literal(en, lang='en')))

g.load('eu.ttl', format='ttl')
g.load('de.ttl', format='ttl')
g.load('us.ttl', format='ttl')

g.serialize('juris.ttl', format='ttl')