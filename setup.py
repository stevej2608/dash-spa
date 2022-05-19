import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="dash-pages-spa",
    version="0.1.0",
    url="https://github.com/stevej2608/dash-pages-spa",
    license='MIT',

    author="Steve Jones",
    author_email="jonesst2608@gmail.com",

    description="Dash Pages SPA Framework",
    long_description=read("README.md"),

    packages=find_packages(exclude=('tests',)),
    python_requires='>=3.6'
    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
