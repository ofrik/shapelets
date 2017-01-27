__author__ = 'Ofri'

import numpy as np
import math
from random import uniform

from shapelets.utils.utils import GenerateSubsequences, Gain
from shapelets.models import *
import random
from multiprocessing import Pool
from shapelets.utils.utils import timeit

MIN_SEQUENCE_SIZE = 3


def FindingShapeletBF(D, minlen, maxlen):
    bsf_gain = 0
    bsf_shapelet = None
    counter = 0
    gains = dict()
    for S in GenerateCandidates(D, minlen, maxlen):
        print "scanned %s candidates" % counter
        if str(S) in gains:
            gain = gains[str(S)]
        else:
            gain = CheckCandidate(D, S)
            gains[str(S)] = gain
        counter += 1
        if gain > bsf_gain:
            bsf_gain = gain
            bsf_shapelet = S
    return bsf_shapelet


@timeit
def FindKShapelet(D, K, minlen, maxlen):
    bsf_gain = 0
    worst_best_gain = 0
    kbest = []
    counter = 0
    gains = dict()
    number_of_candidates = len(list(GenerateCandidates(D, minlen, maxlen)))
    for S in GenerateCandidates(D, minlen, maxlen):
        print "scanned %s/%s candidates" % (counter,number_of_candidates)
        if str(S) in gains:
            print "used cache"
            counter += 1
            continue
        else:
            gain = CheckCandidate(D, S, worst_best_gain, False,False)
            gains[str(S)] = gain
        counter += 1
        # if gain > bsf_gain:
        bsf_gain = gain
        kbest.append((bsf_gain, S))
        kbest = sorted(kbest, key=lambda x: x[0])[-K:]
        worst_best_gain = kbest[0][0]
    return [s[1] for s in kbest]

def ShapeletsTransform(S,D):
    X = []
    Y = []
    for T in D.getSequencesGenerator():
        transformed = []
        for s in S:
            dist = SubsequenceDistanceEarlyAbandon(T,s)
            transformed.append(dist)
        X.append(transformed)
        Y.append(T.getLabel())
    return X,Y

def EstimateMinAndMax(D):
    shapelets = []
    for i in range(10):
        random.shuffle(D.getSequences())
        D_ = Dataset(sequences=D.getSequences()[:10],fields=D.getFields(),observationPeriod=D.getObservationPeriod(),predictionPeriod=D.getPredictionPeriod())
        foundShepelets = FindKShapelet(D_,10,MIN_SEQUENCE_SIZE,D_.getObservationPeriod())
        shapelets += foundShepelets
    shapelets.sort(key=len)
    min = len(shapelets[25])
    max = len(shapelets[75])
    return min,max

def GenerateCandidates(D, minlen, maxlen):
    for l in reversed(xrange(minlen, maxlen + 1)):
        for T in D.getSequencesGenerator():
            for s, i in GenerateSubsequences(T.getValues(), l):
                yield s

def CheckCandidate(D, S, worst_best_gain, toTryToPrune=False,parallel=False):
    objects_histogram = {}
    counter = 0
    if parallel:
        def aggregator(res):
            if res[0] not in objects_histogram:
                objects_histogram[res[0]] = []
            objects_histogram[res[0]].append(res[1])
        pool = Pool()
    for T in D.getSequencesGenerator():
        if parallel:
            pool.apply_async(SubsequenceDistanceEarlyAbandon,args=(T,S),callback=aggregator)
        else:
            dist = SubsequenceDistanceEarlyAbandon(T, S)
            if dist not in objects_histogram:
                objects_histogram[dist] = []
            objects_histogram[dist].append(T)
        counter += 1
        if toTryToPrune and counter >= 5:
            C_A, C_B = D.getAllOtherSequences(objects_histogram.values())
            if EntropyEarlyPrune(worst_best_gain, objects_histogram, C_A, C_B, D.getFields()):
                print "pruned"
                return 0
    if parallel:
        pool.close()
        pool.join()
    return CalculateInformationGain(objects_histogram, D.getFields())


def CalculateInformationGain(obj_hist, fields):
    def OptimalSplitPoint(obj_hist, fields):
        bestChosen = -1
        bestGain = -1
        sortedItems = sorted(obj_hist.items(), key=lambda x: x[0])
        for i in range(1, len(sortedItems)):
            chosen = uniform(sortedItems[i - 1][0], sortedItems[i][0])
            # print "between %s and %s choose %s" % (sortedItems[i - 1][0], sortedItems[i][0], chosen)
            split1 = [item for sublist in sortedItems[:i] for item in sublist[1]]
            split2 = [item for sublist in sortedItems[i:] for item in sublist[1]]
            D1 = Dataset(sequences=split1, fields=fields)
            D2 = Dataset(sequences=split2, fields=fields)
            gain = Gain(D1 + D2, D1, D2)
            if gain > bestGain:
                bestGain = gain
                bestChosen = chosen
        return bestChosen, bestGain

    return OptimalSplitPoint(obj_hist, fields)[1]
    # split_dist = OptimalSplitPoint(obj_hist,field)
    # D1 = Dataset(field=field)
    # D2 = Dataset(field=field)
    # for key,value in obj_hist.iteritems():
    #     if key < split_dist:
    #         D1.addSequencesLocations(value)
    #     else:
    #         D2.addSequencesLocations(value)
    # return Gain(D1 + D2, D1, D2)


def EntropyEarlyPrune(bsf_gain, dist_hist, C_A, C_B, field):
    minend = 0
    maxend = sorted(dist_hist.keys())[-1] + 1
    pred_dist_hist = dist_hist
    pred_dist_hist[minend] = C_A
    pred_dist_hist[maxend] = C_B
    if CalculateInformationGain(pred_dist_hist, field) > bsf_gain:
        return False
    pred_dist_hist[minend] = C_B
    pred_dist_hist[maxend] = C_A
    if CalculateInformationGain(pred_dist_hist, field) > bsf_gain:
        return False
    return True

def SubsequenceDistanceEarlyAbandon(T, S):
    min_dist = np.inf
    stop = False
    for S_i, i in GenerateSubsequences(T.getValues(), len(S)):
        sum_dist = 0
        for k in xrange(0, len(S)):
            for j in xrange(len(S_i[k])):
                d = math.pow((S_i[k][j] - S[k][j]), 2)
                if np.isnan(d):
                    d = 0
                    # print "is nan"
                sum_dist = sum_dist + d
            if sum_dist > min_dist:
                stop = True
                break
        if not stop:
            min_dist = sum_dist
    return 0 if min_dist == 0 else math.log(min_dist)


if __name__ == "__main__":
    print "started"
