# recursive-yaml [![Build Status](https://travis-ci.com/FebruaryBreeze/recursive-yaml.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/recursive-yaml) [![codecov](https://codecov.io/gh/FebruaryBreeze/recursive-yaml/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/recursive-yaml) [![PyPI version](https://badge.fury.io/py/recursive-yaml.svg)](https://pypi.org/project/recursive-yaml/)

Load YAML Recursively.

## Installation

Need Python 3.6+.

```bash
pip install recursive-yaml
```

## Usage

Python:

```python
import recursive_yaml

recursive_yaml.load(config_path='/path/to/yaml')
```

CLI:

```bash
# output directly
recursive-yaml tests/master.yaml

# or pretty print with yq
recursive-yaml tests/master.yaml | yq r -
```
