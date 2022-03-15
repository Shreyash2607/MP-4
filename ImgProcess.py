import cv2
import os
from cv2 import minAreaRect
import numpy as np
import math
import imutils
import datetime


#Function to calculate Percentage Error
def getPercentageError(orginalHB,calculatedHB):
    return (abs(calculatedHB-orginalHB)/(orginalHB))*100

#Function to caluculate HB
def calculate_HB(P,D,d):
    num = 2*P
    if(D>d):
        den = 3.14*D*(D-math.sqrt((D*D) - (d*d)))
        return num/den
    else:
        return 0

#Function to get midpoint
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

#Function to get Diameter
def getDiameter():

    #Local Directories
    directories = [
        'C:/Aditya/Assignments/Sem6/MP4/Script/brinell images/2.5_62.5_99.6HBW',
        'C:/Aditya/Assignments/Sem6/MP4/Script/brinell images/2.5_187.5_198.6HBW/',
        'C:/Aditya/Assignments/Sem6/MP4/Script/brinell images/5_750_200.4HBW/',
        'C:/Aditya/Assignments/Sem6/MP4/Script/brinell images/10_3000_220BHN/'

    ]

    #User Inputs
    givenHB = [99.6,198.6,200.4,220]
    givenwt = [62.5,187.5,750,3000]
    givenDD = [2.5,2.5,5,10]
    diameterVal = [0.8694,1.069,2.1115,4.0783]
    caliberationVal = [54.115386,73.27161,155.26079,299.87802]

    #Counter Variables
    i=0 
    cnt = 0
    ecnt = 0

    #Iterating Over All Folders
    for directory in directories:
        
        print('\n'+ directory + '\n') 
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                
                input_path = os.path.join(directory, filename)
                path = "./brinell images/" + str(filename)
                
                image = cv2.imread(input_path)
                originalImg = image
                
                #Gray Image Conversion
                grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                grayImage = cv2.GaussianBlur(grayImage, (7, 7), 0)
                
                #Thresholding and InverseThresholding
                ret,thresholdImage = cv2.threshold(grayImage,80,255,cv2.THRESH_BINARY)
                ret,inverseThresholdImage = cv2.threshold(grayImage,80,255,cv2.THRESH_BINARY_INV)
                
                #Finding Contours
                contours,heirarchy = cv2.findContours(inverseThresholdImage, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
                mask = np.zeros(inverseThresholdImage.shape, np.uint8)

                #Drawing Contors
                contourImage = cv2.drawContours(mask, contours,-1, (255,255,0), 3)
                duplicateImg = contourImage
                name = './Result/CountourImage/' +str(filename) +'.jpg'
                cv2.imwrite(str(name),duplicateImg)
        

                maxArea = 0
                j=0
                pos = 0
                #Finding Max Area Contour
                for c in contours:
                    if(maxArea < cv2.contourArea(c)):
                        maxArea = cv2.contourArea(c)
                        pos = j
                    j +=1

                        
                    
                #Iterating Over All Contors
                j=0
                for c in contours:
                    if pos!=j:
                        j+=1
                        continue
                    
                    #Calculating Radius Using Box Method
                    box = cv2.minAreaRect(c)
                    box = cv2.boxPoints(box)

                    cX = np.average(box[:,0])
                    cY = np.average(box[:,1])

                    r = math.sqrt((cX-c[4][0][0])**2 + (cY-c[4][0][1])**2)
                    Diameter_pixels = 2*r
                   
                    #Caliberation Value Inputed By User
                    caliberationValue = caliberationVal[i]

                    #Diamter Value Calculated Using Formula 
                    diameterValue = diameterVal[i]

                    reference_mm_per_pixels = diameterValue/caliberationValue
                    
                    #Conversion of Diameter in mm 
                    Diameter_mm = reference_mm_per_pixels * Diameter_pixels
                    
                    #Calculating HB
                    HB = calculate_HB(givenwt[i],float(givenDD[i]),Diameter_mm)
                    HB = round(HB,4)

                    #Finding Percentage Error
                    error = round(getPercentageError(givenHB[i],HB),4)
                    
                    #Printing Result in Form of Table
                    if(error<20): 
                        print(givenHB[i],'    ',HB,'        ',error, '        ',cv2.contourArea(c),'          ',filename,'     ')
                   

                    #Counting Error Values
                    if(error>3):
                        ecnt +=1 


                    box = cv2.minAreaRect(c)
                    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                    box = np.array(box, dtype="int")

                    #Finding Midpoints of side of Box
                    (tl, tr, br, bl) = box
                    (tltrX, tltrY) = midpoint(tl, tr)
                    (blbrX, blbrY) = midpoint(bl, br)
                    (tlblX, tlblY) = midpoint(tl, bl)
                    (trbrX, trbrY) = midpoint(tr, br)

                    # draw the midpoints on the image
                    cv2.drawContours(originalImg, [box.astype("int")], -1, (0, 255, 0), 2)
                    
                    #Looping over the original points and draw them
                    for (x, y) in box:
                        cv2.circle(originalImg, (int(x), int(y)), 5, (0, 0, 255), -1)

                    #Drawing Cicle by joining points 
                    cv2.circle(originalImg, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                    cv2.circle(originalImg, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                    cv2.circle(originalImg, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                    cv2.circle(originalImg, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

                    #Drawing lines between the midpoints
                    cv2.line(originalImg, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                        (0, 255, 0))
                    cv2.line(originalImg, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                        (0, 255, 0))
                    cv2.putText(originalImg, "{:.2f}mm".format(Diameter_mm),
                    (int(tltrX+15), int(tltrY+20)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 0, 255),2)
                    
                    
                    #Storing Result Image
                    name = './Result/IMGRes' +str(cnt) +'.jpg'
                    cnt += 1
                    #cv2.imwrite(str(name),originalImg)

                    cv2.waitKey(0)
                    j += 1
                    
            else:
                continue
        i+=1

    #Error Count and Average    
    print('Error Count : ',ecnt)
    



getDiameter()
