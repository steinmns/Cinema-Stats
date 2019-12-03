from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import mysql.connector

#Database Credentials
dbConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="moviesheet"
)

class EditForm_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(EditForm_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('UI Files/EditMovieForm.ui', self)   #Loads Edit Movie Form Window
        #self.DateWatchedEntry.setDate(QtCore.QDate.currentDate())

        #Definitions for add form entry fields
        self.submitButton = self.findChild(QtWidgets.QPushButton, 'SubmitButton')
        self.submitButton.clicked.connect(self.updateMovie)
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'CancelEntryButton')
        self.cancelButton.clicked.connect(self.close)

        self.titleVal = self.findChild(QtWidgets.QLineEdit, 'MovieTitleEntry')
        self.dateVal = self.findChild(QtWidgets.QDateEdit, 'DateWatchedEntry')
        self.ratingVal = self.findChild(QtWidgets.QComboBox, 'MovieRatingEntry')
        self.genreVal = self.findChild(QtWidgets.QComboBox, 'MovieGenreEntry')
        self.theaterChecked = self.findChild(QtWidgets.QRadioButton, 'MovieLocationTheaterEntry')
        self.homeChecked = self.findChild(QtWidgets.QRadioButton, 'MovieLocationHomeEntry')
        self.commentVal = self.findChild(QtWidgets.QPlainTextEdit, 'MovieCommentsEntry')
        self.errorMessage = ""
        self.locationVal = ""

    def updateMovie(self):
        #Updates a movie entry
        if self.validateSubmission() == True:
            sql = "UPDATE WHERE"
            vals = [self.titleVal.text(), self.dateVal.date().toString('yyyy-MM-dd'), self.ratingVal.currentText(), self.genreVal.currentText(), self.locationVal, self.commentVal.toPlainText()] 
            cursor = dbConnection.cursor()
            cursor.execute(sql, vals)
            dbConnection.commit()
            cursor.close()
            print('Success!')
            self.close()
        else:
            print("Error: " + self.errorMessage)

    def validateSubmission(self):
        #Ensures that there are not errors with the movie entry being edited
        if self.titleVal.text() == "" or self.titleVal.text() == None:
            self.errorMessage = "Title is Null"
            return False
        if self.dateVal.date().toString() == None:
            self.errorMessage = "Date is Null"
            return False
        if self.ratingVal.currentText() == None:
            self.errorMessage = "Rating is Null"
            return False
        if self.genreVal.currentText() == None:
            self.errorMessage = "Genre is Null"
            return False

        if self.theaterChecked.isChecked() == True: 
            self.locationVal = "Theater"
        elif self.homeChecked.isChecked() == True:
            self.locationVal = "Home"
        else:
            self.locationVal = None

        return True 

        
        
