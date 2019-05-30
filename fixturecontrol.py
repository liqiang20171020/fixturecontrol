from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QComboBox, QMessageBox, QAction, QWidget, QPushButton
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
from datetime import datetime
import jipUI, codelock, usermanagement, login, processui
import pymysql
from configparser import ConfigParser
import xlwings

class FixtureControl(QMainWindow, jipUI.Ui_MainWindow):
    def __init__(self):
        super(FixtureControl, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('治具管控软件V1.0.5')
        self.setWindowIcon(QtGui.QIcon('ball.ico'))

        self.tabWidget.currentChanged.connect(self.choseTab)

        self.comboBox_model.setCurrentIndex(-1)
        self.comboBox_gw.setCurrentIndex(-1)
        self.comboBox_board.setCurrentIndex(-1)
        self.comboBox_result.setCurrentIndex(-1)

        self.comboBox_model_2.setCurrentIndex(-1)
        self.comboBox_result_2.setCurrentIndex(-1)
        self.comboBox_gw_2.setCurrentIndex(-1)
        self.comboBox_line.setCurrentIndex(-1)

        self.lineEdit_serino_2.returnPressed.connect(self.choseModel2)
        self.pushButton_3.clicked.connect(self.flowSave)

        self.result = 0
        self.pushButton_4.clicked.connect(self.selectFixture)

        self.action1 = QAction(QtGui.QIcon('user.ico'), '新增员工', self)
        self.action1.triggered.connect(self.userManage)

        self.menu.addAction(self.action1)

        self.pushButton_2.clicked.connect(self.setValid)

        self.workerid = ''  # 防止直接点击确认程序崩溃

        self.comboBox_model_3.setCurrentIndex(-1)
        self.comboBox_board_2.setCurrentIndex(-1)
        self.comboBox_result_3.setCurrentIndex(-1)
        self.comboBox_3.setCurrentIndex(-1)
        self.comboBox_2.setCurrentIndex(-1)
        self.comboBox_auditor.setCurrentIndex(-1)

        try:
            unclock = codelock.CodeLock()
            con = ConfigParser()
            con.read('configure')
            ip = unclock.topassword('', con.get('DB', 'ip'))
            username = unclock.topassword('', con.get('DB', 'username'))
            password = unclock.topassword('', con.get('DB', 'password'))
            database = unclock.topassword('', con.get('DB', 'database'))
        except:
            ip = '192.168.4.242'
            username = 'root'
            password = 'root'
            database = 'test01'

        try:
            self.con = pymysql.connect(ip, username, password, database)
            self.cur = self.con.cursor()
        except:
            QMessageBox.warning(self, '警告', '数据库连接失败')
            self.tabWidget.setEnabled(0)

    def fixtureCheckin(self):       #治具验收
        self.comboBox_model.currentIndexChanged.connect(self.choseModel1)
        self.lineEdit_serino.returnPressed.connect(self.getSerino)
        self.pushButton.clicked.connect(self.save)

    def fixtureFlow(self):          #治具管控
        pass

    def fixtureRecord(self):        #治具状态查询
        pass

    def thermocoupleGridManager(self):
        self.comboBox_model_3.setCurrentIndex(-1)
        self.lineEdit_pcb_2.setText('')
        self.lineEdit_serino_4.setText('')
        self.lineEdit_machineid_3.setText('')
        self.comboBox_board_2.setCurrentIndex(-1)
        self.comboBox_result_3.setCurrentIndex(-1)
        self.comboBox_3.setCurrentIndex(-1)
        self.comboBox_2.setCurrentIndex(-1)
        self.label_39.setText('')
        self.comboBox_auditor.setCurrentIndex(-1)
        self.textEdit_3.setText('')
        self.tableWidget_4.clearContents()

        self.thermocoupleGridCanUse = 0     #当前编号的温测板是否可用，默认为不可用

        self.comboBox_model_3.currentIndexChanged.connect(self.choseModel3)
        self.pushButton_5.clicked.connect(self.thermocoupleGridSave)
        self.lineEdit_serino_4.returnPressed.connect(self.thermocoupleGridsetValue)

    def getCurrentTime(self):       #获取服务器当前时间
        sql = "select NOW()"
        self.cur.execute(sql)
        return self.cur.fetchall()[0][0]

    def closeEvent(self, *args, **kwargs):      #关闭函数重写
        if self.con:
            self.cur.close()
            self.con.close()

    def choseTab(self):              #切换tab选择不同的函数
        if self.tabWidget.currentIndex() == 0:
            self.fixtureCheckin()
        elif self.tabWidget.currentIndex() == 1:
            self.fixtureFlow()
        elif self.tabWidget.currentIndex() == 2:
            self.fixtureRecord()
        elif self.tabWidget.currentIndex() == 3:
            self.thermocoupleGridManager()
        else:
            pass

    def choseModel1(self):      #治具验收选择不同种类时，检查项目展示不同的内容、基础信息
        if self.comboBox_model.currentIndex() == 0:
            #设置部分控件不可用
            self.tableWidget.clearContents()
            self.comboBox_gw.setEnabled(0)
            self.comboBox_board.setEnabled(0)

            #显示检查项目
            self.tableWidget.setRowCount(6)
            item_list = [['刮刀平整度', '≤0.08mm', '塞规', '', ''], ['挡边到刮刀口的距离', '3±1mm', '尺子', '', ''], ['刮刀长度', '以测量为准', '尺子', '', ''], \
                         ['刮刀片厚度', '0.3±0.05', '游标卡尺', '', ''], ['刮刀片外观', '无变形、凸起、划痕', '目视', 'N/A', ''], ['刮刀角度', '45°/60°', '角度尺', '', '']]
            #给检查项目增加判定按钮
            for i in range(len(item_list)):
                com_bt  = QComboBox(self)
                com_bt.addItem('合格')
                com_bt.addItem('不合格')
                com_bt.setEditable(1)
                com_bt.setCurrentIndex(-1)
                self.tableWidget.setCellWidget(i, 4, com_bt)
                for j in range(6):
                    if j != 4 and j !=5:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(item_list[i][j])))
                    elif j == 5:
                        self.tableWidget.setItem(i, j , QTableWidgetItem(''))
        elif self.comboBox_model.currentIndex() == 1:
            self.tableWidget.clearContents()
            self.comboBox_gw.setEnabled(1)
            self.comboBox_board.setEnabled(1)

            self.tableWidget.setRowCount(11)
            item_list = [['外框尺寸', '736*736±5mm', '卷尺', '', ''], ['机种、流向，编号、日期、厚度等刻字 ', '完整，全面', '目视', 'N/A', ''], \
                         ['绷网是否完好', '无开胶', '目视', 'N/A', ''], ['钢网外观检查', '无顶坏、划伤等不良', '目视', 'N/A', ''], ['钢网厚度', '开制要求', '千分尺', '', ''], \
                         ['钢网孔壁无毛刺', '光滑、无毛刺', '高倍显微镜', '', ''], ['钢网开孔完整', '无多开孔、少开孔', '钢网检测机', '', ''], \
                         ['钢网张力符合要求', '40N~55N，单点差异小于10N', '钢网检测机', '', ''], ['钢网开孔尺寸符合要求', '面积比90~110%', '钢网检测机', '', ''], \
                         ['MARK点', '刻于非印刷面且完整无缺', '目视', 'N/A', ''], ['钢网开刻位置', '居中', '目视', 'N/A', '']]
            for i in range(len(item_list)):
                com_bt  = QComboBox(self)
                com_bt.addItem('合格')
                com_bt.addItem('不合格')
                com_bt.setEditable(1)
                com_bt.setCurrentIndex(-1)
                self.tableWidget.setCellWidget(i, 4, com_bt)
                for j in range(6):
                    if j != 4 and j != 5:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(item_list[i][j])))
                    elif j == 5:
                        self.tableWidget.setItem(i, j , QTableWidgetItem(''))
        elif self.comboBox_model.currentIndex() == 2:
            self.tableWidget.clearContents()
            self.comboBox_gw.setEnabled(0)
            self.comboBox_board.setEnabled(1)
            self.tableWidget.setRowCount(10)
            item_list = [['治具表面', '无凹坑，划痕，凸起，螺栓下沉无凸起，脱落。', '目视', 'N/A', ''], ['治具本体', '本体无变形，无毛刺，所有直角边倒角', '目视', 'N/A', ''], \
                         ['标示', '机种、流向、日期、厂商名称，图纸尺寸L*W*H，标示清楚', '目视', 'N/A', ''], ['材质', '铝合金', '目视', 'N/A', ''], \
                         ['零件避让', '零件避让安全距离X方向大于5mm,Y方向大于3mm,零件密集产品必须满足安全距离2mm', '亚克力透明罩板', '', ''], \
                         ['避让下沉深度', '8mm±0.5mm，特殊说明除外', '高度规/千分尺', '', ''], ['表面平整度', '最大值与最小值的差<0.15mm', '高度规/千分尺', '', ''], \
                         ['底部平整度', '治具放于大理石平台使用厚薄规检查底部缝隙，≤0.1mm', '塞规', '', ''], \
                         ['定位柱', """DEK:6mm±0.05mm
                                    松下：4.0mm±0.05mm""", '游标卡尺', '', ''], ['治具整体高度', """DEK 一体：81.00±0.1mm
                                                                                                MPM：39.00±0.1mm
                                                                                                松下：41.00±0.1mm
                                                                                                DEK/松下通用：19.00±0.1mm""", '游标卡尺/千分尺', '', '']]
            for i in range(len(item_list)):
                com_bt  = QComboBox(self)
                com_bt.addItem('合格')
                com_bt.addItem('不合格')
                com_bt.setEditable(1)
                com_bt.setCurrentIndex(-1)
                self.tableWidget.setCellWidget(i, 4, com_bt)
                for j in range(6):
                    if j != 4 and j != 5:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(item_list[i][j])))
                    elif j == 5:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(''))
        else:
            pass

    def save(self):         # 0治具验收，信息保存逻辑
        can = 1
        if self.comboBox_model.currentIndex() == 0:
            for z in range(6):
                check_item = self.tableWidget.item(z, 0).text()        #type: QTableWidgetItem
                check_standard = self.tableWidget.item(z, 1).text()
                check_tools = self.tableWidget.item(z, 2).text()
                test_result = self.tableWidget.item(z, 3).text()
                result = self.tableWidget.cellWidget(z, 4).currentText()
                nots = self.tableWidget.item(z, 5).text()
                serino = self.lineEdit_serino.text()
                if len(result) == 0:
                    can = can * 0
                else:
                    sql = "INSERT into check_process_result (serino, check_item, check_standard, check_tools, test_result, result, nots, save_time ) \
                    values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(serino, check_item, check_standard, check_tools, test_result, \
                    result, nots, self.getCurrentTime())
                    self.cur.execute(sql)
            pcb = self.lineEdit_pcb.text()
            version = self.lineEdit_version.text()
            workerid = self.lineEdit_workerid.text()
            if self.checkPrivileges(workerid, 0) == 1:
                storeid = self.lineEdit_storeid.text()
                machinetype = self.lineEdit_machineid.text()
                jipno = self.lineEdit_zj.text()
                gwthickness = self.lineEdit_gw_thickness.text()
                notes = self.textEdit.toPlainText()
                sql2 = "INSERT into fixture_check (model, pcb_lot, version, serino, worker_id, store_id, machine_type, check_result, jip_no, gw_thickness, nots, save_time, status) \
                values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', -1)".format(self.comboBox_model.currentText(), pcb, version, \
                serino, workerid, storeid, machinetype, self.comboBox_result.currentText(), jipno, gwthickness, notes, self.getCurrentTime())
                self.cur.execute(sql2)

                if can == 1 and len(pcb) >0 and len(version) > 0 and len(workerid) > 0 and len(storeid) > 0 and len(machinetype) > 0 and \
                len(jipno) > 0 and len(gwthickness) > 0 and len(serino) > 0 and self.comboBox_model.currentIndex() > -1 and self.comboBox_result.currentIndex() > -1:
                    self.con.commit()
                    self.clearContent()
                else:
                    QMessageBox.warning(self, '警告', '信息输入不全，无法保存数据！')
            else:
                QMessageBox.warning(self, '警告', '当前账号没有操作权限')
        elif self.comboBox_model.currentIndex() == 1:
            for z in range(11):
                check_item = self.tableWidget.item(z, 0).text()        #type: QTableWidgetItem
                check_standard = self.tableWidget.item(z, 1).text()
                check_tools = self.tableWidget.item(z, 2).text()
                test_result = self.tableWidget.item(z, 3).text()
                result = self.tableWidget.cellWidget(z, 4).currentText()
                nots = self.tableWidget.item(z, 5).text()
                serino = self.lineEdit_serino.text()
                if len(result) == 0:
                    can = 0
                else:
                    sql = "INSERT into check_process_result (serino, check_item, check_standard, check_tools, test_result, result, nots, save_time) \
                    values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(serino, check_item, check_standard, check_tools, test_result, \
                    result, nots, self.getCurrentTime())
                    self.cur.execute(sql)
            pcb = self.lineEdit_pcb.text()
            version = self.lineEdit_version.text()
            workerid = self.lineEdit_workerid.text()
            if self.checkPrivileges(workerid, 0) == 1:
                storeid = self.lineEdit_storeid.text()
                machinetype = self.lineEdit_machineid.text()
                jipno = self.lineEdit_zj.text()
                gwthickness = self.lineEdit_gw_thickness.text()
                notes = self.textEdit.toPlainText()
                gwmaterial = self.comboBox_gw.currentText()
                board = self.comboBox_board.currentText()
                sql2 = "INSERT into fixture_check (model, pcb_lot, version, serino, worker_id, store_id, machine_type, check_result, jip_no, gw_thickness, nots, save_time, gw_material, board, status) \
                values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', -1)".format(self.comboBox_model.currentText(), pcb, version, \
                serino, workerid, storeid, machinetype, self.comboBox_result.currentText(), jipno, gwthickness, notes, self.getCurrentTime(), gwmaterial, board)
                self.cur.execute(sql2)

                if can == 1 and len(pcb) >0 and len(version) > 0 and len(workerid) > 0 and len(storeid) > 0 and len(machinetype) > 0 and len(gwmaterial) > 0 and len(board) > 0 and\
                len(jipno) > 0 and len(gwthickness) > 0 and len(serino) > 0 and self.comboBox_model.currentIndex() > -1 and self.comboBox_result.currentIndex() > -1:
                    self.con.commit()
                    self.clearContent()
                else:
                    QMessageBox.warning(self, '警告', '信息输入不全，无法保存数据！')
            else:
                QMessageBox.warning(self, '警告', '当前账号没有操作权限!')
        elif self.comboBox_model.currentIndex() == 2:
            serino = self.lineEdit_serino.text()
            for z in range(10):
                check_item = self.tableWidget.item(z, 0).text()        #type: QTableWidgetItem
                check_standard = self.tableWidget.item(z, 1).text()
                check_tools = self.tableWidget.item(z, 2).text()
                test_result = self.tableWidget.item(z, 3).text()
                result = self.tableWidget.cellWidget(z, 4).currentText()
                nots = self.tableWidget.item(z, 5).text()
                if len(result) == 0:
                    can = 0
                else:
                    sql = "INSERT into check_process_result (serino, check_item, check_standard, check_tools, test_result, result, nots, save_time) \
                    values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(serino, check_item, check_standard, check_tools, test_result, \
                    result, nots, self.getCurrentTime())
                    self.cur.execute(sql)
            pcb = self.lineEdit_pcb.text()
            version = self.lineEdit_version.text()
            workerid = self.lineEdit_workerid.text()
            if self.checkPrivileges(workerid, 0) == 1:
                storeid = self.lineEdit_storeid.text()
                machinetype = self.lineEdit_machineid.text()
                jipno = self.lineEdit_zj.text()
                gwthickness = self.lineEdit_gw_thickness.text()
                notes = self.textEdit.toPlainText()
                board = self.comboBox_board.currentText()
                sql2 = "INSERT into fixture_check (model, pcb_lot, version, serino, worker_id, store_id, machine_type, check_result, jip_no, gw_thickness, nots, save_time, board, status) \
                values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', -1)".format(self.comboBox_model.currentText(), pcb, version, \
                serino, workerid, storeid, machinetype, self.comboBox_result.currentText(), jipno, gwthickness, notes, self.getCurrentTime(), board)
                self.cur.execute(sql2)
                if can == 1 and len(pcb) >0 and len(version) > 0 and len(workerid) > 0 and len(storeid) > 0 and len(machinetype) > 0  and len(board) > 0 and\
                len(jipno) > 0 and len(gwthickness) > 0 and len(serino) > 0 and self.comboBox_model.currentIndex() > -1 and self.comboBox_result.currentIndex() > -1:
                    self.con.commit()
                    self.clearContent()
                else:
                    QMessageBox.warning(self, '警告', '信息输入不全，无法保存数据！')
            else:
                QMessageBox.warning(self, '警告', '当前账号没有操作权限')
        else:
            pass

    def clearContent(self):
        if self.tabWidget.currentIndex() == 0:
            self.lineEdit_pcb.clear()
            self.lineEdit_version.clear()
            self.lineEdit_serino.clear()
            self.lineEdit_workerid.clear()
            self.lineEdit_storeid.clear()
            self.lineEdit_machineid.clear()
            self.comboBox_result.clear()
            self.lineEdit_zj.clear()
            self.lineEdit_gw_thickness.clear()
            self.textEdit.clear()

            if self.comboBox_model.currentIndex() == 0:
                for i in range(6):
                    self.tableWidget.cellWidget(i, 4).setCurrentIndex(-1)
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(''))
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(''))
                self.tableWidget.setItem(4, 3, QTableWidgetItem('N/A'))
            elif self.comboBox_model.currentIndex() == 1:
                self.comboBox_gw.setCurrentIndex(-1)
                self.comboBox_board.setCurrentIndex(-1)
                for i in range(11):
                    self.tableWidget.cellWidget(i, 4).setCurrentIndex(-1)
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(''))
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(''))
                self.tableWidget.setItem(1, 3, QTableWidgetItem('N/A'))
                self.tableWidget.setItem(2, 3, QTableWidgetItem('N/A'))
                self.tableWidget.setItem(3, 3, QTableWidgetItem('N/A'))
                self.tableWidget.setItem(9, 3, QTableWidgetItem('N/A'))
                self.tableWidget.setItem(10, 3, QTableWidgetItem('N/A'))
            elif self.comboBox_model.currentIndex() == 2:
                self.comboBox_board.setCurrentIndex(-1)
                for i in range(10):
                    self.tableWidget.cellWidget(i, 4).setCurrentIndex(-1)
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(''))
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(''))
                self.tableWidget.setItem(0, 3, QTableWidgetItem('N/A'))
                self.tableWidget.setItem(1, 3, QTableWidgetItem('N/A'))
                self.tableWidget.setItem(2, 3, QTableWidgetItem('N/A'))
                self.tableWidget.setItem(3, 3, QTableWidgetItem('N/A'))
            else:
                pass
        elif self.tabWidget.currentIndex() == 1:
            self.comboBox_model_2.setCurrentIndex(-1)
            self.lineEdit_serino_2.clear()
            self.comboBox_gw_2.setCurrentIndex(-1)
            self.lineEdit_workerid_2.clear()
            self.comboBox_line.setCurrentIndex(-1)
            self.lineEdit_machineid_2.clear()
            self.comboBox_result_2.setCurrentIndex(-1)
            self.textEdit_2.clear()
            self.lineEdit_use_age.clear()

            self.lineEdit_workerid_2.setFocus()

            self.tableWidget_2.clearContents()
            self.tableWidget_2.setRowCount(0)

            self.comboBox.setCurrentIndex(0)

        elif self.tabWidget.currentIndex() == 2:
            pass
        else:
            pass

    def choseModel2(self):      #治具管控选择不同种类时，检查项目展示不同的内容、基础信息
        self.tableWidget_2.clearContents()
        self.tableWidget_2.setRowCount(0)
        self.comboBox_gw_2.setCurrentIndex(-1)
        process_list = ['领用', '出库检查', '上线', '下线', '归还检查', '清洁', '检查', '入库']
        self.workerid = self.lineEdit_workerid_2.text()
        self.serino = self.lineEdit_serino_2.text()
        if len(self.workerid) > 0 and len(self.serino) > 0:
            if self.checkValid(self.serino) == 1:               #可用
                sql1 = "select COUNT(code) from user_access where CODE = '{}'".format(self.workerid)
                self.cur.execute(sql1)
                worker_result = self.cur.fetchall()
                if worker_result[0][0] == 1:            # 输入的员工号可用
                    sql2 = "select serino, save_time, pcb_lot, store_id, machine_type, board, model, `status`, worksheet, line from fixture_check where serino = '{}' ORDER BY save_time DESC LIMIT 1".format(self.serino)
                    self.cur.execute(sql2)
                    self.result = self.cur.fetchall()
                    if self.cur.rowcount == 1:                               #根据输入的序列号查询得到记录
                        cur_process = self.result[0][-3]
                        if cur_process != -1 and cur_process != 7:           #当前工序为领用时需要输入线别、工单，其余工序则自动带出
                            self.lineEdit_machineid_2.setText(str(self.result[0][-2]))
                            self.comboBox_line.setCurrentText(str(self.result[0][-1]))
                        if cur_process == 7 :
                            self.next_process = 0
                        else:
                            self.next_process = cur_process + 1
                            if self.result[0][-4] == '刮刀':
                                self.comboBox_model_2.setCurrentIndex(0)
                                if self.next_process == 1:
                                    item_list = [['刮刀整洁度', '正反面无锡膏残留、脏污'], ['刮刀标示', '无破损、字迹清晰'], ['刮刀片', '无变形、无缺口'], \
                                    ['刮刀领用确认', '型号、角度、长度'], ['挡板', '无缺失、无凸起'], ['螺丝', '无松动、无脱落']]
                                    self.tableWidget_2.setRowCount(6)
                                    for i in range(6):
                                        for j in range(2):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 2, QTableWidgetItem('目视'))
                                            self.tableWidget_2.setItem(i, 3, QTableWidgetItem('N/A'))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                elif self.next_process == 4:
                                    item_list = [['表面', '无锡膏堆积'], ['刮刀标示', '无破损、字迹清晰'], ['刮刀片', '无变形、无缺口'], \
                                                ['挡板', '无缺失、无凸起'], ['螺丝', '无松动、无脱落']]

                                    self.tableWidget_2.setRowCount(5)
                                    for i in range(5):
                                        for j in range(2):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 2, QTableWidgetItem('目视'))
                                            self.tableWidget_2.setItem(i, 3, QTableWidgetItem('N/A'))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                elif self.next_process == 6:
                                    item_list = [['外观检查', '本体无变形，刀片无损伤', '目视', 'N/A'], ['刮刀标签', '清晰无破损', '目视', 'N/A'], \
                                                 ['表面清洁度', '正反面无锡膏残留', '目视', 'N/A'], ['刮刀片磨损', '小于0.08mm', '塞规', ''], \
                                                 ['挡板位置', '距离刮刀口3±1mm', '游标卡尺', ''], ['螺丝紧固', '无松动、无脱落', '目视', '']]
                                    self.tableWidget_2.setRowCount(6)
                                    for i in range(6):
                                        for j in range(4):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                else:
                                    pass
                            elif self.result[0][-4] == '钢网':
                                self.comboBox_model_2.setCurrentIndex(1)
                                if self.next_process == 1:
                                    item_list = [['钢网领用正确性', '产品名称，PCB料号，钢网版本，PCB面别'], ['绷网', '无开胶、无破损'], ['边框', '无变形'], \
                                    ['贴膜', '完整'], ['外观', '印刷区域顶坏\划伤(参照SOP定义)'], ['标签', '无破损，无脱落'], ['钢网整洁度', '正反面无锡膏残留，脏污']]
                                    self.tableWidget_2.setRowCount(7)
                                    for i in range(7):
                                        for j in range(2):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 2, QTableWidgetItem('目视'))
                                            self.tableWidget_2.setItem(i, 3, QTableWidgetItem('N/A'))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                elif self.next_process == 4:
                                    item_list = [['绷网', '无开胶、无破损'], ['边框', '无变形'], ['外观', '印刷区域顶坏\划伤(参照SOP定义)'], ['标签', '无破损，无脱落'], ['表面', '无锡膏堆积']]
                                    self.tableWidget_2.setRowCount(5)
                                    for i in range(5):
                                        for j in range(2):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 2, QTableWidgetItem('目视'))
                                            self.tableWidget_2.setItem(i, 3, QTableWidgetItem('N/A'))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                elif self.next_process == 6:
                                    item_list = [['绷网', '无开胶、无破损', '目检', 'N/A'], ['外观', '印刷区域顶坏\划伤(参照SOP定义)', '目检', 'N/A'], \
                                                 ['表面清洁度', '正反面无锡膏残留', '目检', 'N/A'], ['孔壁清洁度', '单个开孔内少于3颗锡珠', '高倍显微镜', ''], \
                                                 ['张力', '30N~55N(单点差异小于10N)', '钢网检测机', ''], ['开孔面积比', '面积比90~110%', '钢网检测机', '']]
                                    self.tableWidget_2.setRowCount(6)
                                    for i in range(6):
                                        for j in range(4):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                else:
                                    pass
                            elif self.result[0][-4] == '印刷治具':
                                self.comboBox_model_2.setCurrentIndex(2)
                                if self.next_process == 1:
                                    item_list = [['领用确认', '型号、机种、PCB料号'], ['治具本体', '无破损凸起'], ['治具标示', '无破损、字迹清晰'], \
                                    ['表面清洁', '正反面无锡膏残留、赃污']]
                                    self.tableWidget_2.setRowCount(4)
                                    for i in range(4):
                                        for j in range(2):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 2, QTableWidgetItem('目视'))
                                            self.tableWidget_2.setItem(i, 3, QTableWidgetItem('N/A'))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                elif self.next_process == 4:
                                    item_list = [['治具本体', '无破损凸起'], ['治具标示', '无破损、字迹清晰'], ['表面清洁', '正反面无锡膏残留、赃污']]
                                    self.tableWidget_2.setRowCount(3)
                                    for i in range(3):
                                        for j in range(2):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 2, QTableWidgetItem('目视'))
                                            self.tableWidget_2.setItem(i, 3, QTableWidgetItem('N/A'))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                elif self.next_process == 6:
                                    item_list = [['外观检查', '本体无损伤', '目视', 'N/A'], ['治具标签', '清晰无破损', '目视', 'N/A'], \
                                                 ['表面清洁度', '正反面无锡膏残留', '目视', 'N/A'], ['治具平整度', '小于0.1mm', '千分尺', '']]
                                    self.tableWidget_2.setRowCount(4)
                                    for i in range(4):
                                        for j in range(4):
                                            self.tableWidget_2.setItem(i, j, QTableWidgetItem(item_list[i][j]))
                                            self.tableWidget_2.setItem(i, 5, QTableWidgetItem(''))
                                            com_bt = QComboBox(self)
                                            com_bt.addItem('合格')
                                            com_bt.addItem('不合格')
                                            com_bt.setEditable(1)
                                            com_bt.setCurrentIndex(-1)
                                            self.tableWidget_2.setCellWidget(i, 4, com_bt)
                                else:
                                    pass
                            else:
                                pass
                        self.comboBox_gw_2.setCurrentIndex(self.next_process)
                    else:               #输入的序列号查询不到任何记录
                        pass

                    palette = QtGui.QPalette()
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
                    brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
                    brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
                    self.label_20.setPalette(palette)
                    self.label_20.setText('请点击按钮确认')
                else:
                    palette = QtGui.QPalette()
                    brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
                    brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
                    brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
                    brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
                    self.label_20.setPalette(palette)
                    self.label_20.setText('请输入正确的工号')
            elif self.checkValid(self.serino) == -1:            #暂停
                QMessageBox.warning(self, '警告', '当前序列号已经被暂停使用')
                self.comboBox_model_2.setEnabled(0)
                self.lineEdit_serino_2.setEnabled(0)
                self.lineEdit_workerid_2.setEnabled(0)

                #以下代码为新增：暂停使用的材料可以维修后继续使用
                sql2 = "select serino, save_time, pcb_lot, store_id, machine_type, board, model, `status`, worksheet, line from fixture_check where serino = '{}' ORDER BY save_time DESC LIMIT 1".format(
                self.serino)
                self.cur.execute(sql2)
                self.result = self.cur.fetchall()
            elif self.checkValid(self.serino) == -2:            #报废
                QMessageBox.warning(self, '警告', '当前序列号已经被报废')
                self.comboBox_model_2.setCurrentIndex(-1)
                self.lineEdit_serino_2.clear()
                self.lineEdit_workerid_2.clear()
                self.lineEdit_workerid_2.setFocus()
            else:
                pass
        else:
            pass

    def flowSave(self):     #1治具管控，信息保存逻辑
        can = 1
        if len(self.workerid) > 0 and self.checkPrivileges(self.workerid, self.next_process+1) == 1:
            line = self.comboBox_line.currentText()
            worksheet = self.lineEdit_machineid_2.text()
            downreason = self.comboBox_result_2.currentText()
            notes = self.textEdit_2.toPlainText()
            useage = self.lineEdit_use_age.text()          #新增字段，下线是的使用次数
            if useage is None or len(useage) == 0:
                useage = 0
            if self.result == 0:
                QMessageBox.warning(self, '警告', '请先输入输入员工号和序列号。')
            else:
                sql1 = "INSERT into fixture_check (serino, status, line, worksheet, pcb_lot, save_time, worker_id, store_id, down_reason, notes, machine_type, board, model, use_age) VALUES \
                ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', {13:d})".format(self.serino, self.next_process, line, worksheet, self.result[0][2], \
                self.getCurrentTime(), self.workerid, self.result[0][3], downreason, notes, self.result[0][4], self.result[0][5], self.comboBox_model_2.currentText(), int(useage))
                # print(sql1)
                for z in range(self.tableWidget_2.rowCount()):
                    check_item = self.tableWidget_2.item(z, 0).text()                     # type: QTableWidgetItem
                    check_standard = self.tableWidget_2.item(z, 1).text()
                    check_tools = self.tableWidget_2.item(z, 2).text()
                    test_result = self.tableWidget_2.item(z, 3).text()
                    result = self.tableWidget_2.cellWidget(z, 4).currentText()
                    nots = self.tableWidget_2.item(z, 5).text()
                    serino = self.lineEdit_serino_2.text()
                    if len(result) == 0:
                        can = 0
                    else:
                        sql = "INSERT into check_process_result (serino, check_item, check_standard, check_tools, test_result, result, nots, save_time ) \
                        values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(serino, check_item, check_standard, check_tools, test_result, \
                        result, nots, self.getCurrentTime())
                        self.cur.execute(sql)

                if len(line) > 0 and len(worksheet) > 0 and can == 1:
                    delta_times = str(self.getCurrentTime() - self.result[0][1]).split(':')
                    delta_times = int(delta_times[1]) + int(delta_times[0]) * 60
                    if self.next_process == 6:
                        if int(delta_times) > 10:
                            self.cur.execute(sql1)
                            self.con.commit()
                            self.clearContent()
                        else:
                            QMessageBox.warning(self, '警告', '检查时间与清洁时间间隔不足10分钟。')
                    elif self.next_process == 7:
                        if int(delta_times) > 3:
                            self.cur.execute(sql1)
                            self.con.commit()
                            self.clearContent()
                        else:
                            QMessageBox.warning(self, '警告', '入库时间与检查时间间隔不足3分钟。')
                    else:
                        if self.next_process == 3 and (self.comboBox_result_2.currentIndex() == -1 or len(str(useage)) == 0 or int(useage) == 0):                       #当前工序为线下时，必须选择下线原因\使用数量。这个地方处理有点问题，如果输入字符串就崩溃了
                            QMessageBox.warning(self, '警告', '当前工序为下线，请选择下线原因且输入使用次数！')
                        else:
                            self.cur.execute(sql1)
                            self.con.commit()
                            self.clearContent()

                else:
                    QMessageBox.warning(self, '提示', '信息输入不完全，无法保存数据！')
        else:
            QMessageBox.warning(self, '警告', '当前账号没有操作权限！')

    def selectFixture(self):
        self.tableWidget_3.setRowCount(0)
        serino = self.lineEdit_serino_3.text()
        sql1 = "SELECT serino, `status`, line, worksheet, machine_type, pcb_lot, save_time, worker_id, gw_thickness, nots, \
        store_id, down_reason, notes, version, board, is_valid, use_age, model, manager_id, process_name from fixture_check where serino = '{}'".format(serino)
        self.cur.execute(sql1)
        result = self.cur.fetchall()
        num = self.cur.rowcount
        self.tableWidget_3.setRowCount(num)
        for i in range(num):
            for j in range(20):
                if j == 1:
                    select_btn = QPushButton('', self)
                    select_btn.setFlat(True)
                    self.tableWidget_3.setCellWidget(i, j, select_btn)
                    select_btn.clicked.connect(self.selectProcessResult)
                    if result[i][-3] != '测温板':
                        if result[i][j] == -1:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('验收'))
                        elif result[i][j] == 0:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('领用'))
                        elif result[i][j] == 1:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('出库检查'))
                        elif result[i][j] == 2:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('上线'))
                        elif result[i][j] == 3:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('下线'))
                        elif result[i][j] == 4:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('归还检查'))
                        elif result[i][j] == 5:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('清洁'))
                        elif result[i][j] == 6:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('检查'))
                        elif result[i][j] == 7:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('入库'))
                    else:
                        if result[i][j] == 0:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('新做'))
                        elif result[i][j] == 1:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('正在使用'))
                        elif result[i][j] == 2:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem('报废'))

                elif j == 15:
                    if result[i][j] == 0:
                        self.tableWidget_3.setItem(i, j, QTableWidgetItem('可用'))
                    elif result[i][j] == 1:
                        self.tableWidget_3.setItem(i, j, QTableWidgetItem('暂停'))
                    elif result[i][j] == 2:
                        self.tableWidget_3.setItem(i, j, QTableWidgetItem('报废'))
                else:
                    self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def getSerino(self):
        if self.comboBox_model.currentIndex() == 0:         #刮刀
            sql1 = "select * from sys_serial where use_key = 'YSODGD'"
            self.cur.execute(sql1)
            result1 = self.cur.fetchall()
            if self.cur.rowcount == 1:
                cur_serial = '{:0>5d}'.format(int(result1[0][-1]) + 1)
                sql2 = "update sys_serial set serial_no = '{}' where use_key = 'YSODGD'".format(cur_serial)
                self.cur.execute(sql2)
                self.con.commit()
                self.lineEdit_serino.setText('YSODGD' + cur_serial)

            elif self.cur.rowcount == 0:
                sql3 = "insert into sys_serial (use_key, serial_no) values ('YSODGD', '00001')"
                self.cur.execute(sql3)
                self.con.commit()
                cur_serial = '00001'
                self.lineEdit_serino.setText('YSODGD' + cur_serial)
            else:
                pass
        elif self.comboBox_model.currentIndex() == 1:
            sql1 = "select * from sys_serial where use_key = 'YSODGW'"
            self.cur.execute(sql1)
            result1 = self.cur.fetchall()
            if self.cur.rowcount == 1:
                cur_serial = '{:0>5d}'.format(int(result1[0][-1]) + 1)
                sql2 = "update sys_serial set serial_no = '{}' where use_key = 'YSODGW'".format(cur_serial)
                self.cur.execute(sql2)
                self.con.commit()
                self.lineEdit_serino.setText('YSODGW' + cur_serial)

            elif self.cur.rowcount == 0:
                sql3 = "insert into sys_serial (use_key, serial_no) values ('YSODGW', '00001')"
                self.cur.execute(sql3)
                self.con.commit()
                cur_serial = '00001'
                self.lineEdit_serino.setText('YSODGW' + cur_serial)
            else:
                pass
        elif self.comboBox_model.currentIndex() == 2:       #印刷治具实装
            sql1 = "select * from sys_serial where use_key = 'YSODYS'"
            self.cur.execute(sql1)
            result1 = self.cur.fetchall()
            if self.cur.rowcount == 1:
                cur_serial = '{:0>5d}'.format(int(result1[0][-1]) + 1)
                sql2 = "update sys_serial set serial_no = '{}' where use_key = 'YSODYS'".format(cur_serial)
                self.cur.execute(sql2)
                self.con.commit()
                self.lineEdit_serino.setText('YSODYS' + cur_serial)

            elif self.cur.rowcount == 0:
                sql3 = "insert into sys_serial (use_key, serial_no) values ('YSODYS', '00001')"
                self.cur.execute(sql3)
                self.con.commit()
                cur_serial = '00001'
                self.lineEdit_serino.setText('YSODYS' + cur_serial)
            else:
                pass
        else:
            pass

    def userManage(self):
        self.login_ui = UserManagementLogin(self)       #显示权限登录界面，只有权限为0的才可以处理
        self.login_ui.show()

    def checkValid(self, no):
        sql = "select serino, is_valid from fixture_check where serino = '{}' ORDER BY save_time DESC LIMIT 1".format(no)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        count = self.cur.rowcount
        if count == 0:
            pass                               #没有记录
        else:
            if result[0][-1] == 1:             #暂停
                return -1
            elif result[0][-1] == 2:           #报废
                return -2
            elif result[0][-1] == 0:           #可用
                return 1

    def setValid(self):
            if self.result == 0:
                pass
            else:
                isvalid = self.comboBox.currentIndex()
                serail_no = self.result[0][0]
                save_time = self.result[0][1]
                sql = "update fixture_check set is_valid = {0} where serino = '{1}' and save_time = '{2}'".format(isvalid, serail_no, save_time)
                if len(self.textEdit_2.toPlainText()) > 0:
                    self.cur.execute(sql)
                    self.con.commit()
                    self.clearContent()
                    self.comboBox_model_2.setEnabled(1)
                    self.lineEdit_serino_2.setEnabled(1)
                    self.lineEdit_workerid_2.setEnabled(1)
                else:
                    QMessageBox.warning(self, '警告', '请选择状态变更原因！')
                    self.textEdit_2.setFocus()

    def checkPrivileges(self, usercode, curwork):      #检查当前账号是否有权限进行操作,usercode员工号，curwork当前工序id
        # if self.tabWidget.currentIndex() == 0:
        #     pass
        # elif self.tabWidget.currentIndex() == 1:
        #     pass
        # else:
        #     pass
        sql = "select `code`, user_privieges from user_access where `code` = '{}'".format(usercode)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        ncount = self.cur.rowcount
        if ncount == 0:
            return 0
        else:
            if len(result[0][-1]) == 9:             #防止有人用超级账号,导致程序崩溃
                if 1 != int(result[0][-1][curwork]):
                    return 0
                else:
                    return 1
            else:
                pass

    def selectProcessResult(self):
        self.process_result_ui = ProcessResult(self)
        self.process_result_ui.show()

        # print(self.tableWidget_3.currentRow())
        # print(self.tableWidget_3.item(self.tableWidget_3.currentRow(), 6).text())

    def choseModel3(self):      #测温板管理界面，当选择不同工序时出现的不同选项
        self.thermocoupleGridClear()
        if self.comboBox_model_3.currentIndex() == 0:       #新做
            #显示检查项目
            self.tableWidget_4.setRowCount(4)
            item_list = [['机种', '实际测温板是否与当前机种相同', '目视', 'N/A', ''], ['零件', '测温板上测温零件是否齐备', '目视', 'N/A', ''], ['测温线', '测温线是否符合要求', '目视', 'N/A', ''], \
                         ['PCB', 'PCB板是否完好', '目视', 'N/A', '']]
            #给检查项目增加判定按钮
            for i in range(len(item_list)):
                com_bt  = QComboBox(self)
                com_bt.addItem('合格')
                com_bt.addItem('不合格')
                com_bt.setEditable(1)
                com_bt.setCurrentIndex(-1)
                self.tableWidget_4.setCellWidget(i, 4, com_bt)
                for j in range(6):
                    if j != 4 and j !=5:
                        self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(item_list[i][j])))
                    elif j == 5:
                        self.tableWidget_4.setItem(i, j , QTableWidgetItem(''))
        elif self.comboBox_model.currentIndex() == 1:       #正在使用
            pass
        elif self.comboBox_model.currentIndex() == 2:       #报废
            pass
        else:
            pass

    def thermocoupleGridSave(self):     #测温板数据保存
        can = 1
        tg_worksite = self.comboBox_model_3.currentText()       #测温板工序
        tg_pcb = self.lineEdit_pcb_2.text()         #测温板pcb
        tg_machine = self.lineEdit_machineid_3.text()       #测温板机种
        tg_sn = self.lineEdit_serino_4.text()       #测温板sn
        tg_process = self.comboBox_board_2.currentText()        #制程段
        tg_worker = self.comboBox_result_3.currentText()        #制作人
        tg_thickness = self.comboBox_3.currentText()            #板厚
        tg_line = self.comboBox_2.currentText()                 #线别
        tg_manager = self.comboBox_auditor.currentText()        #审核人
        tg_notes = self.textEdit_3.toPlainText()                #备注

        if len(str(self.comboBox_model_3.currentText())) == 0 or len(tg_pcb) == 0 or len(tg_sn) == 0 or len(tg_machine) == 0 or \
        len(str(self.comboBox_board_2.currentIndex())) == 0 or len(str(self.comboBox_result_3.currentIndex())) == 0 or len(str(self.comboBox_3.currentIndex())) == 0 \
        or len(str(self.comboBox_2.currentIndex())) == 0 or len(str(self.comboBox_auditor.currentIndex())) == 0 or len(tg_manager) == 0:
            QMessageBox.warning(self, '警告', '当前信息输入不完整！')
        else:
            sql1 = "select serino, is_valid from fixture_check where model = '测温板' and serino = '{}' order by save_time desc limit 1".format(tg_sn)
            self.cur.execute(sql1)
            result1 = self.cur.fetchall()
            num = self.cur.rowcount
            if self.comboBox_model_3.currentIndex() == 0:  # 新做
                if num != 0:
                    QMessageBox.information(self, '提示', '当前编号的测温板已经存在')
                    self.thermocoupleGridClear()
                elif num == 0:
                    sql2 = "INSERT into fixture_check (model, pcb_lot, serino, status, machine_type, worker_id, gw_thickness, line, notes, process_name, manager_id, save_time) \
                    values ('测温板', '{0}', '{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}')".format(tg_pcb, tg_sn, 0, tg_machine, tg_worker, tg_thickness, tg_line, \
                    tg_notes, tg_process, tg_manager, self.getCurrentTime())
                    for z in range(self.tableWidget_4.rowCount()):
                        check_item = self.tableWidget_4.item(z, 0).text()                               # type: QTableWidgetItem
                        check_standard = self.tableWidget_4.item(z, 1).text()
                        check_tools = self.tableWidget_4.item(z, 2).text()
                        test_result = self.tableWidget_4.item(z, 3).text()
                        result = self.tableWidget_4.cellWidget(z, 4).currentText()
                        nots = self.tableWidget_4.item(z, 5).text()
                        serino = self.lineEdit_serino_4.text()
                        if len(result) == 0:
                            can = 0
                        else:
                            sql = "INSERT into check_process_result (serino, check_item, check_standard, check_tools, test_result, result, nots, save_time ) \
                            values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(serino, check_item, check_standard, check_tools, test_result, \
                            result, nots, self.getCurrentTime())
                            self.cur.execute(sql)
                    if can == 1:
                        print(sql2)
                        self.cur.execute(sql2)
                        self.con.commit()
                        self.thermocoupleGridClear()
                    else:
                        QMessageBox.warning(self, '警告', '检验项目未填写完成！')
                else:
                    self.thermocoupleGridClear()
            elif self.comboBox_model_3.currentIndex() == 1:
                if self.thermocoupleGridCanUse == 1:
                    if self.current_cwb_useage != 99:
                        sql2 = "INSERT into fixture_check (model, pcb_lot, serino, status, machine_type, worker_id, gw_thickness, line, notes, process_name, manager_id, save_time, use_age) \
                        values ('测温板', '{0}', '{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', {11})".format(tg_pcb, tg_sn, 1, tg_machine, tg_worker, tg_thickness, tg_line, \
                        tg_notes, tg_process, tg_manager, self.getCurrentTime(), self.current_cwb_useage+1)
                        self.cur.execute(sql2)
                    else:
                        sql2 = "INSERT into fixture_check (model, pcb_lot, serino, status, machine_type, worker_id, gw_thickness, line, notes, process_name, manager_id, save_time, use_age, is_valid) \
                        values ('测温板', '{0}', '{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', {11}, 2)".format(tg_pcb, tg_sn, 1, tg_machine, tg_worker, tg_thickness, tg_line, \
                        tg_notes, tg_process, tg_manager, self.getCurrentTime(), self.current_cwb_useage + 1)
                    self.con.commit()
                else:
                    QMessageBox.information(self, '提示', '当前编码的测温板已经停用或使用次数已用完！')
                self.thermocoupleGridClear()
            elif self.comboBox_model_3.currentIndex() == 2:
                if self.thermocoupleGridCanUse == 1:
                    sql2 = "INSERT into fixture_check (model, pcb_lot, serino, status, machine_type, worker_id, gw_thickness, line, notes, process_name, manager_id, save_time, use_age, is_valid) \
                    values ('测温板', '{0}', '{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', 2)".format(tg_pcb, tg_sn, 2, tg_machine, tg_worker, tg_thickness, tg_line, \
                    tg_notes, tg_process, tg_manager, self.getCurrentTime(), self.current_cwb_useage)
                    self.cur.execute(sql2)
                    self.con.commit()
                else:
                    QMessageBox.information(self, '提示', '当前编码的测温板已经停用或使用次数已用完！')
                self.thermocoupleGridClear()

            else:
                pass

    def thermocoupleGridClear(self):        #测温板管理清除功能
        if self.comboBox_model_3.currentIndex() == 0:
            self.lineEdit_pcb_2.clear()
            self.lineEdit_serino_4.clear()
            self.lineEdit_machineid_3.clear()
            self.comboBox_board_2.setCurrentIndex(-1)
            self.comboBox_result_3.setCurrentIndex(-1)
            self.comboBox_3.setCurrentIndex(-1)
            self.comboBox_2.setCurrentIndex(-1)
            self.label_39.setText('0')
            self.comboBox_auditor.setCurrentIndex(-1)
            self.textEdit_3.clear()

            n = self.tableWidget_4.rowCount()
            for i in range(n):
                self.tableWidget_4.cellWidget(i, 4).setCurrentIndex(-1)
                self.tableWidget_4.setItem(i, 5, QTableWidgetItem(''))

        else:
            self.tableWidget_4.clearContents()
            self.tableWidget_4.setRowCount(0)
            self.lineEdit_pcb_2.clear()
            self.lineEdit_serino_4.clear()
            self.lineEdit_machineid_3.clear()
            self.comboBox_board_2.setCurrentIndex(-1)
            self.comboBox_result_3.setCurrentIndex(-1)
            self.comboBox_3.setCurrentIndex(-1)
            self.comboBox_2.setCurrentIndex(-1)
            self.label_39.setText('0')
            self.comboBox_auditor.setCurrentIndex(-1)
            self.textEdit_3.clear()

    def thermocoupleGridsetValue(self):
        tg_sn = self.lineEdit_serino_4.text()
        sql = "select serino, is_valid, use_age, pcb_lot, machine_type, gw_thickness, line, process_name from fixture_check where model = '测温板' and serino = '{}' order by save_time desc limit 1".format(tg_sn)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        num = self.cur.rowcount
        if num == 1 and result[0][2] != 100 and result[0][1] == 0:         # 查询得到结果且使用次数不等于100且没有停用
            if result[0][2] is not None:
                self.current_cwb_useage = result[0][2]
            else:
                self.current_cwb_useage = 0
            if self.comboBox_model_3.currentIndex() == 1:
                self.thermocoupleGridCanUse = 1
                self.label_39.setText(str(self.current_cwb_useage))
            elif self.comboBox_model_3.currentIndex() == 2:
                self.thermocoupleGridCanUse = 1
                self.label_39.setText(str(self.current_cwb_useage))
                self.lineEdit_pcb_2.setText(result[0][3])
                self.lineEdit_machineid_3.setText(result[0][4])
                self.comboBox_board_2.setCurrentText(result[0][7])
                self.comboBox_3.setCurrentText(result[0][5])
                self.comboBox_2.setCurrentText(result[0][6])
        elif num == 0:
            pass
        else:
            QMessageBox.information(self, '提示', '当前编码的测温板已经停用或使用次数已用完！')
            self.thermocoupleGridCanUse = 0



class UserManagement(QWidget, usermanagement.Ui_Form):
    def __init__(self, parent):
        super(UserManagement, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('人员管理')
        self.setWindowIcon(QtGui.QIcon('user.ico'))

        self.pushButton.clicked.connect(self.userDel)
        self.pushButton_2.clicked.connect(self.userAdd)

        self.user_cur = parent.login_cur
        self.user_con = parent.login_con

        self.pushButton_3.clicked.connect(self.showUser)

    def userAdd(self):
        code = self.lineEdit_username.text()
        name = self.lineEdit_password.text()
        if code is not None and name is not None and len(code) > 0 and len(name) > 0:
            sql = "delete from user_access where code = '{0}' and name = '{1}'".format(code, name)
            self.user_cur.execute(sql)
            self.user_con.commit()
            self.label_3.setStyleSheet("color: rgb(0, 0, 255);")
            self.label_3.setText('删除员工信息成功')
            self.lineEdit_password.clear()
            self.lineEdit_username.clear()
            self.lineEdit_username.setFocus()
        else:
            QMessageBox.information(self, '提示', '删除员工必须输入正确的员工号和姓名')

    def userDel(self):
        user_privileges = ''
        code = self.lineEdit_username.text()
        name = self.lineEdit_password.text()
        if code is not None and name is not None and len(code) > 0 and len(name) > 0:
            checkbox_list = [self.checkBox_0, self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5, self.checkBox_6, self.checkBox_7, self.checkBox_8]
            for i in range(9):
                if checkbox_list[i].isChecked() == False:
                    user_privileges += '0'
                else:
                    user_privileges += '1'
            sql = "insert into user_access (code, name, user_privieges) values ('{0}', '{1}', '{2}')".format(code, name, user_privileges)
            try:
                self.user_cur.execute(sql)
                self.user_con.commit()
                self.label_3.setStyleSheet("color: rgb(0, 0, 255);")
                self.label_3.setText('添加员工信息成功')
                for j in range(9):
                    checkbox_list[j].setChecked(False)
            except Exception as e:
                self.label_3.setStyleSheet("color: rgb(255, 0, 0);")
                self.label_3.setText(str(e))
            self.lineEdit_password.clear()
            self.lineEdit_username.clear()
            self.lineEdit_username.setFocus()
        else:
            QMessageBox.information(self, '提示', '添加员工必须输入正确的员工号和姓名')

    def showUser(self):
        name = self.lineEdit_name.text()
        code = self.lineEdit_code.text()
        if len(name) > 0 and len(code) == 0:
            sql = "select `code`, `name`, user_privieges from user_access where `name` = '{}'".format(name)
        elif len(name) == 0 and len(code) > 0:
            sql = "select `code`, `name`, user_privieges from user_access where `code` = '{}'".format(code)
        elif len(name) > 0 and len(code) > 0:
            sql = "select `code`, `name`, user_privieges from user_access where `code` = '{0}' and `name` = '{1}'".format(code, name)
        else:
            pass
        self.user_cur.execute(sql)
        result = self.user_cur.fetchall()
        num = self.user_cur.rowcount
        if num > 0:
            self.tableWidget.setRowCount(num)
            for i in range(num):
                for j in range(3):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))


class UserManagementLogin(QWidget, login.Ui_Form):
    def __init__(self, parent):
        super(UserManagementLogin, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('人员权限管理登录')
        self.setWindowIcon(QtGui.QIcon('user.ico'))
        self.pushButton_in.clicked.connect(self.login)
        self.login_cur = parent.cur
        self.login_con = parent.con
        self.lineEdit_password.setEnabled(0)

    def login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        if username is not None and len(username) > 0:
            sql = "select user_privieges from user_access where code = {}".format(username)
            self.login_cur.execute(sql)
            login_result = self.login_cur.fetchall()
            if self.login_cur.rowcount == 0:
                pass
            else:
                if str(login_result[0][0]) == '0':
                    self.close()
                    self.user_ui = UserManagement(self)
                    self.user_ui.show()
                else:
                    QMessageBox.warning(self, '警告', '当前账号没有操作权限')


class ProcessResult(QMainWindow, processui.Ui_MainWindow):
    def __init__(self, parent):
        super(ProcessResult, self).__init__()
        self.setupUi(self)
        self.process_cur = parent.cur
        self.setWindowTitle('检查记录查询')
        self.setWindowIcon(QtGui.QIcon('ball.ico'))

        load_action = QAction(QtGui.QIcon('excel.ico'), '导出', self)
        load_action.triggered.connect(self.loadToExcel)
        self.menu.addAction(load_action)

        serial_no = parent.tableWidget_3.item(parent.tableWidget_3.currentRow(), 0).text()
        save_time = parent.tableWidget_3.item(parent.tableWidget_3.currentRow(), 6).text()
        sql = "select check_item, check_standard, check_tools, test_result, result, nots from check_process_result where \
        serino = '{0}' and save_time = '{1}'".format(serial_no, save_time)
        self.process_cur.execute(sql)
        self.result = self.process_cur.fetchall()
        self.tableWidget.setRowCount(self.process_cur.rowcount)
        for i in range(self.process_cur.rowcount):
            for j in range(6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))

    def loadToExcel(self):
        app = xlwings.App(visible=False, add_book=False)
        app.display_alerts=False
        app.screen_updating=False

        try:
            wb = app.books.add()                                     #type:xlwings.Book
            sht = wb.sheets.add('治具检验项目明细表')                 #type:xlwings.Sheet
            sht.range('A1').value = ['检查项目', '检验标准', '检验工具', '实际值', '判定结果', '备注']
            sht.range('A2').value = self.result
            wb.save('治具检验项目明细表.xlsx')
        finally:
            wb.close()
            app.quit()

# if __name__ == "__main__":
#         app = QApplication(sys.argv)
#         ui = FixtureControl()
#         ui.show()
#         sys.exit(app.exec_())