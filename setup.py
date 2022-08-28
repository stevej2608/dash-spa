import os
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

def read_req_file(req_type):
    with open(f"requires-{req_type}.txt", encoding="utf-8") as fp:
        requires = (line.strip() for line in fp)
        return [req for req in requires if req and not req.startswith("#")]

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

    packages=find_packages(exclude=["pages*", "examples*", "tests*"]),

    include_package_data=True,
	python_requires='>=3.6',
    install_requires=read_req_file("install"),

    extras_require={
        "admin": read_req_file("admin"),
        "dev": read_req_file("dev"),
        "redis": read_req_file("redis"),
        "diskcache": read_req_file("diskcache"),
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