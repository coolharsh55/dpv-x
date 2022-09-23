# Generates an Overview Index for DPV

Requires a SPARQL 1.1 query engine (e.g. ARQ from Jena Fuseki used below)

```bash
sparql --data=../dpv/dpv.ttl --query sparql_iris.rq --results=CSV > iris.csv
sparql --data=../dpv/dpv.ttl --query sparql_parents.rq --results=CSV > parents.csv
sparql --data=../dpv/dpv.ttl --query sparql_children.rq --results=CSV > children.csv
python generate_data.py
```

The final output is saved in `data.json`, which must be copied into the index.html script (this can be automated in future).

The `index.html` file uses the `jqTree` library/plugin.