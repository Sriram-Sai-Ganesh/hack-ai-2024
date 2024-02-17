import skimage
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
import opencv
import scipy

#Determines how to binarize data
#Assumes images is between [0,1] and grayscale
THRESHOLD = 0.95
TOLERANCE = 0.05
#Potential problem: need to detect if image is [0,1] or [0,255]
def binarize(Im,rgb=True):
    grayIm = skimage.color.rgb2gray(Im[:,:,0:3])
    return grayIm

#Detects information about dividers
def divider_info(Im):
    #detection method: sum each row. Rows that are mostly pixels are dividers
    density = (Im.shape[1]-np.sum(Im,axis=1))/Im.shape[1]
    #The maximum density is going to be a divider
    divider_density = np.max(density)
    #Detect which lines are close to the max density, within a tolerance
    compare = np.full((density.shape),divider_density)
    dividers = np.isclose(density,compare,rtol=TOLERANCE)
    #Get indices of dividers and use to find info
    divider_indices = np.argwhere(dividers)
    divider_indices = divider_indices[:,0]
    print(divider_indices)
    divider_indices = divider_indices + np.array([[0],[1]])
    print(divider_indices)
    return divider_indices

#Segments horizontal lines and returns an array of lines
def segment_lines(Im):
    indices = divider_info(Im)
    segments = np.split(Im,indices[:,0])
    lines = segments[::2]
    return lines

def CC(Im):
    from skimage.measure import label, regionprops, regionprops_table
    labels = label(Im,background=1)
    regions = regionprops(labels)
    largest_region = regions[0].image
    io.imshow(largest_region, cmap='gray'); io.show()

def main():
    test = io.imread('White_Data.png')
    bin = binarize(test)>THRESHOLD
    lines = segment_lines(bin)
    io.imshow(lines[1],cmap='gray'); io.show()
    CC(lines[1])
    #io.imshow(bin); io.show()
    return 0

if __name__=="__main__": 
    main() 