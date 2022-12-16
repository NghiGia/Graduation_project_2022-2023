import sys
from PyQt5.QtCore import *
import pyqtgraph as pg
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Controller import *
import cv2
import numpy as np

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self,clients):
        super(MainWindow, self).__init__()
        self.widget = QStackedWidget()
        self.setCentralWidget(self.widget)
        self.Scrn1 = Screen1(clients)
        self.Scrn2 = Screen2(clients)
        # self.Scrn1.buttonMotor.clicked.connect(self.changetoScreen1)
        self.Scrn1.buttonCamera.clicked.connect(self.changetoScreen2)
        self.Scrn2.buttonMotor.clicked.connect(self.changetoScreen1)
        # self.Scrn2.buttonCamera.clicked.connect(self.changetoScreen2)
        self.widget.addWidget(self.Scrn1)
        # self.widget.addWidget(self.Scrn2)
        self.widget.setCurrentWidget(self.Scrn1)
    def changetoScreen1(self):
        self.widget.setCurrentWidget(self.Scrn1)

    def changetoScreen2(self):
        self.widget.setCurrentWidget(self.Scrn2 )

class Screen1(QWidget):

    def __init__(self,clients):
        print(clients)
        super().__init__()
        self.setWindowTitle("Widgets App")
        self.setFixedHeight(38*25)
        self.setFixedWidth(49*25)
        layout = QGridLayout()

        height_short = 8
        width_short = 16

        height_long = height_short * 2 + 1
        width_long = width_short * 2 + 1

        self.emptylayout=QLabel()


        # Menu Bar
        self.buttonMotor = QPushButton('Motor')
        # self.buttonMotor.setGeometry(200, 100, 100, 40)
        self.buttonCamera = QPushButton('Camera')
        # self.buttonCamera.setGeometry(200, 100, 100, 40)
        self.buttonMotor.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "}"
                             "QPushButton::pressed"
                             )
        self.buttonCamera.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}"
                             "QPushButton::pressed"
                             )


        # layout.addWidget(self.buttonMotor,0,0,1,1)
        # layout.addWidget(self.buttonCamera,0,1,1,1)
        # ====================================================



        # Check Box
        self.box1 = QCheckBox("Check Box")
        self.box1.stateChanged.connect(lambda: box1_show_state(self.box1))
        # ===============================================



        # Dial
        self.box2 = QDial()
        self.box2.setRange(0, 50)
        self.box2.setSingleStep(1)
        self.box2_display_data=QLabel("Threshold:")
        self.box2.valueChanged.connect(lambda: box2_value_changed(self.box2,self.box2_display_data))
        self.box2.sliderMoved.connect(lambda: box2_slider_position(self.box2,self.box2.sliderPosition()))
        self.box2.sliderPressed.connect(lambda: box2_slider_pressed(self.box2))
        self.box2.sliderReleased.connect(lambda: box2_slider_released(self.box2))
        self.box2_display_data.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # ===============================================

        # Date
        self.box3 = QDateEdit()
        self.box3.editingFinished.connect(lambda: box3_update_calendar(self.box3))

        self.box4 = QDateEdit()
        self.box4.editingFinished.connect(lambda : box4_update_calendar(self.box4))
        self.titlebox3=QLabel("Start Date: ")
        self.titlebox4=QLabel("End Date: ")
        self.titlebox3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.titlebox4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # ================================================

        # Button
        self.box5 =QLabel("On")
        self.box5.setStyleSheet("border:3px  solid black; font-weight:bold")
        clients.publish("relay1", "1")
        self.box5.mousePressEvent = partial(box5_button_clicked, self.box5, clients)
        self.box5.setAlignment(Qt.AlignCenter)

        self.box6 = QLabel("On")
        self.box6.setStyleSheet("border:3px  solid black; font-weight:bold")
        clients.publish("relay2", "1")
        self.box6.mousePressEvent = partial(box6_button_clicked, self.box6, clients)
        self.box6.setAlignment(Qt.AlignCenter)

        self.titlebox5 = QLabel("Relay1")
        self.titlebox6 = QLabel("Relay2")
        self.titlebox5.setStyleSheet("background-color:lightgreen;border:3px  solid black; font-weight:bold")
        self.titlebox6.setStyleSheet("background-color:lightblue;border:3px  solid black; font-weight:bold")
        self.titlebox5.setAlignment(Qt.AlignCenter)
        self.titlebox6.setAlignment(Qt.AlignCenter)
        # ================================================

        # Line
        self.box7=pg.PlotWidget()
        self.box7.setXRange(0,20,padding=0)
        self.box7.setYRange(0, 60, padding=0)
        self.box7.setBackground('w')
        pen = pg.mkPen(color=(0, 0, 255))
        self.hourbox7 = [0,0]
        self.temperature = [0,0]
        styles = {'color': 'r', 'font-size': '20px'}
        self.box7.setTitle("Temperature", color="b", size="30pt")
        self.box7.setLabel('left', 'Temperature (°C)', **styles)
        self.box7.setLabel('bottom', 'Hour (H)', **styles)
        self.box7.showGrid(x=True, y=True)
        self.data_line_box7=self.box7.plot(self.hourbox7,self.temperature,pen=pen)


        self.box8 = pg.PlotWidget()
        self.box8.setXRange(0, 20, padding=0)
        self.box8.setYRange(0, 60, padding=0)
        self.box8.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.hourbox8 = [0, 0]
        self.moisture = [0, 0]
        styles = {'color': 'r', 'font-size': '20px'}
        self.box8.setTitle("Moisture", color="r", size="30pt")
        self.box8.setLabel('left', 'Moisture (%)', **styles)
        self.box8.setLabel('bottom', 'Hour (H)', **styles)
        self.box8.showGrid(x=True, y=True)
        self.data_line_box8 = self.box8.plot(self.hourbox8, self.moisture, pen=pen)

        Layout_Temp=QVBoxLayout()
        Layout_Moisture=QVBoxLayout()
        Layout_Temp.addWidget(self.box7)
        Layout_Moisture.addWidget(self.box8)
        # ================================================

        # Label show temp, moisture

        self.box9 = QLabel("Temp: 0")
        self.box9.setStyleSheet("border:3px  solid black ;font-weight:bold")
        self.box10 = QLabel("Moisture: 0")
        self.box10.setStyleSheet("border:3px  solid black; font-weight:bold")
        self.box9.setAlignment(Qt.AlignCenter)
        self.box10.setAlignment(Qt.AlignCenter)

        # =================================================

        # AI Capture
        self.box11= QLabel()
        self.box11.setStyleSheet("border:3px  solid blue ")
        grey = QPixmap(18*25, 8*25)
        self.box11.setPixmap(grey)

        self.disply_width_box11 = 16  * 25
        self.display_height_box11 = 8 * 25
        self.thread_box11 = VideoThread_box11()
        # connect its signal to the update_image slot
        self.thread_box11.change_pixmap_signal.connect(self.update_image_box11)
        # start the thread
        self.thread_box11.start()
        # ===============================em day==================

        # AI show
        self.disply_width_box12 =  18*25 # 18
        self.display_height_box12 = 18*25
        self.box12=QLabel()

        self.thread_box12 = VideoThread_box12()
        # connect its signal to the update_image slot
        self.thread_box12.change_pixmap_signal.connect(self.update_image_box12)
        # start the thread
        self.thread_box12.start()

        # https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
        # self.image=cv2.imread("logo.jpg")
        # self.tmp = self.image
        # image = imutils.resize( self.image, width=15*25)
        # frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        # self.box12.setPixmap(QPixmap.fromImage(image))

        # =================================================




        layout.addWidget(self.box9,0,0,height_short,width_short)
        layout.addWidget(self.box10, 0, 17, height_short, width_short)



        layout.addWidget(self.box7,9,0,height_long,width_long)
        layout.addWidget(self.box8, 27, 0, height_long, width_long)

        layout.addWidget(self.titlebox5, 9, 34, height_short, 6)
        layout.addWidget(self.titlebox6, 18, 34, height_short, 6)
        layout.addWidget(self.box5,9,40,height_short,10)
        layout.addWidget(self.box6, 18, 40, height_short, 10)

        layout.addWidget(self.box11, 0, 34, height_short, width_short)
        layout.addWidget(self.box12,27,34,height_long,16)
        self.setLayout(layout)

    def update_image_box11(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt_box11(cv_img)
        self.box11.setPixmap(qt_img)

    def convert_cv_qt_box11(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format =QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width_box11, self.display_height_box11, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def update_image_box12(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt_box12(cv_img)
        self.box12.setPixmap(qt_img)

    def convert_cv_qt_box12(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width_box12, self.display_height_box12, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class Screen2(QWidget):
    def __init__(self,clients):
        print(clients)
        super().__init__()
        self.setWindowTitle("Widgets App")

        layout = QGridLayout()

        # Menu Bar

        self.buttonMotor = QPushButton('Motor')
        # self.buttonMotor.setGeometry(200, 100, 100, 40)
        self.buttonCamera = QPushButton('Camera')
        # self.buttonCamera.setGeometry(200, 100, 100, 40)
        self.buttonMotor.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}"
                             "QPushButton::pressed"
                             )
        self.buttonCamera.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "}"
                             "QPushButton::pressed"
                             )



        # ====================================================
        self.setLayout(layout)


# class VideoThread(QThread):
#     change_pixmap_signal = pyqtSignal(np.ndarray)
#
#     def run(self):
#         # capture from web cam
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, cv_img = cap.read()
#             if ret:
#                 self.change_pixmap_signal.emit(cv_img)