import unittest
from shapelets.utils.utils import GenerateSubsequences
import numpy as np

class test_utils(unittest.TestCase):
    def test_generateSubsequences(self):
        windows = GenerateSubsequences(np.array([i for i in range(10)]), 3)
        res = list(windows)
        self.assertEqual(len(res),8)
        self.assertEqual(res[0].shape[0],3)
        self.assertEqual(list(res[0]),[0,1,2])


if __name__ == '__main__':
    unittest.main()
