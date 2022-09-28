#!/bin/bash
python3 -m pip install --upgrade setuptools wheel           # upgrade setuptools and wheel
python3 setup.py sdist bdist_wheel                          # build source and wheel distributions
python3 -m pip install --upgrade twine                      # upgrade twine
python3 -m twine upload dist/* --repository toolkit4life    # upload distributions to PyPI