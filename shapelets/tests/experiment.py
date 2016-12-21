__author__ = 'Ofri'

import glob
import random
import csv
import os
from shapelets import FindingShapeletBF, FindKShapelet, EstimateMinAndMax, ShapeletsTransform
from shapelets.models import Dataset
import time
import cPickle as pickle
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from scipy.stats import linregress
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import confusion_matrix,classification_report


class Experiment(object):
    counter = 0
    resultsPath = ""
    NUM_CROSS_VAL = 5

    def __init__(self, trainDataset, testDataset, obsPeriod, predPeriod, shepeletsToExtract):
        self.observationPeriod = obsPeriod
        self.predictionPeriod = predPeriod
        self.trainDatasetPaths = trainDataset
        self.testDatasetPaths = testDataset
        self.id = Experiment.counter
        self.shapeletsToExtract = shepeletsToExtract
        self.shapelets = []
        self.shapeletsFeatures = []
        self.aggregatedFeatures = []
        self.shapeletsTrainTime = None
        self.shapeletsFeatureExtractionTime = None
        self.aggregatedTrainTime = None
        self.YShapelets = []
        # self.YAggregated = []
        self.aggregatedFeatureExtractionTime = None
        self.fields = ['smart_1_normalized', 'smart_1_raw', 'smart_5_raw', 'smart_5_normalized', 'smart_7_raw',
                       'smart_7_normalized', 'smart_187_raw', 'smart_187_normalized', 'smart_197_raw',
                       'smart_197_normalized']
        self.trainDataset = Dataset(trainDataset, self.fields, obsPeriod, predPeriod)
        self.testDataset = Dataset(testDataset, self.fields, obsPeriod, predPeriod)
        self.shapeletsClfs = []
        self.aggregatedClfs = []
        self.shapeletsConfMatrix = []
        self.aggregatedConfMatrix = []
        Experiment.counter += 1

    def writeExperiment(self):
        if not os.path.exists(Experiment.resultsPath + "results.csv"):
            with open(Experiment.resultsPath + "results.csv", 'ab') as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow(
                    ["id", "number_of_train_sequences",
                     "number_of_test_sequences", "observation_period", "prediction_period",
                     "shapelets_feature_extraction_time", "aggregated_feature_extraction_time",
                     "shapelets_train_time", "aggregated_train_time", "shapelets_conf_matrix",
                     "aggregated_conf_matrix"])
        with open(Experiment.resultsPath + "results.csv", 'ab') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow([self.counter, len(self.trainDataset), len(self.testDataset), self.observationPeriod,
                                self.predictionPeriod, self.shapeletsFeatureExtractionTime,
                                self.aggregatedFeatureExtractionTime, self.shapeletsTrainTime,
                                self.aggregatedTrainTime,self.shapeletsConfMatrix,self.aggregatedConfMatrix])

    def getClassifiers(self):
        return [SVC(), RandomForestClassifier(), KNeighborsClassifier(n_neighbors=1)]

    def findShapelets(self, dataset):
        min_len, max_len = EstimateMinAndMax(dataset)
        self.shapelets = FindKShapelet(dataset, self.shapeletsToExtract, min_len, max_len)
        return self.shapelets

    def transformShapelets(self, shapelets, dataset):
        return ShapeletsTransform(shapelets, dataset)

    def evaluateShapelets(self):
        t0 = time.time()
        self.findShapelets(self.trainDataset)
        X, Y = self.transformShapelets(self.shapelets, self.trainDataset)
        self.shapeletsFeatureExtractionTime = time.time() - t0
        clfs = [("SVM",SVC()), ("Random Forest",RandomForestClassifier()), ("1NN",KNeighborsClassifier(n_neighbors=1))]
        for name,clf in clfs:
            scores = cross_val_score(clf,X,Y,cv=self.NUM_CROSS_VAL,n_jobs=-1)
            print name,scores.mean()
            clf.fit(X,Y)
        self.shapeletsTrainTime = time.time() - self.shapeletsFeatureExtractionTime
        self.shapeletsClfs = clfs
        X_test, Y_test = self.transformShapelets(self.shapelets,self.testDataset)
        for name,clf in clfs:
            pred = clf.predict(X_test)
            m = confusion_matrix(Y_test,pred)
            self.shapeletsConfMatrix.append((name,m))
            print name,m
            print classification_report(Y_test,pred)
            print "expected", Y_test
            print "actual", pred,"\n"
        return clfs

    def extractAggregatedFeatures(self, df):
        stds = list(np.nan_to_num(df.std()))
        means = list(np.nan_to_num(df.mean()))
        slopes = []
        for col in df.columns:
            slope, _, _, _, _ = linregress(x=df[col], y=range(len(df[col])))
            slopes.append(0 if np.isnan(slope) else slope)
        return stds + means + slopes

    def extractAllAggregatedFeatures(self,paths):
        X = []
        Y = []
        for path in paths:
            subdf = pd.read_csv(path, compression='gzip')
            X.append(self.extractAggregatedFeatures(
                subdf[self.fields][-self.predictionPeriod - self.observationPeriod:-self.predictionPeriod]))
            l = 1 if "failed" in path else 0
            Y.append(l)
        return X,Y

    def evaluateAggregated(self):
        t0 = time.time()
        X,Y = self.extractAllAggregatedFeatures(self.trainDatasetPaths)
        self.aggregatedFeatureExtractionTime = time.time() - t0
        clfs = [("SVM", SVC()), ("Random Forest", RandomForestClassifier()),
                ("1NN", KNeighborsClassifier(n_neighbors=1))]
        for name,clf in clfs:
            scores = cross_val_score(clf, X, Y, cv=self.NUM_CROSS_VAL, n_jobs=-1)
            print name, scores.mean()
            clf.fit(X, Y)
        self.aggregatedTrainTime = time.time() - self.aggregatedFeatureExtractionTime
        self.aggregatedClfs = clfs
        X_test,Y_test = self.extractAllAggregatedFeatures(self.testDatasetPaths)
        for name, clf in clfs:
            pred = clf.predict(X_test)
            m = confusion_matrix(Y_test, pred)
            self.aggregatedConfMatrix.append((name, m))
            print name, m
            print classification_report(Y_test, pred)
            print "expected", Y_test
            print "actual", pred,"\n"
        return clfs

    def save(self):
        with open(Experiment.resultsPath + "experiment_%s.pkl" % self.counter, 'wb') as f:
            pickle.dump(self, f)


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
    observationPeriods = [10]
    predictionPeriods = [1]
    trainDatabase, testDatabase = paths[:int(len(paths) * 0.8)], paths[int(len(paths) * 0.8):]
    print "Train Size: %s sequences\t Test Size: %s sequences" % (len(trainDatabase), len(testDatabase))
    # writeHeader()
    counter = 0
    NUMBER_OF_SHAPELETS = 100
    for obsPeriod in observationPeriods:
        for predPeriod in predictionPeriods:
            e = Experiment(trainDatabase, testDatabase, obsPeriod, predPeriod, NUMBER_OF_SHAPELETS)
            e.evaluateShapelets()
            e.evaluateAggregated()
            e.writeExperiment()
            e.save()
            # t0 = time.time()
            # D = Dataset(trainDatabase, fields, obsPeriod, predPeriod)
            # min_len, max_len = EstimateMinAndMax(D)
            # print "Using observation period: %s\t prediction period: %s\nmin shapelet length: %s\tmax shapelet length: %s" % (
            #     obsPeriod, predPeriod, min_len, max_len)
            # shapelets = FindKShapelet(D, NUMBER_OF_SHAPELETS, min_len, max_len)
            # took = time.time() - t0
            # with open("experiment_%s.pkl" % counter, 'wb') as f:
            #     pickle.dump(shapelets, f)
            # print "Took %s" % (took)
            # writeExperiment(counter, trainDatabase, testDatabase, len(trainDatabase), len(testDatabase), obsPeriod,
            #                 predPeriod, min_len, max_len, took)
            counter += 1
