from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from main import game
import sys


class Example(QWidget):
    def __init__(self):
        self.count = 0
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 400)
        self.setWindowTitle('Фокус со словами')
        self.btn_play = QPushButton('Играть', self)
        self.btn_play.resize(200, 40)
        self.btn_play.move(10, 20)
        self.btn_play.clicked.connect(self.play)
        self.btn_settings = QPushButton('Настройки', self)
        self.btn_settings.resize(200, 40)
        self.btn_settings.move(10, 70)
        self.btn_settings.clicked.connect(self.settings)
        self.btn_exit = QPushButton('Выйти', self)
        self.btn_exit.resize(200, 40)
        self.btn_exit.move(10, 120)
        self.btn_exit.clicked.connect(self.exit)

    def play(self):
        game()

    def settings(self):
        pass

    def exit(self):
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
