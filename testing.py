from PyQt5 import *

import sys
import time


class ServerThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self)

    def start_server(self):
        for i in range(1,6):
            time.sleep(1)
            self.emit(core.SIGNAL("dosomething(QString)"), str(i))

    def run(self):
        self.start_server()


class MainApp(QWidget):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)

        self.label = gui.QLabel("hello world!!")

        layout = gui.QHBoxLayout(self)
        layout.addWidget(self.label)

        self.thread = ServerThread()
        self.thread.start()

        self.connect(self.thread, core.SIGNAL("dosomething(QString)"), self.doing)

    def doing(self, i):
        self.label.setText(i)
        if i == "5":
            self.destroy(self, destroyWindow =True, destroySubWindows = True)
            sys.exit()


app = gui.QApplication(sys.argv)
form = MainApp()
form.show()
app.exec_()