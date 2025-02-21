from interface.MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon


class Parsing(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def parsing_data(self):
        self.ui.ParserLabel.setText("")

        from dictionary import ParserDictionary
        from parser.__init___ import ParsingNBA, OddsNBA, ParsingNFL, ParsingNHL, OddsNHL, ParsingMLB, OddsMLB

        if self.tournament == 'NFL':
            stage = self.ui.StageComboBox.currentText()
            parser_type = ParserDictionary.getDictionary('parsers_option', self.ui.TypeComboBox.currentText())

            if 'Week' in stage:
                get_num = stage.split()

                stage = [int(get_num[-1]), 2]
            else:
                stage = ParserDictionary.getDictionary('parsers_option', self.ui.StageComboBox.currentText())
            

            year = str(self.ui.YearDate.date().toPyDate()).split('-')
            year = year[0]

        if self.ui.OddsCheckBox.isChecked():
            parser_func = ParserDictionary.getDictionary('parsers', self.tournament, 'Odds')

            if self.ui.CurrentSeasonCheckBox.isChecked():
                if self.ui.DateOddsCheckBox.isChecked():
                    way = "now forward"
                else:
                    way = "now"
            elif self.ui.GetOddsCheckBox.isChecked():
                    way = "get"
            else:
                way = self.ui.FirstDate.date().year()

            
            exec(parser_func)

        else:
            parser_func = ParserDictionary.getDictionary('parsers', self.tournament, 'Espn')
            exec(parser_func)

        self.ui.ParserLabel.setText(f'Данные {self.tournament} собраны')


