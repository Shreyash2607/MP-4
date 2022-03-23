import cv2
from cv2 import minAreaRect
import numpy as np
import math
import imutils

#Function to get midpoint
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def getPercentageError(orginalHB,calculatedHB):
    return (abs(calculatedHB-orginalHB)/(orginalHB))*100

def calculate_HB(P,D,d):
    if d>D:
        return -1
    num = 2*P
    den = 3.14*D*(D-math.sqrt(D*D - d*d))
    return num/den

def single(input,calibration,output,diameter_of_indenter,applied_load,HB_value,method,std_mean_diameter):
    image = cv2.imread(input)
    originalImg = image
    calibration = float(calibration)
    ecnt = 0
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
    # name = './Result/CountourImage/' +str(fi) +'.jpg'
    # cv2.imwrite(str(name),duplicateImg)


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
    cnt = 0
    for c in contours:
        if cv2.contourArea(c)<100:
            continue
        
        #Calculating Radius Using Box Method
        if(method=='Circle'):
            (x,y),radius = cv2.minEnclosingCircle(c)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(originalImg,center,radius,(0,255,0),2)
            centerx = x 
            centery = y
            
        else:
            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box)

            cX = np.average(box[:,0])
            cY = np.average(box[:,1])
            radius = math.sqrt((cX-c[4][0][0])**2 + (cY-c[4][0][1])**2)
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")

            #Finding Midpoints of side of Box
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)
            centerx = tlblX
            centery = tlblY

            # draw the midpoints on the image
            #cv2.drawContours(originalImg, [box.astype("int")], -1, (0, 255, 0), 2)
                #Looping over the original points and draw them
            # for (x, y) in box:
            #     cv2.circle(originalImg, (int(x), int(y)), 5, (0, 0, 255), -1)

            #Drawing Cicle by joining points 
            # cv2.circle(originalImg, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            # cv2.circle(originalImg, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            # cv2.circle(originalImg, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            # cv2.circle(originalImg, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

            # cv2.line(originalImg, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
            # (0, 255, 0))
            # cv2.line(originalImg, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
            # (0, 255, 0))
            

        Diameter_pixels = 2*radius
        
        #Caliberation Value Inputed By User
        caliberationValue = calibration

        #Diamter Value Calculated Using Formula 
        #diameterValue = diameter_calculated
        

        #reference_mm_per_pixels = diameterValue/caliberationValue
        #reference_mm_per_pixels = Diameter_pixels/caliberationValue
        reference_mm_per_pixels = caliberationValue/std_mean_diameter
        #Conversion of Diameter in mm 
        Diameter_mm = reference_mm_per_pixels * Diameter_pixels
        
        #Calculating HB
        HB = calculate_HB(applied_load,diameter_of_indenter,Diameter_mm)
        if HB is -1:
            continue
        HB = round(HB,4)

        #Finding Percentage Error
        error = round(getPercentageError(HB_value,HB),4)
        
        #Printing Result in Form of Table
        if(error<5): 
            print(HB_value,'    ',HB,'        ',error, '        ',cv2.contourArea(c),'     ',cnt)
            cv2.putText(originalImg, str(cnt),
            (int(tltrX + 120), int(tlblY + 200)), cv2.FONT_HERSHEY_SIMPLEX,
            0.9, (0, 0, 255),2)
            cv2.putText(originalImg, str(HB),
            (int(tltrX + 170), int(tlblY + 200)), cv2.FONT_HERSHEY_SIMPLEX,
            0.9, (255, 0, 0),2)

        #Counting Error Values
        if(error>3):
            ecnt +=1 


        #Drawing lines between the midpoints
        
        # cv2.putText(originalImg, str(cnt),
        #     (int(centerx + 15), int(centery + 20)), cv2.FONT_HERSHEY_SIMPLEX,
        #     0.9, (0, 0, 255),2)
        
        
        #Storing Result Image
        name = './Result/Single/'+output 
        cnt += 1
        cv2.imwrite(str(name),originalImg)

        cv2.waitKey(0)
        j += 1

