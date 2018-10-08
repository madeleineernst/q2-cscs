from qiime2.plugin import Plugin
import qiime2.plugin
import q2_cscs.q2_cscs
import biom
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.distance_matrix import DistanceMatrix
from q2_types.tree import Phylogeny, Rooted
from qiime2.plugin import Str, Choices, Properties, Metadata

plugin = Plugin(
    name='cscs',
    version='0.0.1',
    website='https://qiime2.org',
    user_support_text='https://forum.qiime2.org',
    package='q2_cscs'
)


plugin.methods.register_function(
    function=q2_cscs.q2_cscs.cscs,
    inputs={'features': FeatureTable[Frequency],
            },
    parameters={'css_edges': qiime2.plugin.Str, 'weighted': qiime2.plugin.Bool, 'normalization': qiime2.plugin.Bool, 'cosine_threshold': qiime2.plugin.Float % qiime2.plugin.Range(0., None)},
    outputs=[('distance_matrix', DistanceMatrix % Properties('phylogenetic'))],
    input_descriptions={
        'features': ('The feature table containing the samples over which the chemical structural and compositional dissimilarity metric '
                  'should be computed.')
    },
    parameter_descriptions = {'css_edges': '.tsv file containing pair wise cosine scores for all features provided in the feature table', 'normalization':'Perform Total Ion Current Normalization (TIC) on the feature table', 'cosine_threshold':'Min. cosine score between two features to be included'},
    output_descriptions={'distance_matrix': 'The resulting distance matrix.'},
    name='CSCS',
    description=("Computes the chemical structural and compositional dissimilarity metric for all pairs of samples in a feature table.")
)
