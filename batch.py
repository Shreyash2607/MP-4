#
import cv2
import os
from cv2 import minAreaRect
import numpy as np
import math
import imutils
import datetime
from scipy.spatial import distance as dist
centerx = 0
centery = 0
listA=[]
#Function to calculate Percentage Error
def getPercentageError(orginalHB,calculatedHB):
    return (abs(calculatedHB-orginalHB)/(orginalHB))*100
#Mean of observation
def Average(lst):
    #print(len(lst))
    return sum(lst) / len(lst)
#Function to caluculate HB
def calculate_HB(P,D,d):
    if d>D:
        return -1
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

def batch(input,calibration,output,diameter_of_indenter,applied_load,HB_value,method,lower,upper):

    calibration = float(calibration)
    #Local Directories
     # directories = [
     #     'H:/brinell images/MP-4/Camera2 Images/1',
     #     'H:/brinell images/MP-4/Camera2 Images/3',
     #     'H:/brinell images/MP-4/Camera2 Images/4'

     # ]
    directories = [input]


    #Counter Variables
    i=0 
    cnt = 0
    ecnt = 0

    #Iterating Over All Folders
    for directory in directories:
        
        print('\n'+ directory + '\n') 
        print("filename",'   ',"Diameter_p",'  ',"Diameter_mm",'     ',"Actual_HB",'    ',"Predi_HB",'        ',"Error",'         ',"status")
        for filename in os.listdir(directory):
            if filename.endswith(".tif"):
                
                input_path = os.path.join(directory, filename)
                #path = "./10-3000-288.4BHN/" + str(filename)
                
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
                #name = './Result/CountourImage/' +str(filename) +'.jpg'
                #cv2.imwrite(str(name),duplicateImg)
        

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
                    if(method=='circle'):
                        (x,y),radius = cv2.minEnclosingCircle(c)
                        center = (int(x),int(y))
                        radius = int(radius)
                        D=2*radius
                        # cv2.circle(originalImg,center,radius,(0,255,0),2)
                        # centerx = x 
                        # centery = y
                        
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
                    #
                   
                    #Caliberation Value Inputed By User
                    #caliberationValue = calibration
                    calibrationN= calibration
                    Diameter_mc = Diameter_pixels *calibrationN
                    Diameter_ma = Diameter_mc
                    Diameter_mb = Diameter_mc
                    #reference_mm_per_pixels = caliberationValue/std_mean_diameter
                    #Conversion of Diameter in mm
                    #Diameter_mm = reference_mm_per_pixels * Diameter_pixels
                    
                    #Conversion of Diameter in mm 
                    #Diameter_mm = reference_mm_per_pixels * Diameter_pixels
                    
                    #Calculating HB
                    Diameter_mc=float("{:.4f}".format(Diameter_mc))
                    HB = calculate_HB(applied_load,diameter_of_indenter,Diameter_mc)
                    if HB is -1:
                        continue
                    HB = round(HB,4)

                    #Finding Percentage Error
                    #error = round(getPercentageError(HB_value,HB),4)
                    error =abs(HB-HB_value)
                    #Printing Result in Form of Table
                    if(error<3):
                        #print(Diameter_pixels)
                        #print(Diameter_mc)
                        #print(radius*2*calibrationN)
                        # #print(box)
                        status="NA"
                        listA.append(HB)
                        if HB>lower and HB<upper:
                            status ="AC"
                            #listA.append(HB)
                        else:
                            cnt += 1
                        print(filename,'   ',"{:.3f}PX".format(Diameter_pixels),'    ',"{:.1f}mm".format(Diameter_mc),'     ',HB_value,'    ',"{:.2f}".format(HB),'        ',"{:.2f}mm".format(error),'         ',status) 
                        #print(HB_value,'    ',HB,'        ',error, '        ',cv2.contourArea(c),'     ',cnt)
                        # cv2.putText(originalImg, str(cnt),
                        # (int(centerx + 120), int(centery + 200)), cv2.FONT_HERSHEY_SIMPLEX,
                        #     0.9, (0, 0, 255),2)
                        # cv2.putText(originalImg, str(HB),
                        #     (int(centerx + 180), int(centery + 200)), cv2.FONT_HERSHEY_SIMPLEX,
                        #     0.9, (255, 0, 0),2)
                        #draw the midpoints on the image
                        cv2.drawContours(originalImg, [box.astype("int")], -1, (0, 255, 0), 2)
                         #Looping over the original points and draw them
                        for (x, y) in box:
                            cv2.circle(originalImg, (int(x), int(y)), 5, (0, 0, 255), -1)

                        #Drawing Cicle by joining points 
                        cv2.circle(originalImg, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                        cv2.circle(originalImg, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                        cv2.circle(originalImg, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                        cv2.circle(originalImg, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

                        cv2.line(originalImg, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                        (0, 255, 0))
                        cv2.line(originalImg, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                        (0, 255, 0))
                        name = output + filename
                        cv2.putText(originalImg, "{:.1f}mm".format(Diameter_pixels),(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
                        cv2.putText(originalImg, "{:.1f}mm".format(Diameter_pixels),(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)            
                        # cv2.putText(originalImg, str(cnt),(int(tltrX + 120), int(tlblY + 200)), cv2.FONT_HERSHEY_SIMPLEX,0.9, (0, 0, 255),2)
                        cv2.putText(originalImg, str(HB),(int(tltrX + 180), int(tlblY + 200)), cv2.FONT_HERSHEY_SIMPLEX,0.9, (255, 0, 0),2)
                        cv2.imwrite(str(name),originalImg)

                    #Counting Error Values
                     


                    #Drawing lines between the midpoints
                    
                    # cv2.putText(originalImg, str(cnt),
                    #     (int(centerx + 15), int(centery + 20)), cv2.FONT_HERSHEY_SIMPLEX,
                    #     0.9, (0, 0, 255),2)
                    
                    
                    #Storing Result Image
                    

                    cv2.waitKey(0)
                    j += 1
                    
            else:
                continue
        i+=1

    #Error Count and Average    
    #print('Error Count : ',ecnt)
    average = Average(listA)
    print(round(average, 2))
    print(round(abs(HB_value-average),2))
    