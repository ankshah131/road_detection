import cv2
import os

import matplotlib.pyplot as plt
import numpy as np
import skimage

from matplotlib import cm
from Phase_Congruency import phasecongmono
from PIL import Image
from skimage import feature, morphology
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.transform import probabilistic_hough_line


FOLDER = 'LA_12_12_2019'
PATH = 

def phase_output(root_path, contrail_img):
    """
    This function returns the phase congruency output with a grayscale image as the input with its root path.
	Phase congruency is a method of edge detection which detects edges irrespective of the brightness of 
	features. The strength of edge detection can be adjusted by changing the dependent values in phasecongmono.
	The final image is converted into a uint8 format to be read by OpenCV2. 
    """
    image_path = {PATH}
    road_img = cv2.imread(image_path)
    # grayscale using skimage
    road_gray = rgb2gray(road_img)
    # Adjust gamma stretch threshold
    contrast_img = skimage.exposure.adjust_gamma(road_gray, gamma=3.8, gain=1)

    # Image thresholding using global threshold
    thresh = threshold_otsu(contrast_img)

    # Keeping values above threshold the same whereas below threshold are 0.
    contrast_img[contrast_img < thresh] = 0

    # Change the parameters nscale and minWaveLength for detecting smaller or larger objects respectively
    phaseimg = phasecongmono(
        road_gray,
        nscale=5,
        minWaveLength=3,  # 3 is the default
        mult=2.5,  # 2.1 is the default
        sigmaOnf=0.55,
        k=15.0,
        cutOff=0.8,
        g=10.0,
        noiseMethod=-1,
        deviationGain=1.5,
    )
    # Parsing the phase output tuple of arrays
    phasecong0 = phaseimg[0]

    # Converting phasecong0 to uint8
    phasecong0_binary = (phasecong0 / (np.max(phasecong0))) * 255
    phasecong0_close = (np.round(phasecong0_binary)).astype(np.uint8)
    cv2.imwrite(f"{root_path}/{PHASECONG}", phasecong0_close)


if __name__ == "__main__":
    # 	for root, dirs, files in os.walk(GRANULES_FOLDER):
    for root, dirs, files in os.walk(f"{FOLDER}"):
        if TIF_WINDOW_FILE in files:
            phase_output(root, TIF_WINDOW_FILE)

