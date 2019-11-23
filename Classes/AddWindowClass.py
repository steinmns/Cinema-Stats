from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

class AddForm_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(AddForm_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('UI Files/AddMovieForm.ui', self)   #Loads Add Movie Form Window
