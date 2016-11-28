__author__ = 'Ofri'
import numpy as np
import math

def GenerateSubsequences(sequence, windowSize):
    n = sequence.shape[0]
    for i in xrange(0,n-windowSize+1):
        yield np.array(sequence[i:windowSize + i])
    # for i in xrange(n-windowSize):

def GenerateAllSequences(sequence, windowSize):
    for l in reversed(xrange(1,windowSize)):
        for s in GenerateSubsequences(sequence, l):
            yield s



def Gain(D,D1,D2):
    def getClassProbability(D):
        # TODO implement
        pass
    def I(D):
        P_A, P_B = getClassProbability(D)
        return -P_A * math.log(P_A) - P_B * math.log(P_B)

    def IRoof(D):
        f_D1 = D1.shape[0] / D.shape[0]
        f_D2 = 1 - f_D1
        return f_D1 * I(D1) + f_D2 * I(D2)
    return I(D)-IRoof(D)

if __name__ == "__main__":
    print "started"