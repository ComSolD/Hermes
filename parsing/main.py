from parser.NBA.odds import OddsNBA

from parser.NBA.parser import ParsingNBA

# from interface.MainWindow import Ui_MainWindow

# from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon

# import sys

# from function import Starter


# class Statistic(Starter, QMainWindow):
#     def __init__(self):
#         super(Statistic, self).__init__()

#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setWindowTitle("Statistic")
#         self.setWindowIcon(QIcon(':/icon/icon/monitor.png'))

#         self.setAcceptDrops(True)
        

#         self.MainWidget = QVBoxLayout(self.ui.MainWidget)

#         self.starter()




if __name__ == "__main__":

    OddsNBA("get","21-02-2025").get_matches_link()
    
    # ParsingNBA("2024-10-04", "2024-10-04").date_cycle()

    # app = QApplication(sys.argv)

    # window = Statistic()
    # window.showFullScreen()
    # window.show()

    # sys.exit(app.exec())




    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s [%(levelname)s] %(message)s",
    #     filename=".log",  # Логи будут записываться в файл
    #     encoding="utf-8",
    # )

    # logging.info("Программа запускается")

    # ParsingNFL('2023', [5, 3], 'past').date_cycle()
    
    # logging.info("Программа завершила работу")