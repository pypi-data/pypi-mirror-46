"""
CHIME/FRB Application Programming Interface
"""
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    # CHIME/FRB API
    name="chime-frb-api",
    version="2019.05",
    description="CHIME/FRB API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://chime-frb-open-data.github.io/",
    author="CHIME/FRB Collaboration",
    author_email="charanjot.brar@mcgill.ca",
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="CHIME FRB API",
    packages=find_packages(),
    scripts=[],
    install_requires=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
    project_urls={
        "Bug Reports": "https://github.com/CHIMEFRB/frb-api/issues"
    },
)
