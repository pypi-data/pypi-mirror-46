# yoctol-argparse

[![travis][travis-image]][travis-url]
[![pypi][pypi-image]][pypi-url]
![release][release-image]

[travis-image]: https://img.shields.io/travis/Yoctol/yoctol-argparse.svg?style=flat
[travis-url]: https://travis-ci.org/Yoctol/yoctol-argparse
[pypi-image]: https://img.shields.io/pypi/v/yoctol-argparse.svg?style=flat
[pypi-url]: https://pypi.python.org/pypi/yoctol-argparse
[release-image]: https://img.shields.io/github/release/Yoctol/yoctol-argparse.svg

About this project...

## Installation

```bash
pip install yoctol-argparse
```

## Usage

main.py

```python
from yoctol_argparse import YoctolArgumentParser

parser = YoctolArgumentParser()
parser.add_argument('--fruit', choices=['apple', 'banana', 'lemon'])

```

## Test

```bash
make install-dev
make test
```
