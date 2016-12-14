__author__ = 'Ofri'

import glob
import random
import csv
from shapelets import FindingShapeletBF, FindKShapelet, EstimateMinAndMax
from shapelets.models import Dataset
import time
import cPickle as pickle

def writeHeader():
    with open("results.csv", 'ab') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(
            ["id", "train_sequences_paths", "test_sequences_paths", "number_of_train_sequences",
             "number_of_test_sequences", "observation_period", "prediction_period",
             "shapelet_min_length", "shapelet_max_length", "computing_time"])


def writeExperiment(id, trainSeqs, testSeqs, numTrainSeq, numTestSeq, obsPer, predPer, minLen, maxLen, took):
    with open("results.csv", 'ab') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow([id, trainSeqs, testSeqs, numTrainSeq, numTestSeq, obsPer, predPer, minLen, maxLen, took])


if __name__ == "__main__":
    paths = glob.glob("resources/disks/*/*")
    random.shuffle(paths)
    fields = ['smart_1_normalized', 'smart_5_raw', 'smart_5_normalized', 'smart_187_normalized',
              'smart_195_normalized', 'smart_197_raw', 'smart_197_normalized']
    observationPeriods = [10]
    predictionPeriods = [1]
    trainDatabase, testDatabase = paths[:int(len(paths) * 0.8)], paths[int(len(paths) * 0.8):]
    print "Train Size: %s sequences\t Test Size: %s sequences" % (len(trainDatabase), len(testDatabase))
    writeHeader()
    counter = 0
    NUMBER_OF_SHAPELETS = 100
    for obsPeriod in observationPeriods:
        for predPeriod in predictionPeriods:
            t0 = time.time()
            D = Dataset(trainDatabase, fields, obsPeriod, predPeriod)
            min_len, max_len = EstimateMinAndMax(D)
            print "Using observation period: %s\t prediction period: %s\nmin shapelet length: %s\tmax shapelet length: %s" % (
            obsPeriod, predPeriod, min_len, max_len)
            shapelets = FindKShapelet(D, NUMBER_OF_SHAPELETS, min_len, max_len)
            took = time.time() - t0
            with open("experiment_%s.pkl"%counter,'wb') as f:
                pickle.dump(shapelets,f)
            print "Took %s" % (took)
            writeExperiment(counter, trainDatabase, testDatabase, len(trainDatabase), len(testDatabase), obsPeriod,
                            predPeriod, min_len, max_len, took)
            counter += 1
