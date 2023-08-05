# pyeh
A small SDK for EH.

# Usage
Install pyeh package.
```
python3 -m pip install --upgrade pyeh
```

# Release
Build the package and upload to PyPI.
```
python3 setup.py sdist bdist_wheel
python3 -m twine check dist/*
python3 -m twine upload dist/*
```
