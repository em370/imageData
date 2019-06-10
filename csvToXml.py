import numpy
import glob
import sys

fileConvertPath = 'E:/Projects/fake/defectTracker/ImageAnnotation'

mainDir = 'E:/Projects/fake/imageData/annotations/csv'
#outDir = os.path.join(os.getcwd(),'accumulated');


sys.path.append(fileConvertPath)
from fileConvertBatch import fileConvertBatch
fileConvertBatch(mainDir,[200,200])