__author__ = 'tpuctah'

import gevent
import gevent.monkey
gevent.monkey.patch_all()

from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_MainWindow
from PyQt5.Qt import Qt, QTimer, QFont, QKeySequence

import sys
import session
import pyte

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()

stream = pyte.Stream()
screen = pyte.Screen(200, 30)
stream.attach(screen)


def a(QKeyEvent):
    if QKeyEvent.key() == Qt.Key_Up:
        # for idx, line in enumerate(screen.display, 1):
        #     print(u"{0:2d} {1}".format(idx, line))

        for line in screen.buffer:
            for char in line:
                try:
                    if unicode(char.data) != u' ':
                        text = u"{},{},{};".format(unicode(char.data), unicode(char.bg), unicode(char.fg))
                        sys.stdout.write(text)
                except UnicodeEncodeError:
                     print 'error', char




    if QKeyEvent.key() == Qt.Key_Down:
        print 'down'
    #
    # if QKeyEvent.key() == Qt.Key_Escape:
    #     from IPython import embed
    #     embed()

    if QKeyEvent.key() == Qt.Key_V and QKeyEvent.modifiers() == Qt.ControlModifier:
        print 'as'
        ui.lineEdit.paste()

    print "nativeVirtualKey" + str(QKeyEvent.nativeVirtualKey())
    print "text" + QKeyEvent.text()
    print "key" + str(QKeyEvent.key())
    print "nativeModifiers" + str(QKeyEvent.nativeModifiers())
    print "nativeScanCode" + str(QKeyEvent.nativeScanCode())

    b(QKeyEvent)


def send():
    text = u"<span style='color:red'>{}</span>".format(ui.lineEdit.text())
    ui.plainTextEdit.appendHtml(text)
    data = ui.lineEdit.text()
    t = u"{}\n".format(data).encode('cp1251')
    session.send(t)
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


def gevent_pull():
    gevent.sleep(0)


def get_data_from_session():
    while True:
        line = session.get()
        stream.feed(line.decode('cp1251')+u'\n\r')
        ui.plainTextEdit.appendPlainText(line.decode('cp1251'))

gevent.spawn(get_data_from_session)

timer = QTimer()
timer.timeout.connect(gevent_pull)
timer.start(0)



result = app.exec_()
sys.exit(result)
