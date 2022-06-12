#!/usr/bin/env python3
#author: Freissmuth Nicole
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLCDNumber, QCheckBox,QSlider
from PyQt5.QtCore import Qt, QSize, QTimer
from gpiozero import LEDBoard, LED
from signal import pause

#Leider funktioniert das Programm bei mir nicht, es gibt folgende Fehlermeldungen aus:
# Traceback (most recent call last):
#   File "/home/pi/Documents/NWES_2021/GUI/bin2dec.py", line 114, in <module>
#     win = MyWindow()
#   File "/home/pi/Documents/NWES_2021/GUI/bin2dec.py", line 35, in __init__
#     self.slider.bin2dec[int].connect(self.bin2dec)
# AttributeError: 'QSlider' object has no attribute 'bin2dec'

leds=[LED(18),LED(23),LED(24),LED(25)] #LEDs definieren 

# Klasse für das Hauptfenster
class MyWindow(QMainWindow):
    def __init__(self):
        # Konstruktor von QMainWindow aufrufen, Objekt wird erzeugt
        super().__init__()
        self.setMinimumSize(QSize(550, 250))    #Membervariablen dieser Funktion --> self ist wie this
        self.setWindowTitle('Bit 2 Decimal Calculator Freissmuth') 
        
        wid = QWidget(self)
        self.setCentralWidget(wid)

        vlayout = QVBoxLayout() #Layout anlegen
        wid.setLayout(vlayout)
        
        # Slider + Label Anzeige 
        self.slider = QSlider(Qt.Horizontal,wid) #slider anlegen
        self.slider.setRange(0,15) #slider von 0 - 15

        self.slider.setTickInterval(1) # Slider soll in 1er Schritten bewegt werden
        self.slider.setTickPosition(2)
        self.slider.valueChanged[int].connect(self.bin2dec)
        
        self.label = QLabel('0')
        sliderbox = QHBoxLayout()
        sliderbox.addWidget(self.slider)
        sliderbox.addWidget(self.label)
        vlayout.addLayout(sliderbox)

        self.bitlabels = [QLabel("1"),QLabel("2"),QLabel("4"),QLabel("8")] 
        
        
        bitbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addLayout(bitbox)
        vlayout.addLayout(vbox)
        
        
        # Labels fuer 4 Bits     
        for index, bitlabel in enumerate(self.bitlabels):
            bitbox.addWidget(bitlabel)
            # rgb(255,0,0) = rot, rgb(200,200,200) = grau     
            bitlabel.setStyleSheet("background-color: rgb(200,200,200)") 
            bitlabel.setAlignment(Qt.AlignCenter) 
            bitlabel.setFixedWidth(30) 
            bitlabel.setFixedHeight(30)
            
        self.length=len(self.bitlabels)    
    def valueChanged(self, value):  
        cvalue= str(value)
        self.label.setText(str(cvalue))
        for j in range(self.length):
            i=self.length-j-1
            if (cvalue & 1<<j):
                self.bitlabels[i].setStyleSheet("background-color: rgb(255, 0, 0)")
                led.on()
            else:
                self.bitlabels[i].setStyleSheet("background-color: rgb(200,200,200)")
                led.off()

app = QtWidgets.QApplication([])
win = MyWindow()
win.show()
app.exec_()
