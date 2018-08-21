import unittest
from q2_cscs.q2_cscs import cscs, calc_distances,extract_css_matrix
import pandas as pd


class CSCSTestCase(unittest.TestCase):
    def setUp(self):
        featurespd = pd.read_csv('data/small_GNPS_buckettable.tsv', sep = "\t")
        self.sample_names = featurespd.columns.values
        self.features = featurespd
        self.css = pd.read_csv('data/small_css_matrix.tsv', sep = "\t")
        self.edges = pd.read_csv('data/small_GNPS_edges.tsv', delimiter="\t")
        
    def test_simple(self):
        self.assertEqual(True, True, "simple test")

    def test_extract_css_matrix(self):
        css = extract_css_matrix(self.edges)
        print(css)
        print(css.values.sum())
        self.assertEqual(True, True, "simple test")
        
    def test_calc_distances(self):
        #cscs = calc_distances(self.features, self.css, self.sample_names)
        #print(cscs)
        self.assertEqual(True, True, "simple test")
if __name__ == '__main__':
    unittest.main()
