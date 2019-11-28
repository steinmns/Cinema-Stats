from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

class Settings_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(Settings_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('UI Files/SettingsMenu.ui', self)  

        self.saveSettingsButton = self.findChild(QtWidgets.QPushButton, 'SaveButton')
        #self.saveSettingsButton.clicked.connect(self.updateSettings)   #Commented until the updateSettings method is filled out
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'CancelButton')
        self.cancelButton.clicked.connect(self.close) 

    #def updateSettings(self):
        #This will update the settings table so that the selected settings are saved