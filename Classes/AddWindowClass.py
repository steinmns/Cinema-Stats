from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

class AddForm_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(AddForm_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('UI Files/AddMovieForm.ui', self)   #Loads Add Movie Form Window

        #Definitions for add form entry fields
        self.submitbutton = self.findChild(QtWidgets.QPushButton, 'SubmitButton')
        self.submitbutton.clicked.connect(self.validateSubmission)
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'CancelButton')
        self.cancelbutton.clicked.connect(self.closeAddForm)

        self.titleVal = self.findChild(QtWidgets.QLineEdit, 'MovieTitleEntry')
        self.dateVal = self.findChild(QtWidgets.QDateEdit, 'DateWatchedEntry')
        self.ratingVal = self.findChild(QtWidgets.QComboBox, 'MovieRatingEntry')
        self.genreVal = self.findChild(QtWidgets.QComboBox, 'MovieGenreEntry')
        self.theaterChecked = self.findChild(QtWidgets.QRadioButton, 'MovieLocationTheaterEntry')
        self.homeChecked = self.findChild(QtWidgets.QRadioButton, 'MovieLocationHomeEntry')
        self.commentVal = self.findChild(QtWidgets.QPlainTextEdit, 'MovieCommentsEntry')

    def validateSubmission(self):
        print("In form validation")
        print("Title: " + self.titleVal.text())
        print("Date: " + self.dateVal.date().toString())
        print("Rating: " + self.ratingVal.currentText())
        print("Genre: " + self.genreVal.currentText())
        if self.theaterChecked.isChecked() == True: #is there a more concise way to handle this?
            print("Location: Theater")
        elif self.homeChecked.isChecked() == True:
            print("Location: Home")
        else:
            print("Location: Not Specified")
        print("Comment: " + self.commentVal.toPlainText())
        
