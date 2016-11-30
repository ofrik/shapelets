__author__ = 'Ofri'

from collections import Counter
from Sequence import Sequence

class Dataset(object):

    def __init__(self, sequencesLocations=None,field=None):
        self.field = field
        self.classes = Counter()
        self.sequencesLocations = []
        if sequencesLocations is not None:
            for s in sequencesLocations:
                self.addSequenceLocation(s)

    def addSequenceLocation(self, sequenceLocation):
        self.sequencesLocations.append(sequenceLocation)
        seq = Sequence.loadCSVSequence(sequenceLocation,self.field)
        self.classes[seq.getLabel()] += 1

    def addSequencesLocations(self, sequencesLocation):
        for s in sequencesLocation:
            self.addSequenceLocation(s)

    def setField(self,field):
        self.field = field

    def getField(self):
        return self.field

    def getClasses(self):
        return self.classes

    def getSequencesLocations(self):
        return self.sequencesLocations

    def getSequences(self):
        return [Sequence.loadCSVSequence(path,self.field) for path in self.sequencesLocations]

    def getSequencesGenerator(self):
        for path in self.sequencesLocations:
            yield Sequence.loadCSVSequence(path,self.field)

    def getClassesProb(self):
        l = len(self.sequencesLocations)
        # dist = dict()
        # for key,value in self.classes.iteritems():
        #     dist[key] = value/l
        return [(key,float(value)/l) for (key,value) in self.classes.iteritems()]

    def __len__(self):
        return len(self.sequencesLocations)


if __name__ == "__main__":
    print "started"
