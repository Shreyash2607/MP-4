import cv2
from cv2 import minAreaRect
import numpy as np
import math
import imutils
from scipy.spatial import distance as dist
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

def single(input,calibration,output,diameter_of_indenter,applied_load,HB_value,method,lower,upper):
    image = cv2.imread(input)
    originalImg = image
    aoriginalImg = image
    calibration = float(calibration)
    ecnt = 0
    #Gray Image Conversion
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayImage = cv2.GaussianBlur(grayImage, (7, 7), 0)
    
    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    #edged = cv2.Canny(grayImage, 50, 100)
    #edged = cv2.dilate(edged, None, iterations=1)
    #edged = cv2.erode(edged, None, iterations=1)
    #Thresholding and InverseThresholding
    ret,thresholdImage = cv2.threshold(grayImage,80,255,cv2.THRESH_BINARY)
    ret,inverseThresholdImage = cv2.threshold(grayImage,80,255,cv2.THRESH_BINARY_INV)
    
    #Finding Contours
    contours,heirarchy = cv2.findContours(inverseThresholdImage, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #contours= cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #contours = imutils.grab_contours(contours)
    #mask = np.zeros(inverseThresholdImage.shape, np.uint8)

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    #(contours, _) = contours.sort_contours(contours)
    #Drawing Contors
    #contourImage = cv2.drawContours(mask, contours,-1, (255,255,0), 3)
    #1. duplicateImg = contourImage
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
        if cv2.contourArea(c)<3000:
            continue
        #print(cnt, '  ',str(cv2.contourArea(c)))
        #Calculating Radius Using Box Method
        #if(cv2.contourArea(c)==166169.5):
        else:
            if(method=='circle'):
                (x,y),radius = cv2.minEnclosingCircle(c)
                center = (int(x),int(y))
                radius = int(radius)
                centerx = x 
                centery = y
                cv2.circle(originalImg,center,radius,(0,255,0),2)
                cv2.putText(originalImg, str(cnt),(int(x + 120), int(y + 200)), cv2.FONT_HERSHEY_SIMPLEX,0.9, (0, 0, 255),2)

                D=2*radius
                Diameter_pixels = D
                calibrationN= calibration
                Diameter_mc = Diameter_pixels *calibrationN
                Diameter_ma = Diameter_mc
                Diameter_mb = Diameter_mc
                
                #Calculating HB
                HB = calculate_HB(applied_load,diameter_of_indenter,Diameter_mc)
                if HB is -1:
                    continue
                HB = round(HB,4)

                                    #Finding Percentage Error
                error = round(getPercentageError(HB_value,HB),4)
                    
                            #Printing Result in Form of Table
                if(error<100): 
                    #print(Diameter_pixels)
                    #print(Diameter_mc)
                    #print(radius*2*calibrationN)
                    #print(box)
                    status="Not ACCEPT"
                    if HB>lower and HB<upper:
                        status ="ACCEPT"
                    print(HB_value,'    ',HB,'        ',error,'         ',status)
                    # cv2.drawContours(originalImg, [box.astype("int")], 0, (0, 0, 255), 2)
                    #         #Drawing Cicle by joining points 
                    # cv2.circle(originalImg, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                    # cv2.circle(originalImg, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                    # cv2.circle(originalImg, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                    # cv2.circle(originalImg, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

                    # cv2.line(originalImg, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(0, 255, 0))
                    # cv2.line(originalImg, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(0, 255, 0))
                    # cv2.putText(originalImg, "{:.1f}mm".format(Diameter_mc),(int(centerx - 15), int(center - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
                    # cv2.putText(originalImg, "{:.1f}mm".format(Diameter_mc),(int(centerx + 10), int(centery)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)            
                    # cv2.putText(originalImg, str(cnt),(int(tltrX + 120), int(tlblY + 200)), cv2.FONT_HERSHEY_SIMPLEX,0.9, (0, 0, 255),2)
                    # cv2.putText(originalImg, str(HB),(int(tltrX + 180), int(tlblY + 200)), cv2.FONT_HERSHEY_SIMPLEX,0.9, (255, 0, 0),2)


            else:
                            box = cv2.minAreaRect(c)
                            box = cv2.boxPoints(box)

                            cX = np.average(box[:,0])
                            cY = np.average(box[:,1])
                            #radius = math.sqrt((cX-c[4][0][0])**2 + (cY-c[4][0][1])**2)
                            box = cv2.minAreaRect(c)
                            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                            #box = np.array(box, dtype="float")
                            box = np.int64(box)

                            #Finding Midpoints of side of Box
                            (tl, tr, br, bl) = box
                            (tltrX, tltrY) = midpoint(tl, tr)
                            (blbrX, blbrY) = midpoint(bl, br)
                            (tlblX, tlblY) = midpoint(tl, bl)
                            (trbrX, trbrY) = midpoint(tr, br)
                            centerx = tlblX
                            centery = tlblY     
                            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                            D = (dB+dA)/2
                            Diameter_pixels = D
                            calibrationN= calibration
                            Diameter_mc = Diameter_pixels *calibrationN
                            Diameter_ma = Diameter_mc
                            Diameter_mb = Diameter_mc
                            #Calculating HB
                            HB = calculate_HB(applied_load,diameter_of_indenter,Diameter_mc)
                            if HB is -1:
                                continue
                            HB = round(HB,4)

                                    #Finding Percentage Error
                            error = round(getPercentageError(HB_value,HB),4)
                    
                            #Printing Result in Form of Table
                            if(error<10): 
                                #print(HB_value,'    ',HB,'        ',error, '        ',cv2.contourArea(c),'     ',cnt)
                                #print(Diameter_pixels)
                                #print(Diameter_mc)
                                #print(radius*2*calibrationN)
                                #print(box)
                                status="Not ACCEPT"
                                if HB>lower and HB<upper:
                                    status ="ACCEPT"
                                print(HB_value,'    ',HB,'        ',error,'         ',status)
                                cv2.drawContours(originalImg, [box.astype("int")], 0, (0, 0, 255), 2)
                                #Drawing Cicle by joining points 
                                cv2.circle(originalImg, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                                cv2.circle(originalImg, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                                cv2.circle(originalImg, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                                cv2.circle(originalImg, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

                                cv2.line(originalImg, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(0, 255, 0))
                                cv2.line(originalImg, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(0, 255, 0))
                                cv2.putText(originalImg, "{:.1f}mm".format(Diameter_mc),(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
                                cv2.putText(originalImg, "{:.1f}mm".format(Diameter_mc),(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)            
                                cv2.putText(originalImg, str(cnt),(int(tltrX + 120), int(tlblY + 200)), cv2.FONT_HERSHEY_SIMPLEX,0.9, (0, 0, 255),2)
                                cv2.putText(originalImg, str(HB),(int(tltrX + 180), int(tlblY + 200)), cv2.FONT_HERSHEY_SIMPLEX,0.9, (255, 0, 0),2)
    
        
        #Storing Result Image
        name = './Result/Single/'+output 
        cnt += 1
        # cv2.imwrite(str(name),originalImg)
        cv2.imshow("Show",originalImg)
        cv2.waitKey(0)
        j += 1

