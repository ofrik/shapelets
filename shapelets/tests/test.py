__author__ = 'Ofri'

import glob
from shapelets import FindingShapeletBF,FindKShapelet,EstimateMinAndMax
from shapelets.models import Dataset

if __name__ == "__main__":
    paths = glob.glob("resources/*/*/*")
    D = Dataset(paths, ["smart_7_raw"],observationPeriod=10,predictionPeriod=1)
    print EstimateMinAndMax(D)
    # print FindKShapelet(D,100, 2, 10)
