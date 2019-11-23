from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

class Settings_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(Settings_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('UI Files/SettingsMenu.ui', self)   