[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/stp-scraper/badge.svg?branch=master&t=V0q7kh)](https://coveralls.io/github/cuenca-mx/stp-scraper?branch=master)
[![Build Status](https://travis-ci.com/cuenca-mx/stp-scraper.svg?token=MSMdx4sxrH14mMPzx2Cx&branch=master)](https://travis-ci.com/cuenca-mx/stp-scraper)
[![PyPI](https://img.shields.io/pypi/v/stp-scraper.svg)](https://pypi.org/project/stp-scraper/)

# stp-scraper
STP scraper library for obtaining all transactions given a range of dates.

## Requirements
Python 3.7+

## Installation
```bash
pip install stp_scraper
```

## Tests
```bash
make test
```

## Basic usage
Get transactions of prior week
```python
import stp_scraper
stp_scraper.extract(None, None)
```

Get transactions for specific dates
```python
from stp_scraper import extract
extract('01/02/2019', '15/02/2019')
```

## Release to PyPi

```bash
pip install -U setuptools wheel twine
make release
# PyPi will prompt you to log in
```