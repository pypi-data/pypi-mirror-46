[![Build Status](https://travis-ci.org/kmedian/potpourri.svg?branch=master)](https://travis-ci.org/kmedian/potpourri)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/kmedian/potpourri/master?urlpath=lab)

# potpourri

## Table of Contents
* [Project Requirements](#project-requirements)
* [Folder Structure](#folder-structure)
* [Installation](#installation) 
* [Usage](#usage)
* [Commands](#commands)
* [Support](#support)
* [Contributing](#contributing)


## Project Requirements
* apply different algorithms to a dataset as a batch script
* store *evalutations* (results, run times) in a database


## Folder Structure
* `potpourri` -- different model implementations as python module. Each module contains three objects: 
    * `model` -- a sklearn Pipeline to fit and predict
    * `hyper` -- dictionary with hyperparameters for sklearn's `RandomizedSearchCV`,
    * `meta` --  a python `dict` with further information
* `verto` -- Feature Engineering. Each module contain two objects
    * `trans` -- a sklearn pipeline to transform data
    * `meta` --  a python `dict` with further information
* `seasalt` -- contains different utility, glue, etc. functions and classes
* `nbs` -- notebooks to try, check, profile, etc. each model
* `datasets` -- demo datasets


## Installation
The `potpourri` [git repo](http://github.com/kmedian/potpourri) is available as [PyPi package](https://pypi.org/project/potpourri)

```
pip install potpourri
```


## Usage
Check the [nbs](http://github.com/kmedian/potpourri/nbs) folder for notebooks.


## Commands
* Check syntax: `flake8 --ignore=F401,E251`
* Remove `.pyc` files: `find . -type f -name "*.pyc" | xargs rm`
* Remove `__pycache__` folders: `find . -type d -name "__pycache__" | xargs rm -rf`
* Remove Jupyter checkpoints: `find . -type d -name ".ipynb_checkpoints" | xargs rm -rf`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

Othe helpful commands

* Find package folders: `python -c 'from setuptools import find_packages; print(find_packages())' `

## Support
Please [open an issue](https://github.com/kmedian/potpourri/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/potpourri/compare/).
