#!/usr/bin/env bash

#!/bin/bash

# Ensure at least one argument is provided
if [ "$1" == "-D" ] || [ "$1" == "--download" ]; then
  gh issue list --repo w3c/dpv --state open --limit 200 --json number,title,author,labels > issues.json
fi

./export.py