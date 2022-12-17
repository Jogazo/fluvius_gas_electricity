# Gas and electricity analysis

Jupyter notebook(s) with scaffolding Python code to analyse Fluvius gas and electricity exports.


## Required system packages:
- `python 3.10 or higher`
- `pip3`

## Create your virtual env relative to project home
`python3 -m venv .venv`

Activate the virtualenv:
`source .venv/bin/activate`

Next, use pip3 to install dependencies in the python venv
`pip3 install -r requirements.txt`

Optionally, if you want to develop:
`pip3 install -r requirements_dev.txt`


## Coding guide lines
All python code should follow the [PEP-8](https://www.python.org/dev/peps/pep-0008/) standard. Therefore please make a symbolic link from `pre-commit.sh` to `.git/hooks/pre-commit` or make sure that this functionallity is in your pre-commit hook.
