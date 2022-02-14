import cv2
import os
from cv2 import minAreaRect
import numpy as np
import math
# from imutils import perspective
# from imutils import contours
import imutils
import datetime


def getPercentageError(orginalHB,calculatedHB):
    return (abs(calculatedHB-orginalHB)/(orginalHB))*100

def calculate_HB(P,D,d):
    num = 2*P
    if(D>d):
        den = 3.14*D*(D-math.sqrt((D*D) - (d*d)))
        return num/den
    else:
        return 0

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# load the image, convert it to grayscale, and blur it slightly

directories = [
    'C:/Aditya/Assignments/Sem6/MP4/Script/brinell images/2.5_62.5_99.6HBW',
    'C:/Aditya/Assignments/Sem6/MP4/Script/brinell images/2.5_187.5_198.6HBW/',
    'C:/Aditya/Assignments/Sem6/MP4/Script/brinell images/5_750_200.4HBW/',
    'C:/Aditya/Assignments/Sem6/MP4/Script/brinell images/10_3000_220BHN/'

]
givenHB = [99.6,198.6,200.4,220]
givenwt = [62.5,187.5,750,3000]
givenDD = [2.5,2.5,5,10]
i=0 
cnt = 0
for directory in directories:
    
    print('\n'+ directory + '\n') 
    

    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            input_path = os.path.join(directory, filename)
            path = "./brinell images/" + str(filename)
            #print(path)
            image = cv2.imread(input_path)
            originalImg = image
            #cv2.imshow("initial image",image)
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            grayImage = cv2.GaussianBlur(grayImage, (7, 7), 0)
            ret,thresholdImage = cv2.threshold(grayImage,80,255,cv2.THRESH_BINARY)
            #cv2.imshow("Thresholded image",thresholdImage)

            ret,inverseThresholdImage = cv2.threshold(grayImage,80,255,cv2.THRESH_BINARY_INV)
            # cv2.imshow("Inverse Thresholded image",inverseThresholdImage)

            contours,heirarchy = cv2.findContours(inverseThresholdImage, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
           
            mask = np.zeros(inverseThresholdImage.shape, np.uint8)
            contourImage = cv2.drawContours(mask, contours,-1, (255,255,0), 3)
            # cv2.imshow("Contour Image",contourImage)

            duplicateImg = contourImage
            name = './Result/CountourImage/' +str(filename) +'.jpg'
            cv2.imwrite(str(name),duplicateImg)
            #cv2.drawContours(inverseThresholdImage, contours, -1, (255, 255, 0), 6)
            #cv2.imshow("Countors",inverseThresholdImage)
            #print(contours)
            
                


            for c in contours:
                if cv2.contourArea(c) < 2000:
                    continue
                #print(c[1])
                #print("Area Of Contour",cv2.contourArea(c))
                box = cv2.minAreaRect(c)
                box = cv2.boxPoints(box)
                #print("Co-ordinates of Rectangle",box)
                cX = np.average(box[:,0])
                #print(cX)
                cY = np.average(box[:,1])
                r = math.sqrt((cX-c[4][0][0])**2 + (cY-c[4][0][1])**2)
                Diameter_pixels = 2*r
                #print("Diameter in pixels:",Diameter_pixels)
                reference_mm_per_pixels = 0.0136
                Diameter_mm = reference_mm_per_pixels * Diameter_pixels
                #print("Diameter in mm:",Diameter_mm)
                HB = calculate_HB(givenwt[i],float(givenDD[i]),Diameter_mm)
                HB = round(HB,4)
                #print("HB:",HB)
                print(givenHB[i],'    ',HB,'        ',round(getPercentageError(givenHB[i],HB),4), '        ',cv2.contourArea(c),'          ',filename)

                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                (tl, tr, br, bl) = box
                (tltrX, tltrY) = midpoint(tl, tr)
                (blbrX, blbrY) = midpoint(bl, br)


                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)
                # draw the midpoints on the image
                cv2.drawContours(originalImg, [box.astype("int")], -1, (0, 255, 0), 2)
	        # loop over the original points and draw them
                for (x, y) in box:
                    cv2.circle(originalImg, (int(x), int(y)), 5, (0, 0, 255), -1)

                cv2.circle(originalImg, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                cv2.circle(originalImg, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                cv2.circle(originalImg, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                cv2.circle(originalImg, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

                # draw lines between the midpoints
                
                cv2.line(originalImg, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                    (0, 255, 0))
                cv2.line(originalImg, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                    (0, 255, 0))
                cv2.putText(originalImg, "{:.2f}mm".format(Diameter_mm),
                (int(tltrX+15), int(tltrY+20)), cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0, 0, 255),2)
                # cv2.imshow('Res',originalImg)
                 
                name = './Result/IMGRes' +str(cnt) +'.jpg'
                cnt += 1
                cv2.imwrite(str(name),originalImg)

                cv2.waitKey(0)
                
        else:
            continue
    
    i = i+1
