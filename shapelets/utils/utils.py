__author__ = 'Ofri'
import numpy as np
import math

def GenerateSubsequences(sequence, windowSize):
    n = len(sequence)
    for i in xrange(0,n-windowSize+1):
        yield sequence[i:windowSize + i]

def GenerateAllSequences(sequence, windowSize):
    for l in reversed(xrange(1,windowSize+1)):
        for s in GenerateSubsequences(sequence, l):
            yield s

def Gain(D,D1,D2):
    def getClassProbability(D):
        return D.getClassesProb()

    def I(D):
        P_A, P_B = getClassProbability(D)
        return -P_A * math.log(P_A) - P_B * math.log(P_B)

    def IRoof(D):
        f_D1 = len(D1) / len(D)
        f_D2 = 1 - f_D1
        return f_D1 * I(D1) + f_D2 * I(D2)
    return I(D)-IRoof(D)

if __name__ == "__main__":
    print "started"