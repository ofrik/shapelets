__author__ = 'Ofri'

import pandas as pd


class Sequence(object):
    values = []
    label = None

    def __init__(self, values, label, src=""):
        self.values = values
        self.label = label
        self.src = src

    def getValues(self):
        return self.values

    def getLabel(self):
        return self.label

    def addValue(self, val):
        self.values.append(val)

    def getSrc(self):
        return self.src

    def __eq__(self, other):
        if type(other) != Sequence:
            return False
        return self.getLabel() == other.getLabel() and self.getValues() == other.getValues()

    def __len__(self):
        return len(self.values)

    def __getitem__(self, item):
        return self.values[item]

    @staticmethod
    def loadCSVSequence(path, field, compression="gzip"):
        df = pd.read_csv(path, compression=compression)
        l = "failed" if "failed" in path else "run"
        # TODO: get only window of the sequence that will be defined
        return Sequence(list(df[field].values), l, src=path)


if __name__ == "__main__":
    print "started"
