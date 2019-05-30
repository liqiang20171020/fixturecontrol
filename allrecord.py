import allUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction
from PyQt5.QtGui import QIcon
import sys
import inpic
import fixturecontrol

class AllUI(QMainWindow, allUI.Ui_MainWindow):
    def __init__(self):
        super(AllUI, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('绑定软件')
        self.item_bar = QMenuBar(self)
        self.item_bar.addMenu('权限管理')
        self.item_bar.addMenu(QIcon('ball.ico'), '权限管理1')
        self.setMenuBar(self.item_bar)

        self.pushButton.clicked.connect(self.showfix)

    def showfix(self):
        self.ui = fixturecontrol.FixtureControl()
        self.ui.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = AllUI()
    ui.show()
    sys.exit(app.exec_())
