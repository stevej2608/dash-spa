import io
import os
import re

from setuptools import find_packages, setup

HERE = os.path.dirname(os.path.abspath(__file__))

DASH_SPA_DIR = 'dash_spa'

def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


def _get_version():
    """ Get version by parsing _version programmatically """
    version_ns = {}
    with open(
            os.path.join(HERE, DASH_SPA_DIR, "_version.py")
    ) as f:
        exec(f.read(), {}, version_ns)
    version = version_ns["__version__"]
    return version


setup(
    name="dash-spa",
    version=_get_version(),
    description="Dash Single Page Application (SPA) Framework",
    packages=find_packages(),
    long_description=read("landing-page.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
    url="https://github.com/stevej2608/dash-spa",
    author="Steve Jones",
    author_email="jonesst2608@gmail.com",
    license='MIT',
    install_requires=[
        'dash-bootstrap-components',
        'dash-holoniq-components',
    ],
    extras_require={
        "dev": [
            "pytest >= 3.6",
            "invoke",
            "twine",
            "termcolor"
        ],
    },
)
