### dash-spa

    pip install poetry
    poetry install --no-root

#### Testing

To run the tests (in Docker container):

    pytest

#### Build & Publish

    rm -rf dist && poetry build

    poetry publish

Or upload to local package repository:

    poetry publish -r pypicloud