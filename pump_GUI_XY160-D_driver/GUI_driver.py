from pickle import FALSE, TRUE
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import pandas as pd
import csv

app = QtWidgets.QApplication([])
ui = uic.loadUi("pump_GUI_XY160-D_driver/GUI_QT_Main.ui")
ui.setWindowTitle("Pump Control GUI")


serial = QSerialPort()
serial.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()

global dataCurrentSens
dataCurrentSens = []
global dataFlowSens
dataFlowSens = []
global dataCurrent_accelerate
dataCurrent_accelerate = []

# preparing for starting
listClose = [ui.StartButton, ui.StopButton, ui.SpeedSlider, ui.InvertDirRB, ui.ManualSetCheckBox, ui.AutoSetCheckBox,
             ui.StartFreqSpinBox, ui.FreqStepspinBox, ui.AccelTimeSpinBox, ui.FinishFreqSpinBox, ui.FreqspinBox
             , ui.AccelarationStartButton]
for i in listClose:
    i.setEnabled(False)
ui.SliderShowLabel.setText(str(float('{:.1f}'.format(((ui.SpeedSlider.value()/ui.SpeedSlider.maximum())*100)))))

for port in ports:
    portList.append(port.portName())
ui.COMlist.addItems(portList) 

def onOpen():  # open COM-port
    serial.setPortName(ui.COMlist.currentText())
    serial.open(QIODevice.ReadWrite)
    if (serial.isOpen()):
        ui.StartButton.setEnabled(True)
        ui.StopButton.setEnabled(True)
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
    # сохраняем данные с момента подключения к COM-порту и до закрытия (данные приходят раз в 1 сек)
    if ui.AutoSetCheckBox.isChecked():
        file_name = "data_from_sensors" + str(ui.StartFreqSpinBox.value()) + "__"+ str(ui.FinishFreqSpinBox.value()) + "angle_valve_50" + ".csv"
    else:
        file_name = "data_from_sensors" + str(ui.FreqspinBox.value()) + "angle_valve_70" + ".csv"
    df = pd.DataFrame([dataCurrentSens, dataFlowSens])
    df = df.transpose() 
    df.to_csv(file_name, index=False, header=None)
    dataFlowSens.clear()
    dataCurrentSens.clear()
 
    listClose = [ui.StartButton, ui.StopButton, ui.SpeedSlider,ui.StartFreqLabel,
                 ui.StartFreqSpinBox, ui.FreqStepspinBox, ui.AccelTimeSpinBox, ui.FinishFreqSpinBox, ui.FreqspinBox
                 , ui.EngineFreqLabel, ui.EngineSpeedLabel, ]
    for i in listClose:
        i.setEnabled(False)
    ui.statusbar.setStyleSheet("QStatusBar{padding-left:8px;color:black;background:rgb(252,179,53);font-weight:bold;}")
    ui.statusbar.showMessage("Serial port is closed", 5000)
    ui.StartButton.setChecked(False)
    StopAll()
    serial.close()
    # analyse data from experiment


def serialSend(data): # sending packet by serial
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
    print([2])
    serialSend([2])

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"



def onRead():       # read serial data receiving by serial    
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    if (data[0]) == '0':
       ui.WFS_LCD.display(int(float(data[1]))) 
       dataCurrentSens.append(data[2])
       dataFlowSens.append(data[1])
       Plotting(int(data[2]))                #update value in plot of current
       print(data[2])


       
def engineFreqSpeedcontrol(): # 1st Option - working on constant frequency
    if (ui.StartButton.isChecked() & ui.ManualSetCheckBox.isChecked()):
        serialSend([3,ui.FreqspinBox.value(), 1])
        print([3, ui.FreqspinBox.value(), 1])
        ui.SliderShowLabel.setStyleSheet("QLabel { font-weight:bold; color : blue; }")   
    else:
        ui.SliderShowLabel.setStyleSheet("QLabel { font-weight:bold; color : black; }")  
    ui.SliderShowLabel.setText(str(float('{:.1f}'.format(((ui.SpeedSlider.value()/ui.SpeedSlider.maximum())*100)))))
def stopOn():
    StopAll()
    ui.StartButton.setChecked(False)
    

def startOn():
    if (ui.StartButton.isChecked()):
        if (ui.ManualSetCheckBox.isChecked()):
            engineFreqSpeedcontrol() # инициализация выставленных начальных значений
            ui.SpeedSlider.valueChanged.connect(engineFreqSpeedcontrol)
            ui.FreqspinBox.valueChanged.connect(engineFreqSpeedcontrol)
            
        elif (ui.AutoSetCheckBox.isChecked()):
            ui.ManualSetCheckBox.setEnabled(False)
            #engineAcceleration()
    else:
        StopAll()
        ui.AutoSetCheckBox.setCheckState(False)
        ui.ManualSetCheckBox.setCheckState(False)
        ui.ManualSetCheckBox.setEnabled(True)
        ui.AutoSetCheckBox.setEnabled(True)
        ui.AccelarationStartButton.setEnabled(False)
    ui.GraphCurrent.clearPlots()
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
        serialSend([4, start_value, finish_value, time_step, ui.SpeedSlider.value(),ui.FreqStepspinBox.value(),
                int(not(ui.InvertDirRB.isChecked())), int(ui.InvertDirRB.isChecked())]) # последние два значения передаем для выбора направления
        Plotting(ui.SpeedSlider.value())
        print([4, start_value, finish_value, time_step, ui.SpeedSlider.value(),ui.FreqStepspinBox.value()])
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

listX = [i for i in range(100)]
listY = [0 for i in range(100)]
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

