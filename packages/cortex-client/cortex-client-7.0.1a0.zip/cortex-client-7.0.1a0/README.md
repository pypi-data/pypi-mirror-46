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

When developing, it's a best practice to work in a virtual environment. Create and activate a virtual environment:
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

## Unit Tests

Follow above setup instructions (making sure to be in the virtual environment and having the necessary dependencies)

- `make dev.test` to run test suite

> if you get this cryptic error message: `RuntimeError: Python is not installed as a framework.`
create a file `~/.matplotlib/matplotlibrc` and write inside of it: `backend: TkAgg`

To run an individual file or class method, use pytest. Example tests shown below:

- file: `pytest test/unit/agent_test.py` 
- class method: `pytest test/unit/agent_test.py::TestAgent::test_get_agent`

## Using the New SDK

Suppose you made some changes to the SDK, and you want to try/test the new SDK before committing your changes to dev. We need to use an alpha version of the client.

- get push privileges to the `cortex-client` pypi (via lastpass)
- bump up the version in `setup.py` but making sure to include an alpha tag (e.g. `7.0.1a` if the previous version was `7.0.0`)
- run `make dev.push`

The above changes will push our new SDK docker image to the pypi registry. The above steps are necessary if you wish to run ActionBuilder and commands that require pulling from the private cortex docker registry.

We are going to be testing our new SDK in skill lab. Go to https://docs.cortex-dev.insights.ai/docs/skill-development/pre-skill-development/import-run-notebooks/#load-example-notebooks to get
a working example notebook in skill lab (if you don't have one already). We are going to use `cortex-examples/skill-lab/skills_hello_world.ipynb` as a reference.

In the hello world notebook:
- create and run a new cell with the command `!pip show cortex-client` - this will show our current cortex-client.
Run that command, and you'll see under Location, it currently points to the old SDK. We need to point it to our new sdk. Take note of this.
- create another cell and run the command `!which python` - this will show which python version (and likely virutalenv) you're using.
Take note of this.

Create a terminal tab in skill lab. We need to point the python version in the terminal session to be the same one as the hello world note book. This process will be specific to the user, but possible steps include having to run `conda deactivate` and `conda actviate <python virtual env the hello world notebook is in>`

Now, in the terminal tab you should be in the correct python environment. Next, We need to use our new local sdk. pip install -e `<localdirectory location/cortex-python-lib>`

Finally: if you go back to the hello world notebook, and run `!pip show cortex-client`, you should see the new SDK version and location. You can now test your new, local SDK on skill-lab.




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

