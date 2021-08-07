#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

"""Generate GraphViz diagrams for DPV Concepts"""

import graphviz as gv
import logging
logging.getLogger("graphviz").setLevel(logging.WARNING)

graph = None
node_primary = None

def new_graph(graphlabel):
    """Create an return an empty graph from template"""
    global graph
    graph = gv.Digraph(graphlabel)
    # graph.attr(label=graphlabel)
    graph.attr(labelloc='t')
    graph.attr(overlap='false')
    graph.attr(splines='true')
    graph.attr(rankdir='LR')
    graph.nodes = []


def export_graph(filepath='graph'):
    """Export the graph at filepath"""
    if len(graph.nodes) < 5:
        graph.attr(layout='dot')
    else:
        graph.attr(layout='neato')
    graph.render(format='png', filename=filepath)


def render_graph_svg():
    """Render the graph in SVG"""
    # print(graph.source)
    return graph.pipe(format='svg').decode('utf-8')


def node_add_main(label):
    """Add the primary/main node"""
    global node_primary
    node_primary = label
    graph.node(label, style='filled', color='Black', fillcolor='Yellow', penwidth='2')
    graph.nodes.append(label)


def node_add_ancestor(parent, ancestor=None):
    """Add ancestors for the primary node"""
    if ancestor is None:
        graph.node(parent, style='filled', color='Black', fillcolor='lightskyblue')
        graph.edge(node_primary, parent, label='subclassOf', arrowhead='normal', color='blue', fontcolor='blue')
        graph.nodes.append(parent)
    else:
        graph.node(ancestor, style='filled', color='Black', fillcolor='lightskyblue1')
        graph.edge(parent, ancestor, style='dashed', label='subclassOf', arrowhead='onormal', color='blue', fontcolor='blue')
        graph.nodes.append(ancestor)


def node_add_child(child):
    """Add child for the primary node"""
    graph.node(child, style='filled', color='Black', fillcolor='cornflowerblue')
    edge = graph.edge(child, node_primary, label='subclassOf', arrowhead='normal', color='blue', fontcolor='blue')
    graph.nodes.append(child)


def property_add_domain(property, range, ancestor=False):
    """Add property where primary node is domain"""
    # add range node if it isn't already in the graph
    if range not in graph.nodes:
        graph.node(range, style='filled', color='Black', fillcolor='darkseagreen')
    # create edge from primary node to range
    graph.edge(
        node_primary, range, 
        label=property, arrowhead='normal', 
        color='darkgreen', fontcolor='darkgreen', 
        style='dashed' if ancestor else 'solid')


def property_add_range(property, domain, ancestor=False):
    """Add property where primary node is range"""
    # first check if node already exists in graph
    if domain not in graph.nodes:
        graph.node(
            domain, style='filled', 
            color='Black', fillcolor='darkseagreen2')
    # create edge from primary node to range
    graph.edge(
        domain, node_primary,
        label=property, arrowhead='normal', 
        color='darkgreen', fontcolor='darkgreen', 
        style='dashed' if ancestor else 'solid')


def property_suggestion(property, range='rdfsResource'):
    """Add property as a possible suggestion to be used"""
    if range not in graph.nodes:
        graph.node(range, color='gray95', style='filled')
        if range == 'rdfsResource':
            graph.node(range, shape='circle', fontcolor='firebrick', xlabel='rdfs:Resource', label='', width='0.25', style='filled', fillcolor='pink', color='black')
    graph.edge(node_primary, range, label=property, style='dashed', arrowhead='normal', color='brown4', fontcolor='brown4')


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
    property_suggestion('hasIntention', 'Purpose')
    # render_graph()
    with open('graph.svg', 'w') as fd:
        fd.write(render_graph_svg())
