__author__ = 'Ofri'


class Sequence(object):
    values = []
    label = None

    def __init__(self, values, label):
        self.values = values
        self.label = label
        pass

    def getValues(self):
        return self.values

    def getLabel(self):
        return self.label

    def addValue(self, val):
        self.values.append(val)


if __name__ == "__main__":
    print "started"
