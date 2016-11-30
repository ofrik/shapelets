import unittest

from shapelets.shapelet import GenerateCandidates,SubsequenceDistanceEarlyAbandon,CalculateInformationGain
from shapelets.models import *

class test_shapelet(unittest.TestCase):
    def test_GenerateCandidates(self):
        d = Dataset(["resources/disks/failed/5XW0L6BV.csv.gz", "resources/disks/run/5VMJW1LH.csv.gz"],"smart_1_normalized")
        res = list(GenerateCandidates(d,1,1))
        self.assertEqual(len(res),568)
        res = list(GenerateCandidates(d, 2, 2))
        self.assertEqual(len(res), 566)
        res = list(GenerateCandidates(d, 1, 2))
        self.assertEqual(len(res), 1134)

    def test_CheckCandidate(self):
        self.fail()

    def test_CalculateInformationGain(self):
        dist = {
            0.1:["resources/disks/failed/5XW0L6BV.csv.gz","resources/disks/failed/5XW0L6BV.csv.gz"],
            0.6: ["resources/disks/run/5VMJW1LH.csv.gz"],
            0.7: ["resources/disks/failed/5XW0L6BV.csv.gz"],
            0.8: ["resources/disks/run/5VMJW1LH.csv.gz"],
            0.85: ["resources/disks/run/5VMJW1LH.csv.gz"],
            0.9: ["resources/disks/run/5VMJW1LH.csv.gz"],
            0.3:["resources/disks/failed/5XW0L6BV.csv.gz"],
            0.4:["resources/disks/failed/5XW0L6BV.csv.gz"],
            0.5:["resources/disks/failed/5XW0L6BV.csv.gz"]
        }
        res = CalculateInformationGain(dist,"smart_1_normalized")
        self.assertAlmostEqual(res,0.42,delta=0.01)

    def test_EntropyEarlyPrune(self):
        self.fail()

    def test_SubsequenceDistanceEarlyAbandon(self):
        T = Sequence([2,3,5,7,4,5,8],"test")
        S = Sequence([3,7,4],"test2")
        dist = SubsequenceDistanceEarlyAbandon(T,S)
        self.assertEqual(dist,4)

    def test_FindingShapeletBF(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()
