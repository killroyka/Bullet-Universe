from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QSlider, QLabel, QDialog

from PyQt5.QtCore import Qt
from sounds import Sounds
import sys


class Menu(QMainWindow):
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
        pass

    def settings(self):
        self.next_window = Settings()
        self.next_window.show()
        self.close()

    def exit(self):
        exit()


class Settings(QDialog):
    def __init__(self, parent=None):
        self.sounds = Sounds()
        super().__init__(parent)
        self.button_go_back = QPushButton("Назад", self)
        self.button_go_back.clicked.connect(self.go_back)
        self.setWindowTitle('Настройки')
        self.setFixedSize(400, 300)
        self.sound_label = QLabel(self)
        self.sound_label.setText("Громкость:" + " " + str(self.sounds.get_volume()) + "%")
        self.sound_label.move(20, 40)
        self.slider_sound = QSlider(Qt.Horizontal, self)
        self.slider_sound.setGeometry(30, 70, 200, 30)
        self.slider_sound.setMinimum(0)
        self.slider_sound.setMaximum(100)
        self.slider_sound.setValue(self.sounds.get_volume())
        self.slider_sound.valueChanged.connect(self.volume_changed)

    def volume_changed(self, value):
        s = "Громкость:" + " " + str(value) + "%"
        self.sound_label.setText(s)
        self.sounds.set_volume(value)

    def go_back(self):
        self.next_window = Menu()
        self.next_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
