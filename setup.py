import os
import re

from setuptools import find_packages
from setuptools import setup


HERE = os.path.dirname(os.path.abspath(__file__))

def _get_long_description():
    with open(os.path.join(HERE, "landing-page.md")) as f:
        return f.read()

def _get_version():
    """ Get version by parsing _version programmatically """
    packages = ["dash_spa"]
    version_ns = {}
    with open(
            os.path.join(HERE, packages[0], "_version.py")
    ) as f:
        exec(f.read(), {}, version_ns)
    version = version_ns["__version__"]
    return version

def _get_dependencies():
    """Parse requirements.txt and return a list of dependencies"""
    with open(os.path.join(HERE, "requirements.txt")) as f:
        requirements = f.read()

    result = []
    requirements = requirements.split('\n')
    for r in requirements:
        if r == '# setup.py - exclude':
            break
        if r == '' or r.startswith('#'):
            continue
        result.append(r)
    return result

def _get_extra_dependencies(extra):
    """Parse requirements.txt and return a list of the
    extra dependencies required for 'extra' """
    with open(os.path.join(HERE, "requirements.txt")) as f:
        requirements = f.read()

    result = []
    sections = []
    requirements = requirements.split('\n')
    for r in requirements:
        if r.startswith('# setup.py - extra'):
            sections = re.split(r'\W+', r)[4:]
            continue
        if r == '' or r.startswith('#'):
            if len(result) > 0:
                break
            else:
                continue
        if extra in sections:
            result.append(r)
    return result

setup(
    name="dash-spa",
    version=_get_version(),
    url="https://github.com/stevej2608/dash-spa",
    license='MIT',

    author="Steve Jones",
    author_email="jonesst608@gmail.com",

    description="Dash Pages SPA Framework",
    long_description=_get_long_description(),
    long_description_content_type='text/markdown',

    packages=find_packages(include=[
        'dash_spa','dash_spa.plugins','dash_spa.utils',
        'dash_spa.components','dash_spa.components.table',
        'dash_spa.session','dash_spa.session.backends',
        'dash_spa_admin', 'dash_spa_admin.views'
        ]),

    include_package_data=True,
	python_requires='>=3.6',
    install_requires=_get_dependencies(),
    extras_require={
        "admin": _get_extra_dependencies("dash_spa_admin"),
    },

    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Dash",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)