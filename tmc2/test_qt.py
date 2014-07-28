__author__ = 'tpuctah'

import sys
import gevent
import gevent.monkey
gevent.monkey.patch_all()

from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_MainWindow
from PyQt5.Qt import Qt, QTimer, QFont

import sys
import telnetlib

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()


def a(QKeyEvent):
    if QKeyEvent.key() == Qt.Key_Up:
        print 'up'
    if QKeyEvent.key() == Qt.Key_Down:
        print 'down'
    b(QKeyEvent)


def send():
    text = u"<span style='color:red'>{}</span>".format(ui.lineEdit.text())
    ui.plainTextEdit.appendHtml(text)
    data = ui.lineEdit.text()
    t = u"{}\n".format(data).encode('cp1251')
    tn.write(t)
    ui.lineEdit.clear()


ui.setupUi(window)
ui.lineEdit.returnPressed.connect(send)
b = ui.lineEdit.keyPressEvent
ui.lineEdit.keyPressEvent = a

ui.plainTextEdit.document().setMaximumBlockCount(10000)
ui.plainTextEdit.setReadOnly(True)
ui.plainTextEdit.setCenterOnScroll(False)

font = QFont("Droid Sans Mono", 11)
ui.plainTextEdit.setFont(font)

window.show()

tn = telnetlib.Telnet('arda.pp.ru', 4000)
tn.set_debuglevel(100)


def telnet():
    while True:
        data = tn.read_some()
        if data:
            data = data.replace('\n\r', '\n')
            ui.plainTextEdit.insertPlainText(data.decode('cp1251'))
        gevent.sleep(0)


telnet = gevent.spawn(telnet)


def gevent_pull():
    gevent.sleep(0)

timer = QTimer()
timer.timeout.connect(gevent_pull)
timer.start(0)

result = app.exec_()
telnet.kill()
sys.exit(result)
