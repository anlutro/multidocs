# multidocs

Generate a searchable HTML website with documentation from multiple git repositories containing Markdown files.

## Installing

```
pipsi install multidocs
multidocs -c /path/to/multidocs.yml generate
multidocs -c /path/to/multidocs.yml serve
```

## Developing

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools poetry
poetry develop
multidocs --help
```
