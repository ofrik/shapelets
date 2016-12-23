__author__ = 'Ofri'

from collections import Counter
from Sequence import Sequence


class Dataset(object):
    def __init__(self, sequencesLocations=None, fields=None, observationPeriod=10, predictionPeriod=1,sequences=None):
        self.fields = fields
        self.classes = Counter()
        self.sequencesLocations = []
        self.predictionPeriod = predictionPeriod
        self.observationPeriod = observationPeriod
        self.sequencesClasses = {}
        self.sequences = []
        if sequencesLocations is not None:
            for s in sequencesLocations:
                self.addSequenceLocation(s)
        if sequences is not None:
            for s in sequences:
                self.addSequence(s)

    def addSequenceLocation(self, sequenceLocation):
        self.sequencesLocations.append(sequenceLocation)
        seq = Sequence.loadCSVSequence(sequenceLocation, self.fields, self.observationPeriod, self.predictionPeriod)
        self.sequences.append(seq)
        if seq.getLabel() not in self.sequencesClasses:
            self.sequencesClasses[seq.getLabel()] = []
        self.sequencesClasses[seq.getLabel()].append(sequenceLocation)
        self.classes[seq.getLabel()] += 1

    def addSequence(self,seq):
        self.sequences.append(seq)
        if seq.getLabel() not in self.sequencesClasses:
            self.sequencesClasses[seq.getLabel()] = []
        self.sequencesClasses[seq.getLabel()].append(seq)
        self.classes[seq.getLabel()] += 1

    def addSequencesLocations(self, sequencesLocations):
        for s in sequencesLocations:
            self.addSequenceLocation(s)

    def getSequencesClasses(self):
        return self.sequencesClasses.values()

    def getAllOtherSequences(self, current):
        all_a, all_b = self.getSequencesClasses()
        exclude = [item for list in current for item in list]
        C_A = [item for item in all_a if item not in exclude]
        C_B = [item for item in all_b if item not in exclude]
        return C_A, C_B

    def setFields(self, fields):
        self.fields = fields

    def getFields(self):
        return self.fields

    def getClasses(self):
        return self.classes

    def getSequencesLocations(self):
        return self.sequencesLocations

    # def getSequences(self):
    #     return [Sequence.loadCSVSequence(path, self.fields, self.observationPeriod, self.predictionPeriod) for path in
    #             self.sequencesLocations]

    def getSequences(self):
        return self.sequences

    def getSequencesGenerator(self):
        for seq in self.sequences:
            yield seq

    def getSequencesGeneratorLazy(self):
        for path in self.sequencesLocations:
            yield Sequence.loadCSVSequence(path, self.fields, self.observationPeriod, self.predictionPeriod)

    def setObservationPeriod(self, period):
        self.observationPeriod = period

    def setPredictionPeriod(self, period):
        self.predictionPeriod = period

    def getObservationPeriod(self):
        return self.observationPeriod

    def getPredictionPeriod(self):
        return self.predictionPeriod

    def getClassesProb(self):
        l = len(self.sequences)
        # dist = dict()
        # for key,value in self.classes.iteritems():
        #     dist[key] = value/l
        return [(key, float(value) / l) for (key, value) in self.classes.iteritems()]

    def getOtherClassSequences(self):
        pass

    def __len__(self):
        return len(self.sequences)

    def __add__(self, other):
        if type(other) != Dataset and self.getFields() == other.getFields():
            raise Exception("not the same type")
        d = Dataset(sequences=self.getSequences()+other.getSequences(),fields=self.fields)
        # d.sequencesLocations = self.sequencesLocations + other.getSequencesLocations()
        # d.classes = self.classes + other.getClasses()
        return d


if __name__ == "__main__":
    print "started"
