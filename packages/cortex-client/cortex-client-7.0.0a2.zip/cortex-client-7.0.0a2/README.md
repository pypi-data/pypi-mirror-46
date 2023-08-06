# Cortex ML Models Python Library

The Cortex Python Library provides an SDK to easily integrate and deploy ML algorithms into Cortex. 
Refer to the Cortex documentation for details on how to use the SDK: 

- Developer guide: https://docs.cortex.insights.ai/docs/developer-guide/overview/
- Python SDK references: https://docs.cortex.insights.ai/docs/developer-guide/reference-guides


## Installation

To install the Cortex Client: 
```
  > pip install cortex-client
```

or from source code:
```
  > git clone git@bitbucket.org:cognitivescale/cortex-python-lib.git
  > cd cortex-python-lib
  > pip install -e .
```

## Development 

### Setup

Create and activate a virtual environment:
```
  > virtualenv --python=python3.6 _venv
  > source _venv/bin/activate
```

Install Python SDK in editable mode, and all developer dependencies:

```
  > git clone git@bitbucket.org:cognitivescale/cortex-python-lib.git
  > cd cortex-python-lib
  > make dev.setup
  > make dev.install
```

There's a convenience `Makefile` that has commands to common tasks, such as build, test, etc. Use it!

### Testing

Follow above setup instructions

- `make dev.test` to run test suite

> if you get this cryptic error message: `RuntimeError: Python is not installed as a framework.`
create a file `~/.matplotlib/matplotlibrc` and write inside of it: `backend: TkAgg`

To run an individual file or class method, use pytest. Example tests shown below:

- file: `pytest test/unit/agent_test.py` 
- class method: `pytest test/unit/agent_test.py::test_get_agent`

### Documentation

The Python client documentation is built with Sphinx. To build the documentation:

`cd` to the root directory of the Python SDK project:
```
  > cd <cortex-python-sdk source dir>
```

Activate your virtual environment:
```
> source _venv/bin/activate
```

Setup your environment, if you have not done so:
```
> make dev.install 
```

Build the docs:
```
> make docs.build
```

The documentation will be rendered in HTML format under the `docs/_build/html` directory.

### Pre-release to staging

1. Merge `develop` to `staging` branch:
```
> make stage
```
2. Create a pull request from `staging` to `master`.

