# Tools for Assisting with DPV Issue Management

## Uses

- to easily find and copy issue metadata for inclusion in DPVCG minutes

## Files

- `issues.json` is the exported list of issues in JSON (see `gh` export below)
- `issues.html` is the HTML output containing a list of isuses and a copy button to export the issue to IRC format for W3C DPVCG minutes
- `issues.py` is a python script that takes as parameter a number and prints the issue details, or lists all issues 
- `export_html.py` is a python script that takes the input JSON and creates the HTML output

## Retrieve and Update issues

- presuming `gh` is installed
- `gh issue list --state all --json author,id,labels,number,milestone,state,title,url > <path>/issues.json`