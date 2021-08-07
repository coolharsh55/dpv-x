#!/usr/bin/env python3
#author: Harshvardhan J. Pandit 

'''Generates ReSpec documentation for DPV using RDF and SPARQL'''

# The vocabularies are modular

IMPORT_DPV_PATH = '../dpv/dpv.ttl'
IMPORT_DPV_MODULES_PATH = '../dpv/rdf'
EXPORT_DPV_HTML_PATH = '../dpv'
IMPORT_DPV_GDPR_PATH = '../dpv-gdpr/dpv-gdpr.ttl'
IMPORT_DPV_GDPR_MODULES_PATH = '../dpv-gdpr/rdf'
EXPORT_DPV_GDPR_HTML_PATH = '../dpv-gdpr'

from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL
from rdflib import URIRef
from rdform import DataGraph, RDFS_Resource
import graphviz_diagrams as dia
import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug

TEMPLATE_DATA = {}

ANNOTATIONS = (
    'rdf_type', 'rdfs_type', 'dct_creator', 'rdfs_label', 'rdfs_comment',
    'dct_created', 'dct_description', 'rdfs_subClassOf', 'rdfs_isDefinedBy',
    'rdfs_seeAlso')

G = DataGraph()

with open('./jinja2_resources/links_label.json', 'r') as fd:
    import json
    LINKS_LABELS = json.load(fd)
with open('property_assertions.json', 'r') as fd:
    PROPERTY_ASSERTIONS = json.load(fd)


def load_data(label, filepath):
    DEBUG(f'loading data for {label}')
    g = Graph()
    g.load(filepath, format='turtle')
    G = DataGraph()
    G.load(g)
    G.graph.ns = { k:v for k,v in G.graph.namespaces() }
    TEMPLATE_DATA[f'{label}_classes'] = G.get_instances_of('rdfs_Class')
    TEMPLATE_DATA[f'{label}_properties'] = G.get_instances_of('rdf_Property')


def prefix_this(item):
    # DEBUG(f'item: {item} type: {type(item)}')
    if type(item) is RDFS_Resource:
        item = item.iri
    elif type(item) is URIRef:
        item = str(item)
    if type(item) is str and item.startswith('http'):
        iri = URIRef(item).n3(G.graph.namespace_manager)
    else:
        iri = item
    if iri.count('_') > 0:
        iri = iri.split('_', 1)[1]
    # DEBUG(f'prefixed {item} to: {iri}')
    return iri


def fragment_this(item):
    if '#' not in item:
        return item
    return item.split('#')[-1]


def get_subclasses(item):
    return G.subclasses(item)


def get_properties(item):
    properties = G.properties(item)
    if properties is not None:
        domains, ranges = properties[0], properties[1]
    return domains, ranges


def get_suggested_properties(label):
    domains = PROPERTY_ASSERTIONS['nontransient']['domains'].get(label, [])
    domains_obj = []
    for domain in domains:
        entity = G.get_entity(f'dpv_{domain}')
        if entity is not None:
            domains_obj.append(entity)
    ranges = PROPERTY_ASSERTIONS['nontransient']['ranges'].get(label, [])
    ranges_obj = []
    for range in ranges:
        entity = G.get_entity(f'dpv_{range}')
        if entity is not None:
            ranges_obj.append(entity)
    return domains_obj, ranges_obj


def make_diagram(item):
    """create a diagrammatic representation of concept overview
    for embedding in HTML as SVG image"""
    label = fragment_this(item.iri)
    dia.new_graph(label)
    dia.node_add_main(label)
    DEBUG(item)
    for child in get_subclasses(item):
        dia.node_add_child(str(child))
    # FIXME: add properties if directly specified on the object
    # for k, v in item.metadata.items():
    #     if k in ANNOTATIONS:
    #         continue
    #     DEBUG(f'k:{k} ;; v:{v}')
    #     if type(v) is list:
    #         for vx in v:
    #             if type(vx) is not str:
    #                 vx = prefix_this(vx)
    #             dia.property_add_domain(k, vx)

    properties = get_properties(item)
    if properties is not None:
        domains, ranges = properties[0], properties[1]
        for domain in domains:
            if str(domain) in ANNOTATIONS:
                continue
            if 'rdfs_range' not in domain.metadata:
                range = 'rdfs_Resource'
            else:
                range = fragment_this(domain.rdfs_range.iri)
            dia.property_add_domain(prefix_this(domain.iri), range)
        for range in ranges:
            if str(range) in ANNOTATIONS:
                continue
            if 'rdfs_domain' not in range.metadata:
                domain = 'rdfs_Resource'
            else:
                domain = fragment_this(range.rdfs_domain.iri)
            dia.property_add_range(prefix_this(range.iri), domain)
    domains, ranges = get_suggested_properties(label)
    for domain in domains:
            if 'rdfs_range' not in domain.metadata:
                range = 'rdfs_Resource'
            else:
                range = fragment_this(domain.rdfs_range.iri)
            dia.property_suggestion(prefix_this(domain.iri), range)
    for range in ranges:
            if 'rdfs_domain' not in range.metadata:
                domain = 'rdfs_Resource'
            else:
                domain = fragment_this(range.rdfs_domain.iri)
            dia.property_suggestion(prefix_this(range.iri), domain)

    if not hasattr(item, 'rdfs_subClassOf'):
        return dia.render_graph_svg()

    # add immediate parents
    if type(item.rdfs_subClassOf) is list:
        parents = item.rdfs_subClassOf
    else:
        parents = [item.rdfs_subClassOf]
    for parent in parents:
        # parent_label = '_'.join(str(parent).split(' '))
        dia.node_add_ancestor(fragment_this(parent.iri))
        # get top-most ancestors from parents
        if not hasattr(parent, 'rdfs_subClassOf'):
            continue
        ancestors = set()
        ancestors.add(parent)
        ancestors_top = set()
        while(ancestors):
            ancestor = ancestors.pop()
            if hasattr(ancestor, 'rdfs_subClassOf'):
                # ancestor has ancestors
                if type(ancestor.rdfs_subClassOf) is list:
                    ancestors.update(ancestor.rdfs_subClassOf)
                else:
                    ancestors.add(ancestor.rdfs_subClassOf)
            else:
                # no more ancestors, we're at the top
                if ancestor not in ancestors_top:
                    # DEBUG(f'parent {parent} ;; ancestor {ancestor}')
                    dia.node_add_ancestor(
                        fragment_this(parent.iri), 
                        fragment_this(ancestor.iri))
                    ancestors_top.add(ancestor)
    return dia.render_graph_svg()


def saved_label(item):
    if type(item) is RDFS_Resource:
        item = item.iri
    if not type(item) is str:
        item = str(item)
    if item in LINKS_LABELS:
        return LINKS_LABELS[item]
    return item


# JINJA2 for templating and generating HTML
from jinja2 import FileSystemLoader, Environment
JINJA2_FILTERS = {
    'fragment_this': fragment_this,
    'prefix_this': prefix_this,
    'subclasses': get_subclasses,
    'saved_label': saved_label,
    'make_diagram': make_diagram,
}

template_loader = FileSystemLoader(searchpath='./jinja2_resources')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)
template_env.filters.update(JINJA2_FILTERS)


# LOAD DATA
load_data('core', f'{IMPORT_DPV_MODULES_PATH}/base.ttl')
load_data('personaldata', f'{IMPORT_DPV_MODULES_PATH}/personal_data_categories.ttl')
load_data('purpose', f'{IMPORT_DPV_MODULES_PATH}/purposes.ttl')
load_data('processing', f'{IMPORT_DPV_MODULES_PATH}/processing.ttl')
load_data('technical_organisational_measures', f'{IMPORT_DPV_MODULES_PATH}/technical_organisational_measures.ttl')
load_data('entities', f'{IMPORT_DPV_MODULES_PATH}/entities.ttl')
load_data('consent', f'{IMPORT_DPV_MODULES_PATH}/consent.ttl')
g = Graph()
g.load(f'{IMPORT_DPV_PATH}', format='turtle')
G.load(g)

# DPV: generate HTML

template = template_env.get_template('template_dpv.jinja2')
with open(f'{EXPORT_DPV_HTML_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV spec at f{EXPORT_DPV_HTML_PATH}/index.html')
with open(f'{EXPORT_DPV_HTML_PATH}/dpv.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV spec at f{EXPORT_DPV_HTML_PATH}/dpv.html')

# DPV-GDPR: generate HTML

load_data('legal_basis', f'{IMPORT_DPV_GDPR_MODULES_PATH}/legal_basis.ttl')
load_data('rights', f'{IMPORT_DPV_GDPR_MODULES_PATH}/rights.ttl')
g = Graph()
g.load(f'{IMPORT_DPV_GDPR_PATH}', format='turtle')
G.load(g)

template = template_env.get_template('template_dpv_gdpr.jinja2')
with open(f'{EXPORT_DPV_GDPR_HTML_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV-GDPR spec at f{EXPORT_DPV_GDPR_HTML_PATH}/index.html')
with open(f'{EXPORT_DPV_GDPR_HTML_PATH}/dpv-gdpr.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV-GDPR spec at f{EXPORT_DPV_GDPR_HTML_PATH}/dpv-gdpr.html')

DEBUG('--- END ---')