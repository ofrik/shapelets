__author__ = 'Ofri'

import pandas as pd

class Sequence(object):
    values = []
    label = None

    def __init__(self, values, label):
        self.values = values
        self.label = label

    def getValues(self):
        return self.values

    def getLabel(self):
        return self.label

    def addValue(self, val):
        self.values.append(val)

    @staticmethod
    def loadCSVSequence(path,field,compression="gzip"):
        df = pd.read_csv(path,compression=compression)
        l = "failed" if "failed" in path else "run"
        return Sequence(df[field].values, l)


if __name__ == "__main__":
    print "started"
