import unittest
from shapelets.utils.utils import GenerateSubsequences,Gain
from shapelets.models import *

class test_utils(unittest.TestCase):
    def test_generateSubsequences(self):
        windows = GenerateSubsequences([i for i in range(10)], 3)
        res = list(windows)
        self.assertEqual(len(res),8)
        self.assertEqual(len(res[0]),3)
        self.assertEqual(list(res[0]),[0,1,2])

    def test_Gain(self):
        D = Dataset(["resources/disks/failed/5XW0L6BV.csv.gz", "resources/disks/run/5VMJW1LH.csv.gz"], "smart_1_normalized")
        D1 = Dataset(["resources/disks/failed/5XW0L6BV.csv.gz"],"smart_1_normalized")
        D2 = Dataset(["resources/disks/run/5VMJW1LH.csv.gz"], "smart_1_normalized")
        res = Gain(D,D1,D2)
        self.assertAlmostEqual(res,0.69,delta=0.01)
        D = Dataset(["resources/disks/failed/5XW0L6BV.csv.gz", "resources/disks/run/5VMJW1LH.csv.gz","resources/disks/run/5VMJW1LH.csv.gz"],
                    "smart_1_normalized")
        D1 = Dataset(["resources/disks/failed/5XW0L6BV.csv.gz","resources/disks/run/5VMJW1LH.csv.gz"], "smart_1_normalized")
        D2 = Dataset(["resources/disks/run/5VMJW1LH.csv.gz"], "smart_1_normalized")
        res = Gain(D, D1, D2)
        self.assertAlmostEqual(res, 0.17,delta=0.01)

if __name__ == '__main__':
    unittest.main()
