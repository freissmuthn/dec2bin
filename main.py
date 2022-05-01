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

leds = LEDBoard(18,23,24,25) #LEDs definieren 

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
        #oder:
        #self.slider.setMinimum(0)
        #self.slider.setMaximum(15)
        
        #stylesheet notwendig?
        self.slider.setTickInterval(1) # Slider soll in 1er Schritten bewegt werden
        self.slider.setTickPosition(2)
        self.slider.valueChanged[int].connect(self.bin2dec)
        
        self.label = QLabel('0')
        sliderbox = QHBoxLayout()
        sliderbox.addWidget(self.slider)
        sliderbox.addWidget(self.label)
        vlayout.addLayout(sliderbox)

        self.bitlabels = [QLabel("1"),QLabel("2"),QLabel("4"),QLabel("8")] # Liste hier bitlabels erstellen 
        
        bitbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addLayout(bitbox)
        vlayout.addLayout(vbox)
        
        # Labels fuer 4 Bits     
        for index, bitlabel in enumerate(self.bitlabels): #geht es ohne enumerate?
            bitbox.addWidget(bitlabel)
            # rgb(255,0,0) = rot, rgb(200,200,200) = grau     
            bitlabel.setStyleSheet("background-color: rgb(200,200,200)") #grau beim start
            bitlabel.setAlignment(Qt.AlignCenter) #zentrieren
            bitlabel.setFixedWidth(30) # breite 30
            bitlabel.setFixedHeight(30) #höhe 30

        
        
        # Umrechnungstabelle
        #         zahl      [0]:1    [1]:2   [2]:4   [3]:8
        #         1           x
        #         2                    x
        #         3           x        x
        #         4                            x
        #         5           x                x
        #         6                    x       x
        #         7           x        x       x
        #         8                                    x
        #         9           x                        x
        #         10                   x               x
        #         11          x        x               x
        #         12                           x       x
        #         13          x                x       x
        #         14                   x       x       x
        #         15          x        x       x       x

    def bin2dec(self,value): 
        cvalue = str(value) #wandelt in einen String um
        self.label.setText(cvalue)
        #in den Labels können nur Strings eingetragen werden
        #daher vorher in String cvalue umgewandelt
        
        #Farbzuweisung & LEDs einschalten
        #wenn 1, 3, 5, 7, 9, 11, 13, 15 --> pos 0 von array mit hintergrundfarbe rot
        #bin 1
        if value % 2 == 1:
            self.bitlabels[0].setStyleSheet("background-color: rgb(255,0,0)")
            leds[0].on() #led 18 als zahl 1 geht an
        else: #wenn nicht eine der oben genannten zahlen, dann hintergrundfarbe grau
            self.bitlabels[0].setStyleSheet("background-color: rgb(200,200,200)")
            leds[0].off() #led 18 als 1 bleibt aus
        #bin 2
        if value ==2 or value==3 or value == 6 or value == 7 or value == 10 or value == 11 or value == 14 or value == 15:
            self.bitlabels[1].setStyleSheet("background-color: rgb(255,0,0)")
            leds[1].on()
        else: 
            self.bitlabels[1].setStyleSheet("background-color: rgb(200,200,200)")
            leds[1].off()    
        #bin 4
        if value ==4 or value==5 or value == 6 or value == 7 or value == 12 or value == 13 or value == 14 or value == 15:
            self.bitlabels[2].setStyleSheet("background-color: rgb(255,0,0)")
            leds[2].on()
        else: 
            self.bitlabels[2].setStyleSheet("background-color: rgb(200,200,200)")
            leds[2].off()
        #bin 8 
        if value >=8:
            self.bitlabels[3].setStyleSheet("background-color: rgb(255,0,0)")
            leds[3].on()
        else: 
            self.bitlabels[3].setStyleSheet("background-color: rgb(200,200,200)")
            leds[3].off()

app = QtWidgets.QApplication([])
win = MyWindow()
win.show()
app.exec_()