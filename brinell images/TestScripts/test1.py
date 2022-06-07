import cv2
import os
from cv2 import minAreaRect
import numpy as np
import math
import imutils
import datetime
from scipy.spatial import distance as dist

def getPercentageError(orginalHB,calculatedHB):
    return ((calculatedHB-orginalHB)/(orginalHB))*100

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
    
    "C:/Aditya/Assignments/Sem6/MP4/Repository/MP-4/Camera2 Images/1"

]
givenHB = [99.6]
givenwt = [62.5]
givenDD = [2.5]
i=0 
sum = 0
ecnt = 0
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
            tmpImg = originalImg
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

            maxArea = 0
            j=0
            pos = 0
                    
                
            
            j=0
            a = 0
            for c in contours:
                if cv2.contourArea(c) < 100:
                    continue
                originalImg = tmpImg
                #print(c[1])
                #print("Area Of Contour",cv2.contourArea(c))
                # (x,y),radius = cv2.minEnclosingCircle(c)
                # center = (int(x),int(y))
                # # r = int(radius)
                # cv2.circle(originalImg,center,r,(0,255,0),2)

                # name = './Result/IMGRes' +str(cnt) +'.jpg'
                # cnt += 1
                # cv2.imwrite(str(name),originalImg)
                
                box = cv2.minAreaRect(c)
                box = cv2.boxPoints(box)
                # print(box)
                
               
                


                #print("Co-ordinates of Rectangle",box)
                cX = np.average(box[:,0])
                #print(cX)
                cY = np.average(box[:,1])
                r = math.sqrt((cX-c[4][0][0])**2 + (cY-c[4][0][1])**2)
                Diameter_pixels = 2*r
                # print("Diameter in pixels:",Diameter_pixels)
                reference_mm_per_pixels = 0.01625
                # reference_mm_per_pixels = 0.01606
                Diameter_mm = reference_mm_per_pixels * Diameter_pixels
                # print("Diameter in mm:",Diameter_mm)
                HB = calculate_HB(givenwt[i],float(givenDD[i]),Diameter_mm)
                HB = round(HB,4)
                error = round(getPercentageError(givenHB[i],HB),4)
                #print("HB:",HB)
                
                

# 0.8694 mm


                if(error<2):
                    ecnt +=1 


                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                (tl, tr, br, bl) = box
                (tltrX, tltrY) = midpoint(tl, tr)
                (blbrX, blbrY) = midpoint(bl, br)
                


                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)
                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                if(Diameter_pixels<95 and Diameter_pixels>70):
                    cnt += 1
                    sum +=Diameter_pixels
                    print(givenHB[i],'    ',HB,'        ',error, '        ',cv2.contourArea(c),'          ',filename,'    ',a,'           ',Diameter_pixels)
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
                cv2.putText(originalImg, str(a),
                (int(tltrX+15), int(tltrY+20)), cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0, 0, 255),2)
                a +=1
                # cv2.imshow('Res',originalImg)
                 
                name = './Result/' +str(cnt) +'.jpg'
                
                cv2.imwrite(str(name),originalImg)

                cv2.waitKey(0)
                j += 1
                
        else:
            continue
    
print('Error Count : ',ecnt,'/40')
print("AVG : ",sum/cnt)
    
