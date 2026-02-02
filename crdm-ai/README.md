

## data extraction

using [roqet](https://librdf.org/rasqal/roqet.html)

```bash
roqet -q -D AI-taxonomy.ttl query.sparql -r csv > query_results.csv
```

then run `python3 sort.py` to get results in `normalised.csv`