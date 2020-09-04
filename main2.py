"""Input text and convert into mp3 file"""

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
import pyttsx3

parent_path =  os.path.dirname(os.path.abspath(__file__))   #the path where the code is saved.........


class MainWindow(QMainWindow):
    """ The main window class"""    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.engine = pyttsx3.init() 
        self.voice_gender = 1      #0 male, 1 female
        self.speed = 100

        print("Greetings from Ashraf Minhaj, the creator of Text2mp3.")
        print("Please report bugs or errors if you find any.")
        print("\n'Two steps forward and one step backward is still one step forward.'")

        # Just to tune the audio system
        self.engine.say("Welcome there")
        self.engine.setProperty('rate', 80)
        self.engine.runAndWait()
        
        self.ui()


    def ui(self):
        """our UI here"""
        self.setWindowTitle("Text2mp3")
        self.setMaximumWidth(500)
        self.setMaximumHeight(250)
        #self.setStyleSheet("Background-color: black")
        layout1 = QGridLayout()                            #layout

        self.text_input_label = QLabel("Text to MP3 converter", self)
        self.text_input_label.setFont(QFont('SimHei', 10, weight=QFont.Bold))

        self.adjust_speed_label = QLabel("Adjust Speed", self)
        self.adjust_speed_label.setFont(QFont('SimHei', 10, weight=QFont.Bold))

        self.gender_label = QLabel("Select Voice Gender", self)
        self.gender_label.setFont(QFont('SimHei', 10, weight=QFont.Bold))

        self.file_save_input_label = QLabel("Convert", self)
        self.file_save_input_label.setFont(QFont('SimHei', 10, weight=QFont.Bold))
        self.about_label = QLabel("© Ashraf Minhaj", self)

        # ============ text edition section =====================
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter text..")

        #self.file_name_input.setText("my_text2mp3file")


        # ============ buttons =================================
        self.play_btn = QPushButton(self)
        self.play_btn.setText("Play")
        #self.play_btn.setStyleSheet("Background-color: lightskyblue; color: white")
        self.play_btn.clicked.connect(lambda : self.play())

        self.save_btn = QPushButton(self)
        self.save_btn.setText("convert Text to MP3 file")
        self.save_btn.setFont(QFont('SimHei', 10, weight=QFont.Bold))
        self.save_btn.setStyleSheet("Background-color: cornflowerblue; color: white")
        self.save_btn.clicked.connect(self.save)

        self.male_btn = QRadioButton("Male")
        #self.male_btn.setChecked(True)
        self.male_btn.toggled.connect(lambda : self.set_gender(0))

        self.female_btn = QRadioButton("Female")
        self.female_btn.setChecked(True)
        self.female_btn.toggled.connect(lambda : self.set_gender(1))

        #========== speed slider ===========================
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(120)
        self.speed_slider.setValue(100)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(5)
        self.speed_slider.valueChanged[int].connect(self.speed_val_change)
        
        #======== add everything into layout ==============
        layout1.addWidget(self.text_input_label, 0, 0)
        layout1.addWidget(self.text_input, 1, 0)
        layout1.addWidget(self.play_btn, 2, 0)
        layout1.addWidget(self.adjust_speed_label, 3, 0)
        layout1.addWidget(self.speed_slider, 4, 0)
        layout1.addWidget(self.gender_label, 5, 0)
        layout1.addWidget(self.male_btn, 6, 0)
        layout1.addWidget(self.female_btn, 7, 0)
        layout1.addWidget(self.file_save_input_label, 8, 0)
        layout1.addWidget(self.save_btn, 10, 0)
        layout1.addWidget(self.about_label, 11, 0, alignment=Qt.AlignCenter)
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

        #self.show()


    def play(self):
        words = self.text_input.toPlainText() #get input text
        print(words)
        if len(words) == 0 or words == " ":
            self.message(title="No text", msg="Input text first, then click play")
            return

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.voice_gender].id)
        self.engine.say(words)
        self.engine.setProperty('rate', self.speed)
        self.engine.runAndWait()

    def save(self):
        words = self.text_input.toPlainText()        #get input text
        #print(len(words))
        if len(words) == 0 or words == " ":
            self.message(title="No text to convert", msg="Input text first, then click convert")
            return

        self.file_name =  QFileDialog.getSaveFileName(self, "Save file", "untitled_text2mp3", ".mp3")

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.voice_gender].id)
        #self.engine.say(words)
        self.engine.setProperty('rate', self.speed)
        self.engine.save_to_file(words, f"{self.file_name[0]}.mp3")
        self.engine.runAndWait()

        self.message(title="Done!", 
                     msg="Done")

    def speed_val_change(self, value):
        #print(value)
        self.speed = value
    
    def set_gender(self, gender):
        self.voice_gender = gender

    def message(self, title="ERROR", msg="Something is wrong!"):
        """show message"""
        msg_box = QMessageBox()                       #QMessagebox pops up
        msg_box.setDefaultButton(QMessageBox.Close)   #Set button
        msg_box.setWindowTitle(title)                 #title
        msg_box.setText(msg)                          #inside message
        msg_box.exec_() 




app = QApplication(sys.argv)
window = MainWindow()
window.show()  #windows are hidden by default
app.exec_()    #start event loop