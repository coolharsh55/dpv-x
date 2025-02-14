#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

"""Generate GraphViz diagrams for DPV Concepts"""

import gv

graph = None
node_primary = None

def new_graph(graphlabel):
    """Create an return an empty graph from template"""
    global graph
    graph = gv.digraph(graphlabel)
    gv.setv(graph, 'label', graphlabel)
    gv.setv(graph, 'labelloc', 't')
    gv.setv(graph, 'overlap', 'scale')
    gv.setv(graph, 'splines', 'true')


def render_graph(filepath='graph.png'):
    """Render the graph at filepath"""
    gv.layout(graph, 'neato')
    gv.render(graph, 'png', filepath)


def node_add_main(label):
    """Add the primary/main node"""
    global node_primary
    node_primary = gv.node(graph, label)
    gv.setv(node_primary, 'style', 'filled')
    gv.setv(node_primary, 'color', 'Black')
    gv.setv(node_primary, 'fillcolor', 'Yellow')
    gv.setv(node_primary, 'penwidth', '2')


def node_add_ancestor(parent, ancestor=None):
    """Add ancestors for the primary node"""
    parent = gv.node(graph, parent)
    gv.setv(parent, 'style', 'filled')
    gv.setv(parent, 'color', 'Black')
    gv.setv(parent, 'fillcolor', 'lightskyblue')
    edge = gv.edge(node_primary, parent)
    gv.setv(edge, 'label', 'subclassOf')
    gv.setv(edge, 'arrowhead', 'normal')
    gv.setv(edge, 'color', 'blue')
    gv.setv(edge, 'fontcolor', 'blue')

    if ancestor is None:
        return

    ancestor = gv.node(graph, ancestor)
    gv.setv(ancestor, 'style', 'filled')
    gv.setv(ancestor, 'color', 'Black')
    gv.setv(ancestor, 'fillcolor', 'lightskyblue1')
    edge = gv.edge(parent, ancestor)
    gv.setv(edge, 'style', 'dashed')
    gv.setv(edge, 'label', 'subclassOf')
    gv.setv(edge, 'arrowhead', 'onormal')
    gv.setv(edge, 'color', 'blue')
    gv.setv(edge, 'fontcolor', 'blue')


def node_add_child(child):
    """Add child for the primary node"""
    child = gv.node(graph, child)
    gv.setv(child, 'style', 'filled')
    gv.setv(child, 'color', 'Black')
    gv.setv(child, 'fillcolor', 'cornflowerblue')
    edge = gv.edge(child, node_primary)
    gv.setv(edge, 'label', 'subclassOf')
    gv.setv(edge, 'arrowhead', 'normal')
    gv.setv(edge, 'color', 'blue')
    gv.setv(edge, 'fontcolor', 'blue')


def property_add_domain(property, range, ancestor=True):
    """Add property where primary node is domain"""
    # first check if node already exists in graph
    existing_range = gv.findnode(graph, range)
    if existing_range:
        range = existing_range
    else:
        # range concept does not exist, create it
        range = gv.node(graph, range)
        gv.setv(range, 'style', 'filled')
        gv.setv(range, 'color', 'Black')
        gv.setv(range, 'fillcolor', 'darkseagreen')

    # create edge from primary node to range
    edge = gv.edge(node_primary, range)
    gv.setv(edge, 'label', property)
    gv.setv(edge, 'arrowhead', 'normal')
    gv.setv(edge, 'color', 'darkgreen')
    gv.setv(edge, 'fontcolor', 'darkgreen')
    if ancestor:
        gv.setv(edge, 'style', 'dashed')

def property_add_range(property, domain, ancestor=True):
    """Add property where primary node is range"""
    # first check if node already exists in graph
    existing_domain = gv.findnode(graph, domain)
    if existing_domain:
        domain = existing_domain
    else:
        # domain concept does not exist, create it
        domain = gv.node(graph, domain)
        gv.setv(domain, 'style', 'filled')
        gv.setv(domain, 'color', 'Black')
        gv.setv(domain, 'fillcolor', 'darkseagreen2')

    # create edge from primary node to domain
    edge = gv.edge(domain, node_primary)
    gv.setv(edge, 'label', property)
    gv.setv(edge, 'arrowhead', 'normal')
    gv.setv(edge, 'color', 'darkgreen')
    gv.setv(edge, 'fontcolor', 'darkgreen')
    if ancestor:
        gv.setv(edge, 'style', 'dashed')


def property_suggestion(property, range=None):
    """Add property as a possible suggestion to be used"""
    if range is not None:
        existing_range = gv.findnode(graph, range)
        if existing_range:
            range = existing_range
        else:
            range = gv.node(graph, range)
            gv.setv(range, 'color', 'gray95')
            gv.setv(range, 'style', 'filled')
    else:  # range is None
        existing_range = gv.findnode(graph, 'rdfs:Resource')
        if existing_range:
            range = existing_range
        else:  # add RDFS:Resource
            range = gv.node(graph, 'rdfs:Resource')
            gv.setv(range, 'shape', 'circle')
            gv.setv(range, 'fontcolor', 'firebrick')
            gv.setv(range, 'xlabel', 'rdfs:Resource')
            gv.setv(range, 'label', '')
            gv.setv(range, 'width', '0.25')
            gv.setv(range, 'style', 'filled')
            gv.setv(range, 'fillcolor', 'pink')
    edge = gv.edge(node_primary, range)
    gv.setv(edge, 'label', property)
    gv.setv(edge, 'style', 'dashed')
    gv.setv(edge, 'arrowhead', 'normal')
    gv.setv(edge, 'color', 'brown4')
    gv.setv(edge, 'fontcolor', 'brown4')


if __name__ == "__main__":
    print('running debug tests')
    new_graph('graph')
    node_add_main('main')
    node_add_ancestor('parent', 'ancestor')
    node_add_ancestor('parent2', 'Purpose')
    property_add_domain('hasProcessing', 'Processing')
    property_add_domain('hasPurpose', 'Purpose', ancestor=True)
    property_add_range('hasService', 'ServiceManagement')
    property_add_domain('hasPurpose', 'Service', ancestor=True)
    property_suggestion('hasConsequences')
    render_graph()
