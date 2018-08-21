import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="q2-cscs",
    version="0.0.1",
    author="Asker Brejnrod, Madeleine Ernst, Lasse Buur Rasmussen",
    author_email="askerbrejnrod@gmail.com, mernst@ucsd.edu",
    description="A python implementation of the CSCS distance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askerdb/pyCSCS",
    entry_points={
    'qiime2.plugins': ['q2-cscs=q2_cscs.plugin_setup:plugin']
    },
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    
)
