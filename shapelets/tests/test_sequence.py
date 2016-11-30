from unittest import TestCase
from shapelets.models.Sequence import Sequence

__author__ = 'Ofri'

if __name__ == "__main__":
    print "started"


class TestSequence(TestCase):
    def test_getValues(self):
        seq = Sequence([1,2,3,4,5],"test")
        self.assertItemsEqual(seq.getValues(),[1,2,3,4,5])

    def test_getLabel(self):
        seq = Sequence([1, 2, 3, 4, 5], "test")
        self.assertEqual(seq.getLabel(),"test")

    def test_addValue(self):
        seq = Sequence([1, 2, 3, 4, 5], "test")
        self.assertItemsEqual(seq.getValues(),[1,2,3,4,5])
        seq.addValue(6)
        self.assertItemsEqual(seq.getValues(), [1, 2, 3, 4, 5,6])

    def test_loadCSVSequence(self):
        try:
            seq = Sequence.loadCSVSequence("resources/disks/failed/5XW0L6BV.csv.gz","smart_1_normalized")
        except:
            self.fail("couldn't load the resource")
        self.assertEqual(seq.getLabel(),"failed")
        self.assertEqual(len(seq.getValues()),205)
        self.assertEqual(type(seq.getValues()),list)
        try:
            seq = Sequence.loadCSVSequence("resources/disks/run/5VMJW1LH.csv.gz", "smart_1_normalized")
        except:
            self.fail("couldn't load the resource")
        self.assertEqual(seq.getLabel(), "run")
        self.assertEqual(len(seq.getValues()), 363)
        self.assertEqual(type(seq.getValues()), list)