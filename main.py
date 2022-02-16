from PyQt5 import QtWidgets, uic
import sys
import threading
import time

from PyQt5.QtWidgets import QLCDNumber


class Job(threading.Thread):

    def __init__(self, lcd: QLCDNumber):
        super().__init__()
        self.__flag = threading.Event()
        self.__running = threading.Event()
        self.__running.set()
        self.lcd = lcd
        self.current_time_100 = 0
        self.lcd.display("0.0")

    def run(self):
        while self.__running.is_set():
            while self.__flag.is_set():
                self.lcd.display(round(self.current_time_100 / 10, 2))
                time.sleep(0.1)
                self.current_time_100 += 1
        print("Thread stopped")

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.clear()
        self.__running.clear()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()

    j_1 = Job(window.number_1)
    j_2 = Job(window.number_2)
    j_3 = Job(window.number_3)

    j_1.start()
    j_2.start()
    j_3.start()

    window.start_1.clicked.connect(lambda state: j_1.resume())
    window.start_2.clicked.connect(lambda state: j_2.resume())
    window.start_3.clicked.connect(lambda state: j_3.resume())

    window.pause_1.clicked.connect(lambda state: j_1.pause())
    window.pause_2.clicked.connect(lambda state: j_2.pause())
    window.pause_3.clicked.connect(lambda state: j_3.pause())

    window.stop_1.clicked.connect(lambda state: j_1.stop())
    window.stop_2.clicked.connect(lambda state: j_2.stop())
    window.stop_3.clicked.connect(lambda state: j_3.stop())

    app.exec_()
