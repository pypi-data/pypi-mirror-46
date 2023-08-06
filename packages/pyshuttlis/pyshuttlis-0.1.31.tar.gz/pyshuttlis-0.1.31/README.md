# Shuttlis

`pyshuttlis` is a collection of utility functions that we use across our
Python apps in Shuttl. It is distributed via [PyPI](https://pypi.org/).

### Running Tests

- pip install cython
- pip install ".[test]"
- pytest

### Releasing

- `make bump_patch_version`
- Update [the Changelog](https://github.com/Shuttl-Tech/pyshuttlis/blob/master/Changelog.md)
- Commit changes to `Changelog`, `setup.py` and `setup.cfg`.
- `make release` (this'll push a tag that will trigger a Drone build)
