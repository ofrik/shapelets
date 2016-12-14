from unittest import TestCase
from shapelets.models.Dataset import Dataset
from shapelets.models.Sequence import Sequence
import types

__author__ = 'Ofri'

if __name__ == "__main__":
    print "started"


class TestDataset(TestCase):
    def test_addSequence(self):
        d = Dataset(field="smart_1_normalized")
        self.assertEqual(len(d.getSequencesLocations()), 0)
        d.addSequenceLocation("resources/disks/failed/5XW0L6BV.csv.gz")
        self.assertEqual(len(d.getSequencesLocations()), 1)
        self.assertItemsEqual(d.getSequencesLocations(), ["resources/disks/failed/5XW0L6BV.csv.gz"])

    def test_addSequences(self):
        lst = ["resources/disks/failed/5XW0L6BV.csv.gz", "resources/disks/run/5VMJW1LH.csv.gz"]
        d = Dataset(field="smart_1_normalized")
        self.assertEqual(len(d.getSequencesLocations()), 0)
        d.addSequencesLocations(lst)
        self.assertItemsEqual(d.getSequencesLocations(), lst)

    def test_setField(self):
        d = Dataset()
        self.assertEqual(d.getField(),None)
        d.setField("test")
        self.assertEqual(d.getField(),"test")

    def test_getClasses(self):
        lst = ["resources/disks/failed/5XW0L6BV.csv.gz", "resources/disks/run/5VMJW1LH.csv.gz"]
        d = Dataset(lst, "smart_1_normalized")
        self.assertDictEqual(d.getClasses(),{"failed":1,"run":1})

    def test_getSequencesLocations(self):
        lst = ["resources/disks/failed/5XW0L6BV.csv.gz","resources/disks/run/5VMJW1LH.csv.gz"]
        d = Dataset(lst,"smart_1_normalized")
        self.assertItemsEqual(d.getSequencesLocations(), lst)

    def test_getSequencesGenerator(self):
        lst = ["resources/disks/failed/5XW0L6BV.csv.gz", "resources/disks/run/5VMJW1LH.csv.gz"]
        d = Dataset(lst, "smart_1_normalized")
        s1 = Sequence.loadCSVSequence("resources/disks/failed/5XW0L6BV.csv.gz", "smart_1_normalized", 1, )
        s2 = Sequence.loadCSVSequence("resources/disks/run/5VMJW1LH.csv.gz", "smart_1_normalized", 1, )
        itr = iter(d.getSequencesGeneratorLazy())
        s3 = itr.next()
        s4 = itr.next()
        self.assertEqual(s1,s3)
        self.assertEqual(s2,s4)
        d = Dataset(lst, "smart_1_normalized")
        self.assertEqual(type(d.getSequencesGeneratorLazy()), types.GeneratorType)

    def test_getClassesProb(self):
        lst = ["resources/disks/failed/5XW0L6BV.csv.gz", "resources/disks/run/5VMJW1LH.csv.gz"]
        d = Dataset(lst, "smart_1_normalized")
        self.assertItemsEqual(d.getClassesProb(),[("failed",0.5),("run",0.5)])

    def test___add__(self):
        lst = ["resources/disks/failed/5XW0L6BV.csv.gz", "resources/disks/run/5VMJW1LH.csv.gz"]
        d = Dataset(lst, "smart_1_normalized")
        d2 = Dataset(lst, "smart_1_normalized")
        d3 = d+d2
        self.assertEqual(len(d3),4)
        self.assertDictEqual(d3.getClasses(),{"failed":2,"run":2})
        self.assertEqual(d3.getField(),"smart_1_normalized")
