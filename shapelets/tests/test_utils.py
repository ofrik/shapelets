import unittest
from shapelets.utils.utils import GenerateSubsequences,GenerateAllSequences,Gain
import numpy as np

class test_utils(unittest.TestCase):
    def test_generateSubsequences(self):
        windows = GenerateSubsequences([i for i in range(10)], 3)
        res = list(windows)
        self.assertEqual(len(res),8)
        self.assertEqual(len(res[0]),3)
        self.assertEqual(list(res[0]),[0,1,2])

    def test_GenerateAllSequences(self):
        sequences = GenerateAllSequences([i for i in range(4)],2)
        res = list(sequences)
        self.assertEqual(len(res),7)
        self.assertIn([0],res)
        self.assertIn([0,1],res)

    def test_Gain(self):
        # TODO implement
        self.fail()


if __name__ == '__main__':
    unittest.main()
