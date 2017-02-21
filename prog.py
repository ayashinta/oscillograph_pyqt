import sys
import math
import serial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsView,QGraphicsScene,QApplication,QMainWindow
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from graph_test import Ui_Dialog


#class mySignal(QObject):
#    sgn1 = pyqtSignal()

yellow = QColor(255,255,0)
green = QColor(0,255,0)
white = QColor(255,255,255)
aoi = QColor(0,255,255)
red = QColor(255,0,0)
purple = QColor(160,32,240)
timer = QTimer()
#用于存储串口接收原始数据
outputFile = open('outputTEST.txt','w')

#画布高度
cvs_height = 0
#画布宽度
cvs_width = 0

class myProg(Ui_Dialog):

	#历史遗留变量
	bufferFlag = 1
	rateX = 1
	timeline4X = 0
	ranY = []
	Y_4drawline = []
	#CH的初始Y值
	leline = []
	#画笔
	qpen = []
	#是否可见
	CHvisibility = []
	#记录丢弃数据数量
	flushcount = 0


	#创建一个CH
	def createCH(self,sY,color,wid):
		self.ranY.append(sY)
		self.Y_4drawline.append(0)
		self.leline.append(sY)
		pen = QPen()
		pen.setWidth(wid)
		pen.setColor(color)
		self.qpen.append(pen)
		self.CHvisibility.append(1)

	def setiro_CH1(self,color):
		if color == 0:
			self.qpen[0].setColor(yellow)
			self.label_CH1.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255, 255, 0);")
		if color == 1:
			self.qpen[0].setColor(green)
			self.label_CH1.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(0, 255, 0);")
		if color == 2:
			self.qpen[0].setColor(white)
			self.label_CH1.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255, 255, 255);")
		if color == 3:
			self.qpen[0].setColor(aoi)
			self.label_CH1.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(0, 255, 255);")
		if color == 4:
			self.qpen[0].setColor(red)
			self.label_CH1.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255,0,0);")
		if color == 5:
			self.qpen[0].setColor(purple)
			self.label_CH1.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(160,32,240);")
	def setiro_CH2(self,color):
		if color == 0:
			self.qpen[1].setColor(yellow)
			self.label_CH2.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255, 255, 0);")
		if color == 1:
			self.qpen[1].setColor(green)
			self.label_CH2.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(0, 255, 0);")
		if color == 2:
			self.qpen[1].setColor(white)
			self.label_CH2.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255, 255, 255);")
		if color == 3:
			self.qpen[1].setColor(aoi)
			self.label_CH2.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(0, 255, 255);")
		if color == 4:
			self.qpen[1].setColor(red)
			self.label_CH2.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255,0,0);")
		if color == 5:
			self.qpen[1].setColor(purple)
			self.label_CH2.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(160,32,240);")
	def setiro_CH3(self,color):
		if color == 0:
			self.qpen[2].setColor(yellow)
			self.label_CH3.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255, 255, 0);")
		if color == 1:
			self.qpen[2].setColor(green)
			self.label_CH3.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(0, 255, 0);")
		if color == 2:
			self.qpen[2].setColor(white)
			self.label_CH3.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255, 255, 255);")
		if color == 3:
			self.qpen[2].setColor(aoi)
			self.label_CH3.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(0, 255, 255);")
		if color == 4:
			self.qpen[2].setColor(red)
			self.label_CH3.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255,0,0);")
		if color == 5:
			self.qpen[2].setColor(purple)
			self.label_CH3.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(160,32,240);")
	def setiro_CH4(self,color):
		if color == 0:
			self.qpen[3].setColor(yellow)
			self.label_CH4.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255, 255, 0);")
		if color == 1:
			self.qpen[3].setColor(green)
			self.label_CH4.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(0, 255, 0);")
		if color == 2:
			self.qpen[3].setColor(white)
			self.label_CH4.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255, 255, 255);")
		if color == 3:
			self.qpen[3].setColor(aoi)
			self.label_CH4.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(0, 255, 255);")
		if color == 4:
			self.qpen[3].setColor(red)
			self.label_CH4.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(255,0,0);")
		if color == 5:
			self.qpen[3].setColor(purple)
			self.label_CH4.setStyleSheet("font: 75 18pt 'Adobe 宋体 Std L';background-color: rgb(160,32,240);")

	def setWid_CH1(self, wid):
		self.qpen[0].setWidth(wid)
	def setWid_CH2(self, wid):
		self.qpen[1].setWidth(wid)
	def setWid_CH3(self, wid):
		self.qpen[2].setWidth(wid)
	def setWid_CH4(self, wid):
		self.qpen[3].setWidth(wid)

	def setVis_CH1(self,visibility):
		self.CHvisibility[0] = visibility + 1
	def setVis_CH2(self,visibility):
		self.CHvisibility[1] = visibility + 1
	def setVis_CH3(self,visibility):
		self.CHvisibility[2] = visibility + 1
	def setVis_CH4(self,visibility):
		self.CHvisibility[3] = visibility + 1

	def setCH_Y(self,CHindex,Y_pos):
		self.ranY[CHindex] = Y_pos

	def deleteCH(self,CHindex):
		del self.ranY[CHindex]
		del self.Y_4drawline[CHindex]
		del self.leline[CHindex]

	#绘制函数
	def draw(self):
		#打开COM2
		ser = serial.Serial('COM2',9600,timeout = 1)
		self.scene1.setSceneRect(0,0,cvs_width,0)
		buff = 400
		#while 1:
		data = ser.read(buff)
		print(self.flushcount)
		self.scene1.clear()
		for i in range(len(data)):
			outputFile.write(str(data[i]-48)+' ')
			if self.CHvisibility[i%4] != 1:
				continue
			self.scene1.addEllipse(cvs_width*4//buff*i-cvs_width//2,self.leline[i%4]+(data[i]-48)*10,1,1)
			if i >= 4:
				self.scene1.addLine(cvs_width*4//buff*i-cvs_width//2,self.leline[i%4]+(data[i]-48)*10,cvs_width*4//buff*(i-4)-cvs_width//2,self.leline[i%4]+(data[i-4]-48)*10,self.qpen[i%4])
		outputFile.write('\n')
		self.myView.show()
		self.flushcount += ser.inWaiting()
		ser.flushInput()
		ser.close()

	#历史遗留函数
	def changeView(self):
		W = self.myView.width()

		self.scene1.setSceneRect(self.timeline4X,0,W,0)
		self.scene2.setSceneRect(self.timeline4X,0,W,0)
		for i in range(len(self.ranY)):
			outputFile.write(str(self.ranY[i])+' ')
			if self.CHvisibility[i] != 1:
				self.ranY[i] = self.Y_4drawline[i] = self.leline[i]
				continue
			self.scene1.addEllipse(self.timeline4X,self.ranY[i],0,0)
			if self.timeline4X != 0:
				self.scene1.addLine(self.timeline4X,self.ranY[i],self.timeline4X+self.rateX,self.Y_4drawline[i],self.qpen[i])
			self.scene2.addEllipse(self.timeline4X,self.ranY[i],0,0)
			if self.timeline4X != 0:
				self.scene2.addLine(self.timeline4X,self.ranY[i],self.timeline4X+self.rateX,self.Y_4drawline[i],self.qpen[i])
			self.Y_4drawline[i] = self.ranY[i]
		outputFile.write('\n')

		if self.timeline4X // W % 2 == 0:
			self.myView.setScene(self.scene1)
			if self.bufferFlag == 0:
				self.scene2.clear()
				self.bufferFlag = 1

		else:
			self.myView.setScene(self.scene2)
			if self.bufferFlag == 1:
				self.scene1.clear()
				self.bufferFlag = 0

		self.myView.show()
		self.timeline4X = self.timeline4X - self.rateX

		for i in range(len(self.ranY)):
			if self.ranY[i] > self.leline[i] - 10 * i:
				self.ranY[i] = self.ranY[i] - i
			else:
				self.ranY[i] = self.ranY[i] +  10 * i

	def __init__(self,dialog):
		Ui_Dialog.__init__(self)
		self.setupUi(dialog)
		dialog.setWindowFlags(QtCore.Qt.Widget)
		self.scene1 = QGraphicsScene()
		self.scene2 = QGraphicsScene()
		self.myView.setStyleSheet("background-color:black;")
		self.myView.setScene(self.scene1)



def ratechange():
	timer.start(1000//prog.rate4test.value())

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()
	prog = myProg(dialog)


	prog.comboBox_CH1.activated.connect(prog.setVis_CH1)
	prog.comboBox_CH2.activated.connect(prog.setVis_CH2)
	prog.comboBox_CH3.activated.connect(prog.setVis_CH3)
	prog.comboBox_CH4.activated.connect(prog.setVis_CH4)
	prog.spinBox_CH1.valueChanged.connect(prog.setWid_CH1)
	prog.spinBox_CH2.valueChanged.connect(prog.setWid_CH2)
	prog.spinBox_CH3.valueChanged.connect(prog.setWid_CH3)
	prog.spinBox_CH4.valueChanged.connect(prog.setWid_CH4)
	prog.colorBox_CH1.activated.connect(prog.setiro_CH1)
	prog.colorBox_CH2.activated.connect(prog.setiro_CH2)
	prog.colorBox_CH3.activated.connect(prog.setiro_CH3)
	prog.colorBox_CH4.activated.connect(prog.setiro_CH4)

	#prog.rate4test.valueChanged.connect(ratechange)

	#prog.startButton.clicked.connect(prog.draw)

	cvs_height = prog.myView.height()
	cvs_width = prog.myView.width()

	prog.createCH(cvs_height//10*3+10,yellow,2)
	prog.createCH(cvs_height//10,green,2)
	prog.createCH(-cvs_height//10,white,2)
	prog.createCH(-cvs_height//10*3,aoi,2)

	seri = serial.Serial('COM2')
	seri.flushInput()
	seri.close()
	#timer.timeout.connect(prog.changeView)
	#timer.start(0.1)
	timer.timeout.connect(prog.draw)
	timer.start(1000)

	dialog.show()
	#prog.draw()
	sys.exit(app.exec_())