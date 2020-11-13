# ----------------------------------------------------------------------------
# Copyright (c) 2016--, Shi Huang.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin
from qiime2.plugin import Metadata, MetadataColumn, Categorical, Numeric, SemanticType
from q2_types.feature_table import FeatureTable, RelativeFrequency, BIOMV210DirFmt
import q2_sample_classifier

import q2_microbiome_age
from q2_microbiome_age._age_prediction import age_prediction

cites = qiime2.plugin.Citations.load('citations.bib',
    package='q2_microbiome_age')

plugin = qiime2.plugin.Plugin(
    name='microbiome_age',
    version=q2_microbiome_age.__version__,
    website='http://www.github.com/shihuang047/q2_microbiome_age',
    package='q2_microbiome_age',
    citations=[cites['agepred2020shi']],
    description=('This QIIME 2 plugin performs the age prediction '
                 'for microbiome data in the context of AGP data. '),
    short_description='Age prediction based on microbiome data.',
    user_support_text=('Raise an issue on the github repo: https://github.com/shihuang047/q2_microbiome_age')
)

# Register functions
plugin.methods.register_function(
    function=age_prediction,
    inputs={'table': FeatureTable[RelativeFrequency],
            'metadata': MetadataColumn[Numeric],
    },
    outputs=[('updated_metadata', Metadata[XX])],
    input_descriptions={
        'table': ('The feature table containing the samples which will be '
                  'used for age prediction.')
    },
    parameters={'metadata': MetadataColumn[Numeric],
                '': qiime2.plugin.Int,
                '': qiime2.plugin.Float
    },
    parameter_descriptions={
        'metadata': ('Sample metadata column which has samples '
            'labeled as "case" or "control". Samples which '
            'are not labeled are not included in the output table.'))
    },
    output_descriptions={
        'updated_metadata': ('The microbiome age will be inserted into '
            'metadata file.'
            )},
    name='Microbiome age prediction',
    description=('Age prediction based on microbiome data under the context'
                 'of AGP or other large datasets.')
)

