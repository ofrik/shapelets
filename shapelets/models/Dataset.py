__author__ = 'Ofri'

from collections import Counter
from Sequence import Sequence

class Dataset(object):
    sequencesLocation = []
    classes = Counter()
    field = None

    def __init__(self, sequencesLocation=None):
        if sequencesLocation is not None:
            for s in sequencesLocation:
                self.addSequence(s)

    def addSequence(self, sequenceLocation):
        self.sequencesLocation.append(sequenceLocation)
        seq = Sequence.loadCSVSequence(sequenceLocation)
        self.classes[seq.getLabel()] += 1

    def addSequences(self,sequencesLocation):
        for s in sequencesLocation:
            self.addSequence(s)

    def setField(self,field):
        self.field = field

    def getClasses(self):
        return self.classes

    def getSequences(self):
        return self.sequencesLocation

    def getSequencesGenerator(self):
        for path in self.sequencesLocation:
            yield Sequence.loadCSVSequence(path,self.field)

    def getClassesProb(self):
        l = len(self.sequencesLocation)
        # dist = dict()
        # for key,value in self.classes.iteritems():
        #     dist[key] = value/l
        return [(key,value/l) for (key,value) in self.classes.iteritems()]

    def __sizeof__(self):
        return len(self.sequencesLocation)


if __name__ == "__main__":
    print "started"
