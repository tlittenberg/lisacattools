import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lisacattools", # Replace with your own username
    version="0.0.7",
    author="James I. Thorpe, Tyson B. Littenberg",
    author_email="tyson.b.littenberg@nasa.gov",
    description="A small example package for using LISA catalogs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tlittenberg/ldasoft",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
