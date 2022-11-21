#!/usr/bin/env bash
echo "START"

echo -n "Collecting IRIs..."
sparql --data=../dpv/dpv.ttl --query sparql_iris.rq --results=CSV > iris.csv
echo "DONE"

echo -n "Collecting Parents..."
sparql --data=../dpv/dpv.ttl --query sparql_parents.rq --results=CSV > parents.csv
echo "DONE"

echo -n "Collecting Children..."
sparql --data=../dpv/dpv.ttl --query sparql_children.rq --results=CSV > children.csv
echo "DONE"

echo "Generating data..."
python generate_data.py

