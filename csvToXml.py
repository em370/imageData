import numpy
import glob
import sys

fileConvertPath = 'C:/Users/Eric Minor/TrackingML/defectTracker/ImageAnnotation'

mainDir = 'C:/Users/Eric Minor/TrackingML/imageData/annotations/csv'
#outDir = os.path.join(os.getcwd(),'accumulated');


sys.path.append(fileConvertPath)
from fileConvertBatch import fileConvertBatch
fileConvertBatch(mainDir,[200,200])