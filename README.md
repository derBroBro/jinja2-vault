# Jinja2 library for loading Vault screts
The idea behind this project is to allow dynamically loading [vault](vaultproject.io) secrets in applications like [cookiecutter](https://github.com/audreyr/cookiecutter). 

## Installation
To install just run ```pip install jinja2-vault```

## Usage 
Add the jinja2 `secret` function like this:

```python
from jinja2 import Environment, Template
env = Environment(
    extensions=['jinja2-vault.VaultExtension']
)

template = env.from_string('password={% secret "password", path="database", mount="app1/secret" %}')
result = template.render()
print(result)

```
This example load key `password` from `app1/secret/database` where `app1/secret` is the mount and `database` the path.

## Setup for cookiecutter
TBB

## Todo
[ ] Add some unit tests

## Build
To build and push the package:
```python setup.py sdist```
```python -m twine upload dist/*```