# -*- coding: utf-8 -*-
from os import path

import setuptools

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

about = {}
with open(
    path.join(here, "lisacattools", "_version.py"), encoding="utf-8"
) as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__name__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={"lisacattools": ["README.md", "logging.conf"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=required,
)
