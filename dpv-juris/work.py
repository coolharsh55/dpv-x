#!/usr/bin/env python3


from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

graph = Graph()
graph.load('./juris.ttl', format='turtle')

# query = """
# PREFIX dpv: <http://www.w3.org/ns/dpv#>
# PREFIX juris: <https://w3id.org/dpv/juris#> 
#         CONSTRUCT {
#           ?dpa dpv:hasJurisdiction ?area .
#         }
#         WHERE {
#           ?area dpv:hasAuthority ?dpa .
#         }
# """
# q_prepared = prepareQuery(query)
# results = graph.query(q_prepared)

# for item in results:
#     graph.add(item)

graph.serialize('./juris.ttl', format='turtle')
graph.serialize('./juris.rdf', format='xml')
graph.serialize('./juris.n3', format='n3')
graph.serialize('./juris.json-ld', format='json-ld')
