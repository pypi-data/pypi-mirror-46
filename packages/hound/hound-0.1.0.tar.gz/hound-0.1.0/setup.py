from setuptools import setup
from hound import __version__

setup(
    name = 'hound',
    version = __version__,
    packages = [
        'hound',
    ],
    description = 'A FireCloud database extension',
    url = 'https://github.com/broadinstitute/hound',
    author = 'Aaron Graubert - Broad Institute - Cancer Genome Computational Analysis',
    author_email = 'aarong@broadinstitute.org',
    long_description = 'A FireCloud database extension',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    ],
    license="BSD3"
)
