from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from Classes.QToasterClass import QToaster
import mysql.connector

#Database Credentials
dbConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="moviesheet"
)

class Settings_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(Settings_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('UI Files/SettingsMenu.ui', self)  

        #Save Button Setup
        self.saveSettingsButton = self.findChild(QtWidgets.QPushButton, 'SaveButton')
        self.saveSettingsButton.clicked.connect(self.updateSettings)   #Commented until the updateSettings method is filled out
        
        #Cancel Button Setup
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'CancelButton')
        self.cancelButton.clicked.connect(self.close) 

        self.appThemeVal = self.findChild(QtWidgets.QComboBox, 'ThemeDropdown')
        self.fontSizeVal = self.findChild(QtWidgets.QComboBox, 'FontSizeDropdown')
        self.graphThemeVal = self.findChild(QtWidgets.QComboBox, 'GraphThemeDropdown')

        currentSettings = self.getSettings()
        self.appThemeVal.setCurrentText(currentSettings[0][0])
        self.fontSizeVal.setCurrentText(currentSettings[0][1])
        self.graphThemeVal.setCurrentText(currentSettings[0][2])

    def updateSettings(self):
        #This will update the settings table so that the selected settings are saved
        sql = 'UPDATE settings SET SETTINGS_APP_THEME = %s, SETTINGS_FONT_SIZE = %s, SETTINGS_GRAPH_THEME = %s WHERE SETTINGS_ID = 1'
        vals = [self.appThemeVal.currentText(), self.fontSizeVal.currentText(), self.graphThemeVal.currentText()]
        cursor = dbConnection.cursor()
        cursor.execute(sql, vals)
        dbConnection.commit()
        cursor.close()
        print('Success!')
        QToaster.showMessage(self.parent(), 'Settings Updated', corner=QtCore.Qt.BottomRightCorner)
        self.close()

    def getSettings(self):
        #This will grab the settings val to load them in the main menu
        sql = 'SELECT SETTINGS_APP_THEME, SETTINGS_FONT_SIZE, SETTINGS_GRAPH_THEME FROM settings WHERE SETTINGS_ID = 1'
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult