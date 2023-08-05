# PyBOM
Generate a bill of materials and vulnerability information for your python projects.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/pybom.svg)](https://badge.fury.io/py/pybom)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

## About
PyBOM has two functions:
1. Aggregate a python project's license, package, and vulnerability information in one place by leveraging the GitHub [dependency](https://developer.github.com/v4/previews/#access-to-a-repositories-dependency-graph) and [vulnerability](https://developer.github.com/v4/previews/#repository-vulnerability-alerts) APIs and [PyPI JSON API](https://warehouse.readthedocs.io/api-reference/json/).
2. Report image vulnerability information for docker images pushed to a registry. (Currently in development; Google Container Registry will be the first supported.)

## Getting Started
### Installation
```bash
pip install pybom
```

...or add `pybom` to your `requirements.txt` and run `pip install -r requirements.txt`.

### Usage
#### GitHub Personal Access Token
PyBOM uses GitHub's v4 GraphQL API to get dependency and vulnerability information. To use the API, you must have a Personal Access Token (PAT).

To get a PAT:
1. Navigate to the [Personal access tokens](https://github.com/settings/tokens) page in GitHub's Settings (Settings > Developer settings > Personal access tokens)
1. Click **Generate new token**.
1. Add a note explaining what the token is for, and under **Scopes**, select **Repo**.
1. Click **Generate Token**.
1. Copy the token. You won't be able to see it again.

PyBOM reads the token from the `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable. To set this variable for all bash sessions, include the following in your `.bash_profile` (on macOS):
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=<your-token-here>
```
...then `source ~/.bash_profile` in your current session to set the variable.

#### Python BOM
To get a list of components in your Python project hosted in Github:
(Note: You must have the Dependency Graph API turned on for this to work.)
```python
from pybom.repository import get_components

repo_name = "pybom"
repo_owner = "carbonrelay"

components = get_components(repo_name, repo_owner)
type(components)  # <class 'list'>
type(components[0])  # <class 'pybom.application_component.ApplicationComponent'>
```

#### Python Vulnerabilities
To get a list of vulnerabilities in your Python project hosted on Github:
```python
from pybom.repository import get_vulnerabilities

repo_name = "pybom"
repo_owner = "carbonrelay"

vulnerabilities = get_vulnerabilities(repo_name, repo_owner)
type(vulnerabilities)  # <class 'list'>
type(vulnerabilities[0])  # <class 'pybom.vulnerability.Vulnerability'>
```

#### Image Vulnerabilities
Image vulnerability reporting is not yet fully implemented. It will be  finished in a future release.

## Contributing
PyBOM is developed and tested against Python 3.6. I recommend using `pyenv` to manage your python versions and `venv` to manage project dependencies.

After cloning the repository:

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# run tests with coverage report
./coverage.sh
```

To build the project wheels:
```bash
# adapted from https://packaging.python.org/tutorials/packaging-projects/
pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel
```

If you bump a requirement version in `requirements.txt`, freeze the new dependencies to `requirements-freeze.txt`:
```bash
pip freeze > requirements-freeze.txt
```

## License
This project is licensed under the Apache license. See [LICENSE.md](LICENSE.md).
