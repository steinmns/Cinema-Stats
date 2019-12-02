from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import qtawesome as qta #Possibly make this only material icons at some point

class Help_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(Help_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('UI Files/HelpWidget.ui', self)  

        #Add Button Setup
        plus_icon = qta.icon('mdi.plus')
        self.HelpAddbutton = self.findChild(QtWidgets.QPushButton, 'HelpAddButton') 
        self.HelpAddbutton.setIcon(plus_icon)

        #Settings Button Setup
        settings_icon = qta.icon('mdi.settings-outline')
        self.HelpSettingsbutton = self.findChild(QtWidgets.QPushButton, 'HelpSettingsButton') 
        self.HelpSettingsbutton.setIcon(settings_icon)

        #Delete Button Setup
        delete_icon = qta.icon("mdi.trash-can-outline")
        self.HelpDeleteButton = self.findChild(QtWidgets.QPushButton, 'HelpDeleteButton')
        self.HelpDeleteButton.setIcon(delete_icon)

        #Edit Button Setup
        edit_icon = qta.icon('mdi.table-edit')
        self.HelpEditButton = self.findChild(QtWidgets.QPushButton, 'HelpEditButton')
        self.HelpEditButton.setIcon(edit_icon)

        #Close Button
        self.CloseButton = self.findChild(QtWidgets.QPushButton, 'CloseHelpButton')
        self.CloseButton.clicked.connect(self.close)

        