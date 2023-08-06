#!/usr/bin/env python
import imp
import io
import os

try:
    from setuptools import find_packages, setup
except ImportError:
    raise ImportError(
        "'setuptools' is required but not installed. To install it, "
        "follow the instructions at "
        "https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py")


def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


root = os.path.dirname(os.path.realpath(__file__))
version_module = imp.load_source(
    "version", os.path.join(root, "nengo_sphinx_theme", "version.py"))

install_requires = ["sphinx>=1.8"]

setup(
    name="nengo-sphinx-theme",
    version=version_module.version,
    author="Applied Brain Research",
    author_email="info@appliedbrainresearch.com",
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    url="https://github.com/nengo/nengo-sphinx-theme",
    license="Apache v2",
    description="Sphinx theme for Nengo websites",
    long_description=read("README.rst", "CHANGES.rst"),
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        "sphinx.html_themes": [
            "nengo_sphinx_theme = nengo_sphinx_theme",
        ],
    },
)
