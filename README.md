# multidocs

[![Build Status](https://travis-ci.org/anlutro/multidocs.svg?branch=master)](https://travis-ci.org/anlutro/multidocs)
[![Latest version on PyPI](https://img.shields.io/pypi/v/multidocs?maxAge=2592000)](https://pypi.python.org/pypi/multidocs)
[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

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
