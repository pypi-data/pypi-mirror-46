import os

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


VERSION = os.environ.get("TAG_VERSION")
VERSION = VERSION[1:] if VERSION else "1.0.0.0"

setuptools.setup(
    name="FC Cedibles SDK",
    version=VERSION,
    author="Jose Fidalgo H.",
    author_email="jfidalgo@factorclick.com",
    description="SDK for Cedibles documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/elasbit/fc-cedibledocs-lib",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ),
)
