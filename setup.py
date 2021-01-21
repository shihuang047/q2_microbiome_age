# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, Shi Huang.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

# Setup copied from q2-emperor
setup(
    name="microbiome_age",
    version="2020.11.13",
    packages=find_packages(),
    author="Shi Huang",
    author_email="shh047@health.ucsd.edu",
    description="Age prediction using microbiome data",
    license='BSD-3-Clause',
    url="https://qiime2.org",
    entry_points={
        'qiime2.plugins':
        ['q2_microbiome_age=q2_microbiome_age.plugin_setup:plugin']
    },
    zip_safe=False,
    package_data={
        'q2_microbiome_age': ['citations.bib']
    }
)
