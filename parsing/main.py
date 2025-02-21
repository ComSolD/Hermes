# from parser.MLB.odds import OddsMLB

from parser.MLB.parser import ParsingMLB

import logging
from interface.MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import sys

from function import Starter


class Statistic(Starter, QMainWindow):
    def __init__(self):
        super(Statistic, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Statistic")
        self.setWindowIcon(QIcon(':/icon/icon/monitor.png'))

        self.setAcceptDrops(True)
        

        self.MainWidget = QVBoxLayout(self.ui.MainWidget)

        self.starter()




if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        filename=".log",  # Логи будут записываться в файл
        encoding="utf-8",
    )

    logging.info("Программа запускается")

    # OddsMLB("2024-02-13","2024-02-13").get_matches_link()

    ParsingMLB("2024-03-20", "2024-03-20").date_cycle()

    # app = QApplication(sys.argv)

    # window = Statistic()
    # window.show()

    # sys.exit(app.exec())

    logging.info("Программа завершила работу")


    