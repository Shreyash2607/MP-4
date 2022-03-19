import cv2
from cv2 import minAreaRect
import numpy as np
import math

def calculate_HB(P,D,d):
    num = 2*P
    den = 3.14*D*(D-math.sqrt(D*D - d*d))
    return num/den

def single(input_path,calibration,output_path,diameter_of_indenter,applied_load):
    # load the image, convert it to grayscale, and blur it slightly
    print(type(calibration))
    reference_mm_per_pixels = float(calibration)
    image = cv2.imread(input_path)
    cv2.imshow("initial image",image)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayImage = cv2.GaussianBlur(grayImage, (7, 7), 0)
    ret,thresholdImage = cv2.threshold(grayImage,80,255,cv2.THRESH_BINARY)
    #cv2.imshow("Thresholded image",thresholdImage)

    ret,inverseThresholdImage = cv2.threshold(grayImage,80,255,cv2.THRESH_BINARY_INV)
    cv2.imshow("Inverse Thresholded image",inverseThresholdImage)

    contours,heirarchy = cv2.findContours(inverseThresholdImage, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))
    #print(len(contours1))
    mask = np.zeros(inverseThresholdImage.shape, np.uint8)
    contourImage = cv2.drawContours(mask, contours,-1, (255,255,0), 3)
    cv2.imshow("Contour Image",contourImage)
    #cv2.drawContours(inverseThresholdImage, contours, -1, (255, 255, 0), 6)
    #cv2.imshow("Countors",inverseThresholdImage)
    #print(contours)

    for c in contours:
        if cv2.contourArea(c) < 100:
            continue
        print(c[1])
        print("Area Of Contour",cv2.contourArea(c))
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box)
        print("Co-ordinates of Rectangle",box)
        cX = np.average(box[:,0])
        print(cX)
        cY = np.average(box[:,1])
        r = math.sqrt((cX-c[4][0][0])**2 + (cY-c[4][0][1])**2)
        Diameter_pixels = 2*r
        print("Diameter in pixels:",Diameter_pixels)
        print(type(Diameter_pixels))
        Diameter_mm = reference_mm_per_pixels * Diameter_pixels
        print("Diameter in mm:",Diameter_mm)
        HB = calculate_HB(applied_load,diameter_of_indenter,Diameter_mm)
        print("HB:",HB)

    cv2.imwrite(output_path + "1.jpg",contourImage)
    cv2.waitKey(0)

