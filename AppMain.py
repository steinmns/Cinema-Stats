#Imports
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication
from Classes.MainWindowClass import Main_Win
import sys

def startup():
    app = QApplication(sys.argv)    #System configs
    main_window = Main_Win()
    main_window.show()  #Displays the window
    main_window.refreshLastTenTable()
    main_window.refreshMainLogTable()
    sys.exit(app.exec_()) #Ensures clean exit when user closes window
    
startup() 