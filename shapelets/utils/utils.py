__author__ = 'Ofri'
import numpy as np
import math

def GenerateSubsequences(sequence, windowSize):
    n = len(sequence)
    for i in xrange(0,n-windowSize+1):
        yield sequence[i:windowSize + i]

def Gain(D,D1,D2):
    def getClassProbability(D):
        return D.getClassesProb()

    def I(D):
        sum = 0
        for key,value in getClassProbability(D):
            sum += -value*math.log(value,math.e)
        return sum

    def IRoof(D):
        f_D1 = float(len(D1)) / len(D)
        f_D2 = 1 - f_D1
        return f_D1 * I(D1) + f_D2 * I(D2)
    return I(D)-IRoof(D)

if __name__ == "__main__":
    print "started"