# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'usermanagement.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(550, 284)
        Form.setStyleSheet("border-color: rgb(255, 239, 213);")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_3.setText("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_username = QtWidgets.QLineEdit(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_username.setFont(font)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.gridLayout.addWidget(self.lineEdit_username, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_password = QtWidgets.QLineEdit(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.gridLayout.addWidget(self.lineEdit_password, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(False)
        self.pushButton.setChecked(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoRepeatInterval(50)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_1 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_1.setObjectName("checkBox_1")
        self.gridLayout_2.addWidget(self.checkBox_1, 0, 1, 1, 1)
        self.checkBox_6 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout_2.addWidget(self.checkBox_6, 1, 2, 1, 1)
        self.checkBox_7 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout_2.addWidget(self.checkBox_7, 1, 3, 1, 1)
        self.checkBox_0 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_0.setObjectName("checkBox_0")
        self.gridLayout_2.addWidget(self.checkBox_0, 0, 0, 1, 1)
        self.checkBox_8 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_8.setObjectName("checkBox_8")
        self.gridLayout_2.addWidget(self.checkBox_8, 2, 0, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_2.addWidget(self.checkBox_4, 1, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 0, 2, 1, 1)
        self.checkBox_5 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout_2.addWidget(self.checkBox_5, 1, 1, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_2.addWidget(self.checkBox_3, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 44, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.tab_4)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit_name = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.horizontalLayout_2.addWidget(self.lineEdit_name)
        self.label_5 = QtWidgets.QLabel(self.tab_4)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.lineEdit_code = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_code.setObjectName("lineEdit_code")
        self.horizontalLayout_2.addWidget(self.lineEdit_code)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.tableWidget = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.tableWidget)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout_3.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_username, self.lineEdit_password)
        Form.setTabOrder(self.lineEdit_password, self.pushButton_2)
        Form.setTabOrder(self.pushButton_2, self.pushButton)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "员工号"))
        self.pushButton_2.setText(_translate("Form", "删除"))
        self.label_2.setText(_translate("Form", "员工姓名"))
        self.pushButton.setText(_translate("Form", "新增"))
        self.checkBox_1.setText(_translate("Form", "领用"))
        self.checkBox_6.setText(_translate("Form", "清洁"))
        self.checkBox_7.setText(_translate("Form", "检查"))
        self.checkBox_0.setText(_translate("Form", "验收"))
        self.checkBox_8.setText(_translate("Form", "入库"))
        self.checkBox_4.setText(_translate("Form", "下线"))
        self.checkBox_2.setText(_translate("Form", "出库检查"))
        self.checkBox_5.setText(_translate("Form", "归还检查"))
        self.checkBox_3.setText(_translate("Form", "上线"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "权限分配"))
        self.label_4.setText(_translate("Form", "姓名"))
        self.label_5.setText(_translate("Form", "员工号"))
        self.pushButton_3.setText(_translate("Form", "查询"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "员工号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "姓名"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "权限"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "权限查询"))
