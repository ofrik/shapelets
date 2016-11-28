__author__ = 'Ofri'

from collections import Counter


class Dataset(object):
    sequences = []
    classes = Counter()

    def __init__(self, sequences=None):
        if sequences is not None:
            for s in sequences:
                self.addSequence(s)

    def addSequence(self, sequence):
        self.sequences.append(sequence)
        self.classes[sequence.getLabel()] += 1

    def getClasses(self):
        return self.classes

    def getSequences(self):
        return self.sequences

    def getClassesProb(self):
        l = len(self.sequences)
        dist = dict
        for key,value in self.classes.iteritems():
            dist[key] = value/l
        return dist


if __name__ == "__main__":
    print "started"
