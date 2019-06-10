import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pprint as pp
import numpy as np
from PIL import Image
import glob
import os
from scipy import fftpack
import matplotlib.patches as patches
from pims import ImageSequence


def plot_spectrum(im_fft):
    from matplotlib.colors import LogNorm

    
    plt.imshow(np.abs(im_fft), norm = LogNorm (vmin =5))
    plt.colorbar()
    plt.title('Fourier transform')
    
def standardize(image):
    image = image.astype(np.float64)
    imgMean = np.mean(image)
    imgSTD = np.std(image)
    image= (image - imgMean)/(6*imgSTD)
    image = image+0.5
    #image = image*255
    image = np.clip(image,0,1)
    return image
def standardizeCropped(image,croppedImg):
    image = image.astype(np.float64)
    croppedImg = croppedImg.astype(np.float64)
    imgMean = np.mean(croppedImg)
    imgSTD = np.std(croppedImg)
    image= (image - imgMean)/(6*imgSTD)
    image = image+0.5
    #image = image*255
    image = np.clip(image,0,1)
    return image



class getter:
    def __init__(self,ax,fig):

        self.numClicks = 0
        self.x = [0,0]
        self.y = [0,0]
        self.ax = ax
        self.fig = fig
        self.figsize = fig.get_size_inches()*fig.dpi
        self.rect = patches.Rectangle((1,1),0,0,linewidth=1,edgecolor='r',facecolor='none')
        self.ax.add_patch(self.rect)
        self.fig.canvas.mpl_connect('button_press_event',self.click)
        self.fig.canvas.mpl_connect('motion_notify_event',self.move)
        #print(self.figsize)

    def click(self,event):
        #print(event.xdata,event.ydata)
        self.x[self.numClicks] = event.xdata
        self.y[self.numClicks] = event.ydata
        #print(self.x)
        if self.numClicks > 0:
            plt.close()
        self.numClicks = self.numClicks+1
    def move(self,event):
        if self.numClicks >0:
            mouseX = event.xdata
            mouseY = event.ydata
            if mouseX is not None:
                clickX = self.x[0]
                clickY = self.y[0]

                xsort = [mouseX,clickX]
                ysort = [mouseY,clickY]
                xsort.sort()
                ysort.sort()

                dif = min(xsort[1]-xsort[0],ysort[1]-ysort[0])

                #print(xsort)
                #print(ysort)
                self.rect.remove()
                self.rect = patches.Rectangle((xsort[0],ysort[0]),dif,dif,linewidth=1,edgecolor='r',facecolor='none')
                self.ax.add_patch(self.rect)
                self.fig.canvas.draw()


targetDir = os.path.join(os.getcwd(),'annotations')
ext = 'tif'
outDir = targetDir+"\\corrected\\"
fullImg = 1
if not os.path.exists(outDir):
    os.makedirs(outDir)

filePattern = 	targetDir+"\\*." + ext
first = 1  
for filename in glob.glob(filePattern):
    
    #imgcv = cv2.imread(filename)
    images = ImageSequence(filename)
    imgcv = images[0]
    print(imgcv.dtype)
    fig,ax = plt.subplots()
    imgplot = ax.imshow(imgcv)
    sections = filename.split("\\")
    imName = sections[-1]
    
    #im.save(outDir+imName)
    
    #print(result)
    prePost = imName.split(".")
    noEnd = prePost[0]

    if first == 1:
        getter1 = getter(ax,fig)
        #fig.canvas.mpl_connect('button_press_event',onclick)
        plt.show()

        x = getter1.x
        y = getter1.y

        x.sort()
        y.sort()



        for i in range(0,len(x)):
            x[i] = int(x[i])

        for i in range(0,len(y)):
            y[i] = int(y[i])
        first = 0


    croppedImg = imgcv[y[0]:y[1],x[0]:x[1]]

    outImg = standardizeCropped(imgcv,croppedImg)
    outImg = outImg*256
    outImg = outImg.astype(np.uint8)

    im = Image.fromarray(outImg)
    im.save(outDir+imName)
    #fig,ax = plt.subplots()
    #imgplot = ax.imshow(croppedImg)
    #plt.show()
