### dash-spa

    pip install -r requirements.txt

#### Testing

Pytest is used for testing.

To run the tests:

    pytest

#### Publish

    rm -rf dist dash_spa.egg-info build

    python setup.py sdist bdist_wheel

Upload to pypi:

    twine upload -r dist/*

Or upload to local package repository:

    twine upload -r pypicloud dist/*