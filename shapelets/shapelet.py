__author__ = 'Ofri'

import numpy as np
import math
from random import uniform

from shapelets.utils.utils import GenerateSubsequences, Gain
from shapelets.models import *


def FindingShapeletBF(D, maxlen, minlen):
    bsf_gain = 0
    bsf_shapelet = None
    for candidates in GenerateCandidates(D, minlen,maxlen):
        for S in candidates:
            gain = CheckCandidate(D, S)
            if gain > bsf_gain:
                bsf_gain = gain
                bsf_shapelet = S
    return bsf_shapelet


def GenerateCandidates(D, minlen, maxlen):
    for l in reversed(xrange(minlen, maxlen+1)):
        for T in D.getSequencesGenerator():
            for s in GenerateSubsequences(T.getValues(), l):
                yield s

def CheckCandidate(D, S):
    objects_histogram = {}
    for T in D.getSequencesGenerator():
        dist = SubsequenceDistanceEarlyAbandon(T, S)
        if dist not in objects_histogram:
            objects_histogram[dist] = []
        objects_histogram[dist].append(T)
    return CalculateInformationGain(objects_histogram,D.getField())


def CalculateInformationGain(obj_hist,field):
    def OptimalSplitPoint(obj_hist,field):
        bestChosen = -1
        bestGain = -1
        sortedItems = sorted(obj_hist.items(), key=lambda x: x[0])
        for i in range(1, len(sortedItems)):
            chosen = uniform(sortedItems[i - 1][0], sortedItems[i][0])
            print "between %s and %s choose %s" % (sortedItems[i - 1][0], sortedItems[i][0], chosen)
            split1 = [item for sublist in sortedItems[:i] for item in sublist[1]]
            split2 = [item for sublist in sortedItems[i:] for item in sublist[1]]
            D1 = Dataset(split1,field)
            D2 = Dataset(split2,field)
            gain = Gain(D1 + D2, D1, D2)
            if gain > bestGain:
                bestGain = gain
                bestChosen = chosen
        return bestChosen,bestGain
    return OptimalSplitPoint(obj_hist,field)[1]
    # split_dist = OptimalSplitPoint(obj_hist,field)
    # D1 = Dataset(field=field)
    # D2 = Dataset(field=field)
    # for key,value in obj_hist.iteritems():
    #     if key < split_dist:
    #         D1.addSequencesLocations(value)
    #     else:
    #         D2.addSequencesLocations(value)
    # return Gain(D1 + D2, D1, D2)


def EntropyEarlyPrune(bsf_gain, dist_hist, C_A, C_B):
    # TODO implement
    pass


def SubsequenceDistanceEarlyAbandon(T, S):
    min_dist = np.inf
    stop = False
    for S_i in GenerateSubsequences(T.getValues(), len(S)):
        sum_dist = 0
        for k in xrange(0, len(S)):
            sum_dist = sum_dist + math.pow((S_i[k] - S[k]), 2)
            if sum_dist > min_dist:
                stop = True
                break
        if not stop:
            min_dist = sum_dist
    return min_dist



if __name__ == "__main__":
    print "started"
