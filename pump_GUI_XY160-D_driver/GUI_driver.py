from pickle import FALSE, TRUE
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
import pyqtgraph as pg
# import sys


app = QtWidgets.QApplication([])
ui = uic.loadUi("GUI_QT_Main.ui")
ui.setWindowTitle("PumpDriverGUI")


serial = QSerialPort()
serial.setBaudRate(9600)
portList = []
ports = QSerialPortInfo().availablePorts()


# Предустановки
listClose = [ui.StartButton, ui.StopButton, ui.SpeedSlider, ui.InvertDirRB, ui.ManualSetCheckBox, ui.AutoSetCheckBox,
             ui.StartFreqSpinBox, ui.FreqStepspinBox, ui.AccelTimeSpinBox, ui.FinishFreqSpinBox, ui.FreqspinBox
             , ui.AccelarationStartButton]
for i in listClose:
    i.setEnabled(False)
ui.SliderShowLabel.setText(str(float('{:.1f}'.format(((ui.SpeedSlider.value()/ui.SpeedSlider.maximum())*100)))))

for port in ports:
    portList.append(port.portName())
#print(portList)
ui.COMlist.addItems(portList) 

def onOpen():  # Открытие COM-порта
    serial.setPortName(ui.COMlist.currentText())
    serial.open(QIODevice.ReadWrite)
    if (serial.isOpen()):
        ui.StartButton.setEnabled(True)
        ui.StopButton.setEnabled(True)
        #ui.statusbar.showMessage("<font color:red; Succes! Serial port is open </font>")
        ui.statusbar.setStyleSheet("QStatusBar{padding-left:8px;background:rgba(0,255,0,125);color:black;font-weight:bold;}")
        ui.statusbar.showMessage("Succes! Serial port is open", 5000)
        listOpen  = [ui.StartButton, ui.StopButton, ui.SpeedSlider, ui.InvertDirRB, ui.ManualSetCheckBox,
                     ui.AutoSetCheckBox,
                     ui.StartFreqSpinBox, ui.FreqStepspinBox, ui.AccelTimeSpinBox, ui.FinishFreqSpinBox, ui.FreqspinBox
            , ui.AccelarationStartButton]
        for i in listClose:
            i.setEnabled(True)

    else:
        ui.statusbar.setStyleSheet("QStatusBar{padding-left:8px;background:rgba(255,0,0,125);color:black;font-weight:bold;}")
        ui.statusbar.showMessage("Unable to open serial port")

   
def onClose():
    StopAll()
    serial.close()
    listClose = [ui.StartButton, ui.StopButton, ui.SpeedSlider,ui.StartFreqLabel,
                 ui.StartFreqSpinBox, ui.FreqStepspinBox, ui.AccelTimeSpinBox, ui.FinishFreqSpinBox, ui.FreqspinBox
                 , ui.EngineFreqLabel, ui.EngineSpeedLabel, ]
    for i in listClose:
        i.setEnabled(False)
    # ui.OpenButton.setChecked(False)
    # ui.StartButton.setEnabled(False)
    # ui.StopButton.setEnabled(False)
    # ui.SpeedSlider.setEnabled(False)
    ui.statusbar.setStyleSheet("QStatusBar{padding-left:8px;color:black;background:rgb(252,179,53);font-weight:bold;}")
    ui.statusbar.showMessage("Serial port is closed", 5000)
    ui.StartButton.setChecked(False)

def serialSend(data): #список int
    txs = ""
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serial.write(txs.encode())

def engineControl():
    serialSend([])

def StopAll():
    print([0,0,0,0,0])
    serialSend([0, 0, 0, 0, 0])


def onRead():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    # if data[0] == '0':
    #     ui.currentLCD.display(float(data[2]))
def engineFreqSpeedcontrol(): # Режим работы на постоянной частоте
    if (ui.StartButton.isChecked() & ui.ManualSetCheckBox.isChecked()):
        serialSend([0,ui.FreqspinBox.value(), 1])
        Plotting(ui.SpeedSlider.value())
        print([0, ui.FreqspinBox.value(), 1])
        ui.SliderShowLabel.setStyleSheet("QLabel { font-weight:bold; color : blue; }")   
    else:
        ui.SliderShowLabel.setStyleSheet("QLabel { font-weight:bold; color : black; }")  
    ui.SliderShowLabel.setText(str(float('{:.1f}'.format(((ui.SpeedSlider.value()/ui.SpeedSlider.maximum())*100)))))
def stopOn():
    ui.StartButton.setChecked(False)
    StopAll()

def startOn():
    # // WORK! добавить сообщение в статус при нажатии на недоступную кнопку старт
    if (ui.StartButton.isChecked()):
        if (ui.ManualSetCheckBox.isChecked()):
            engineFreqSpeedcontrol() # инициализация выставленных начальных значений
            ui.SpeedSlider.valueChanged.connect(engineFreqSpeedcontrol)
            ui.FreqspinBox.valueChanged.connect(engineFreqSpeedcontrol)
        elif (ui.AutoSetCheckBox.isChecked()):
            ui.AccelarationStartButton.setEnabled(True)
            #engineAcceleration()
    else:
        StopAll()
        ui.AutoSetCheckBox.setCheckState(False)
        ui.ManualSetCheckBox.setCheckState(False)
        ui.ManualSetCheckBox.setEnabled(True)
        ui.AutoSetCheckBox.setEnabled(True)
        ui.AccelarationStartButton.setEnabled(False)
def engineAcceleration():
    if (ui.AutoSetCheckBox.isChecked() & ui.StartButton.isChecked()):
        start_value = ui.StartFreqSpinBox.value()
        finish_value = ui.FinishFreqSpinBox.value()
        time_step = ui.AccelTimeSpinBox.value()
        freq_step = ui.FreqStepspinBox.value()
        dir_pin = 1 # по умолчанию будет отправлять значение соответствующее
        #  IN1 и IN2 (меняя их - меняем направление)
        if freq_step>((finish_value-start_value)/2):
            show_popup()
        #time_of_accelaration = ((finish_value-start_value)/freq_step)*time_step/1000
        #ui.TimlcdNumber.display(time_of_accelaration)
        serialSend([1, start_value, finish_value, time_step, ui.SpeedSlider.value(),ui.FreqStepspinBox.value(),
                int(not(ui.InvertDirRB.isChecked())), int(ui.InvertDirRB.isChecked())]) # последние два значения передаем для выбора направления
        Plotting(ui.SpeedSlider.value())
        print([1, start_value, finish_value, time_step, ui.SpeedSlider.value(),ui.FreqStepspinBox.value()])
        ui.SliderShowLabel.setStyleSheet("QLabel { font-weight:bold; color : blue; }")  
    else:
        ui.SliderShowLabel.setStyleSheet("QLabel { font-weight:bold; color : black; }") 
def ManualCBclick():
    if (ui.ManualSetCheckBox.isChecked()):
        ui.AutoSetCheckBox.setEnabled(False)
    else:
        ui.AutoSetCheckBox.setEnabled(True)
        ui.AccelarationStartButton.setEnabled(True)

def show_popup():
    msg = QMessageBox()
    msg.setWindowTitle("Warning")
    msg.setText("The Frequency step is too big! <br> The engine the engine will not be able to accelerate" )
 
     
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Ok)
     
    x = msg.exec_()
 

def AutoCBclick():
    if (ui.AutoSetCheckBox.isChecked()):
        ui.AccelarationStartButton.setEnabled(True)
        ui.ManualSetCheckBox.setEnabled(False)
    else:
        ui.AccelarationStartButton.setEnabled(False)
        ui.ManualSetCheckBox.setEnabled(True)


def TimeCalculate(): # предварительный расчет полного времени разгона
    if (ui.StartFreqSpinBox.value()*ui.FinishFreqSpinBox.value()*ui.FreqStepspinBox.value()*ui.AccelTimeSpinBox.value() !=0):
        time_of_accelaration = ((ui.FinishFreqSpinBox.value()-ui.StartFreqSpinBox.value())
                                /ui.FreqStepspinBox.value())*ui.AccelTimeSpinBox.value()/1000
        ui.TimlcdNumber.display(time_of_accelaration)

listX = [i for i in range(1000)]
listY = [0 for i in range(1000)]
def Plotting(value):
    global listY
    global listX
    listY = listY[1:]
    listY.append(value)
    ui.GraphCurrent.clear()
    ui.GraphCurrent.plot(listX,listY)

serial.readyRead.connect(onRead)
ui.OpenButton.clicked.connect(onOpen)
ui.CloseButton.clicked.connect(onClose)
ui.StartButton.clicked.connect(startOn)
ui.StopButton.clicked.connect(stopOn)
ui.SpeedSlider.valueChanged.connect(engineFreqSpeedcontrol)
ui.InvertDirRB.toggled.connect(engineFreqSpeedcontrol)
ui.AccelarationStartButton.clicked.connect(engineAcceleration)
ui.ManualSetCheckBox.clicked.connect(ManualCBclick)
ui.AutoSetCheckBox.clicked.connect(AutoCBclick)
# при изменении одного из параметров пересчет времени
ui.StartFreqSpinBox.valueChanged.connect(TimeCalculate)
ui.FinishFreqSpinBox.valueChanged.connect(TimeCalculate)
ui.AccelTimeSpinBox.valueChanged.connect(TimeCalculate)
ui.FreqStepspinBox.valueChanged.connect(TimeCalculate)
ui.show()
app.exec()

