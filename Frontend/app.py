from tkinter import N
import eel
import random
from datetime import datetime
import base64
import cv2
import toupcam
#import toupcam.camera
import logging
import os
import sys
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox
from ocv import MainWin
import base64
from camera import VideoCamera
from result import single
# from toupcamcamera import ToupcamVideoCamera
import pymongo
from PIL import Image
import io

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Qson2"]
mycol = mydb["single"]



#eel.init('web')

capFram = None

x=None
camFrame=None

@eel.expose
def saveRecord(caliberation,indentor,load,hbvalue,lowerRange,higherRange,filename,jobname,custname,custadd,res,testedby,witnessedby,aprovedby):
    # mydict = { "name": "John", "address": "Highway 37" }
    # x = mycol.insert_one(mydict)
    global camFrame
    f=None
    image_bytes = io.BytesIO()
    capFram.save(image_bytes, format='JPEG')

    image = {
    'image': image_bytes.getvalue()
    }
    if camFrame is not None:
        f=camFrame
    print("RESULT")
    print(caliberation,indentor,load,hbvalue,lowerRange,higherRange,filename,jobname,custname,custadd,res,testedby,witnessedby,aprovedby)
    resdict = {
    "filename":filename, 
    "jobname":jobname ,
    "customer-name":custname,
    "customer-address": custadd,
    "tested-by":testedby,
    "witnessed-by":witnessedby,
    "aprooved-by":aprovedby,
    "calculated-hb":res,
    "given-hb":hbvalue,
    "diameter-of-indentor":indentor,
    "caliberation-value":caliberation,
    "load":load,
    "lowerRange":lowerRange,
    "higherRange":higherRange,
    "date":datetime.now(),
    'image': image_bytes.getvalue()
    }
    x = mycol.insert_one(resdict)
    print(x.inserted_id)

@eel.expose
def getData():
    savedData = []
    k = mycol.find({}, { 'filename': 1 })
    print(k)
    for x in mycol.find({}, { 'filename': 1 ,"tested-by":1,"given-hb":1,"calculated-hb":1}):
        savedData.append(x)
    
    # image = images.find_one()

    # pil_img = Image.open(io.BytesIO(image['data']))
    # plt.imshow(pil_img)
    # plt.show()
    # print(savedData)
    return savedData





@eel.expose
def get_random_name():
    eel.prompt_alerts('Random name')


@eel.expose
def get_random_number():
    eel.prompt_alerts(random.randint(1, 100))



@eel.expose
def get_date():
    eel.prompt_alerts(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


@eel.expose
def getR():
    return 10

@eel.expose
def getResults(calibration,output,diameter_of_indenter,applied_load,HB_value,lower,upper):
    capFram = cv2.imread('0001.tif')
    res = single('0001.tif',float(calibration),output,float(diameter_of_indenter),float(applied_load),float(HB_value),'other',float(lower),float(upper))
    print("RESULT",res)
    return res



@eel.expose

def get_ip():
    eel.prompt_alerts('127.0.0.1')

def gen(camera):
    while True:
        frame = camera.get_frame()
        # if k%256 == 27:
        # # ESC pressed
        #     print("Escape hit, closing...")
        #     break
        # elif k%256 == 32:
        #     # SPACE pressed
        #     img_name = "opencv_frame_{}.png".format(img_counter)
        #     cv2.imwrite('1.png', frame)
        #     print("{} written!".format(img_name))
        #     img_counter += 1
        yield frame




@eel.expose
def video_feed():
    x = VideoCamera()
    y = gen(x)
    print("hi")
    for each in y:
        # Convert bytes to base64 encoded str, as we can only pass json to frontend
        blob = base64.b64encode(each)
        blob = blob.decode("utf-8")
       
        eel.updateImageSrc(blob)()
        # time.sleep(0.1)


@eel.expose
def toupcamvideo_feed(flg):
    global capFram
    if flg == 1:   
        x = VideoCamera()
        y = gen(x)
        print("hi")
        for each in y:
            # Convert bytes to base64 encoded str, as we can only pass json to frontend
            blob = base64.b64encode(each)
            blob = blob.decode("utf-8")
        
            eel.updateImageSrc(blob)()
    if flg == 0:
        print("FUNCTION CALL ")
        x = VideoCamera()
        y = x.capture_frame()
        x.__del__()
        print(y)
        # img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite('1.png', y)
        capFram = y
        im = Image.open("./1.png")

        
        
        # image_id = mycol.insert_one(image).inserted_id
        print("Image saved")
        



# @eel.expose
# def toupcamvideo_feed(flg):
#     global x
#     global camFrame
#     if flg == 1:   
#         x = VideoCamera()
#         y = gen(x)
#         print("hi")
#         # k = cv2.waitKey(1)
#         for each in y:
#             # Convert bytes to base64 encoded str, as we can only pass json to frontend
#             blob = base64.b64encode(each)
#             blob = blob.decode("utf-8")

#             eel.updateImageSrc(blob)()
#     if flg == 0:
#         print(x)
#         if x is not None:
#             #y = x.capture_frame()
#             y = gen(x)
#             y = x.capture_frame()
#             print(y)
#             x.__del__()
#             cv2.imwrite('2.png', y)
#             # img_name = "opencv_frame_{}.png".format(img_counter)
#             camFrame=y
#             for each in y:
#             # Convert bytes to base64 encoded str, as we can only pass json to frontend
#                 blob = base64.b64encode(each)
#                 blob = blob.decode("utf-8")
#                 camFrame=blob
#                 print("**",len(blob))
#                 eel.updateImageSrc(blob)()
            
#             x=None
    # if flg == 0:
    #     if x is not None:
    #         y = x.capture_frame()
    #     print("FUNCTION CALL ")
    #     x = VideoCamera()
    #     y = x.capture_frame()
    #     print(y)
    #     # img_name = "opencv_frame_{}.png".format(img_counter)
    #     cv2.imwrite('1.png', y)
    #     capFram = y
    #     print("{} written!")
    #     x.__del__()
    
    



# @eel.expose
# def video_video():
#     cam=toupcam.camera.ToupCamCamera()

def start_app():
    # Start the server
    try:
        BASEDIR = os.path.dirname(os.path.abspath(__file__))
        start_html_page = 'index.html'
        eel.init('web')
        logging.info("App Started")

        options = {'host': 'localhost', 'port': 0}
        eel.start(start_html_page)
    except Exception as e:
        err_msg = 'Could not launch a local server'
        logging.error('{}\n{}'.format(err_msg, e.args))
        #show_error(title='Failed to initialise server', msg=err_msg)
        logging.info('Closing App')
        sys.exit()


if __name__ == "__main__":
    start_app()
    # app = QApplication(sys.argv)
    # win = MainWin()
    # win.show()
    # sys.exit(app.exec_())
