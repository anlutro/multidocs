# docgen

Generate a searchable HTML website with documentation from multiple git repositories containing Markdown files.

## Installing

```
pipsi install docgen
docgen -c /path/to/docgen.yml generate
docgen -c /path/to/docgen.yml serve
```

## Developing

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools poetry
poetry develop
docgen --help
```
