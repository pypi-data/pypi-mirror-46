"""
See: https://packaging.python.org/tutorials/packaging-projects/
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cobratools",
    version="0.0.2",
    author="Clayton Cafiero",
    author_email="clayton.cafiero@uvm.edu",
    description="Tools for bioinformatics and glue for RLR analysis pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cbcafiero/cobra",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)