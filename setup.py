import os
from setuptools import find_packages, setup

HERE = os.path.dirname(os.path.abspath(__file__))


def _get_long_description():
    with open(os.path.join(HERE, "landing-page.md")) as f:
        return f.read()

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

def _get_version():
    """ Get version by parsing _version programmatically """
    version_ns = {}
    with open(
            os.path.join(HERE, "dash_spa", "_version.py")
    ) as f:
        exec(f.read(), {}, version_ns)
    version = version_ns["__version__"]
    return version


setup(
    name="dash-spa",
    version=_get_version(),
    author="Steve Jones",
    author_email="jonesst608@gmail.com",
    packages=find_packages(exclude=('tests.*','tests','demo', 'user','config', 'examples',)),
    install_requires=_get_dependencies(),
    include_package_data=True,
    license='MIT',
    description="Dash Single Page Application (SPA) Framework",
    long_description=_get_long_description(),
    long_description_content_type="text/markdown",
    classifiers = [
        'Framework :: Dash',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ]
)
