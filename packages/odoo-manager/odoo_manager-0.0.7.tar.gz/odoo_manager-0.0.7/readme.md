# odoo-manager

## Setup

### Dependencies

```
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine
python3 -m pip install --user --upgrade pytest
python3 -m pip install --user --upgrade docopt
```

### Install Test Version Locally

`python3 -m pip install -e .[test]`

## Distribution

### Generating Distribution

`python3 setup.py sdist bdist_wheel`

### Uploading Distribution

`python3 -m twine upload dist/odoo_manager-{current_version}.tar.gz`

