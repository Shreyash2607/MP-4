import imp
import sys, toupcam
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *

class MainWin(QMainWindow):
    eventImage = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.hcam = None
        self.buf = None      # video buffer
        self.w = 0           # video width
        self.h = 0           # video height
        self.total = 0
        self.setFixedSize(800, 600)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.initUI()
        self.initCamera()
        toolbar = QToolBar("Camera Tool Bar")

        # adding tool bar to main window
        self.addToolBar(toolbar)
        
        click_action = QAction("Click photo", self)

        # adding status tip to the photo action
        click_action.setStatusTip("This will capture picture")

        # adding tool tip
        click_action.setToolTip("Capture picture")


        # adding action to it
        # calling take_photo method
        click_action.triggered.connect(self.click_photo)

        # adding this to the tool bar
        toolbar.addAction(click_action)

        # similarly creating action for changing save folder
        change_folder_action = QAction("Change save location",
                                    self)

        # adding status tip
        change_folder_action.setStatusTip("Change folder where picture will be saved saved.")

        # adding tool tip to it
        change_folder_action.setToolTip("Change save location")

        # setting calling method to the change folder action
        # when triggered signal is emitted
        change_folder_action.triggered.connect(self.change_folder)

        # adding this to the tool bar
        toolbar.addAction(change_folder_action)


    def initUI(self):
        self.cb = QCheckBox('Auto Exposure', self)
        self.cb.stateChanged.connect(self.changeAutoExposure)
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.move(0, 30)
        self.label.resize(self.geometry().width(), self.geometry().height())

# the vast majority of callbacks come from toupcam.dll/so/dylib internal threads, so we use qt signal to post this event to the UI thread  
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == toupcam.TOUPCAM_EVENT_IMAGE:
            ctx.eventImage.emit()

# run in the UI thread
    @pyqtSlot()
    def eventImageSignal(self):
        if self.hcam is not None:
            try:
                self.hcam.PullImageV2(self.buf, 24, None)
                print(self.hcam.get_Size)
                self.total += 1
            except toupcam.HRESULTException as ex:
                QMessageBox.warning(self, '', 'pull image failed, hr=0x{:x}'.format(ex.hr), QMessageBox.Ok)
            else:
                self.setWindowTitle('{}: {}'.format(self.camname, self.total))
                img = QImage(self.buf, self.w, self.h, (self.w * 24 + 31) // 32 * 4, QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(img))

    def initCamera(self):
        a = toupcam.Toupcam.EnumV2()
        if len(a) <= 0:
            self.setWindowTitle('No camera found')
            self.cb.setEnabled(False)
        else:
            self.camname = a[0].displayname
            self.setWindowTitle(self.camname)
            self.eventImage.connect(self.eventImageSignal)
            try:
                self.hcam = toupcam.Toupcam.Open(a[0].id)
            except toupcam.HRESULTException as ex:
                QMessageBox.warning(self, '', 'failed to open camera, hr=0x{:x}'.format(ex.hr), QMessageBox.Ok)
            else:
                self.w, self.h = self.hcam.get_Size()
                bufsize = ((self.w * 24 + 31) // 32 * 4) * self.h
                self.buf = bytes(bufsize)
                self.cb.setChecked(self.hcam.get_AutoExpoEnable())            
                try:
                    if sys.platform == 'win32':
                        self.hcam.put_Option(toupcam.TOUPCAM_OPTION_BYTEORDER, 0) # QImage.Format_RGB888
                    self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
                except toupcam.HRESULTException as ex:
                    QMessageBox.warning(self, '', 'failed to start camera, hr=0x{:x}'.format(ex.hr), QMessageBox.Ok)

    def changeAutoExposure(self, state):
        if self.hcam is not None:
            self.hcam.put_AutoExpoEnable(state == Qt.Checked)

    def closeEvent(self, event):
        if self.hcam is not None:
            self.hcam.Close()
            self.hcam = None

    def select_camera(self, i):

        # getting the selected camera
        self.camera =  toupcam.Toupcam.EnumV2()

        # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)

        # setting capture mode to the camera
        self.camera.setCaptureMode(QCamera.CaptureStillImage)

        # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))

        # start the camera
        self.camera.start()

        # creating a QCameraImageCapture object
        self.capture = QCameraImageCapture(self.camera)

        # showing alert if error occur
        self.capture.error.connect(lambda error_msg, error,
                                msg: self.alert(msg))

        # when image captured showing message
        self.capture.imageCaptured.connect(lambda d,
                                        i: self.status.showMessage("Image captured : "
                                                                    + str(self.save_seq)))

        # getting current camera name
        self.current_camera_name = self.available_cameras[i].description()

        # initial save sequence
        self.save_seq = 0

    def click_photo(self):

		# time stamp
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")

        # capture the image and save it on the save path
        self.capture(os.path.join(self.save_path,
                                        "%s-%04d-%s.jpg" % (
            self.current_camera_name,
            self.save_seq,
            timestamp
        )))

        # increment the sequence
        self.save_seq += 1

	# change folder method
    def change_folder(self):

        # open the dialog to select path
        path = QFileDialog.getExistingDirectory(self,
                                                "Picture Location", "")

        # if path is selected
        if path:

            # update the path
            self.save_path = path

            # update the sequence
            self.save_seq = 0

    # method for alerts
    def alert(self, msg):

        # error message
        error = QErrorMessage(self)

        # setting text to the error message
        error.showMessage(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())