
from setuptools import setup
import os

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the readme file
with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()

setup(
    name = "pyodbc-helpers",
    version = "1.0.0",
    description = "Additional features related to pyodbc.",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/srianbury/pyodbc-helpers",
    author = "srianbury",
    license = "MIT",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    packages = ["pyodbch"],
    install_requires = ["pyodbc"]
)