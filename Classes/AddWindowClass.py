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

class AddForm_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(AddForm_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('UI Files/AddMovieForm.ui', self)   #Loads Add Movie Form Window
        self.DateWatchedEntry.setDate(QtCore.QDate.currentDate())

        #Definitions for add form entry fields
        self.submitButton = self.findChild(QtWidgets.QPushButton, 'SubmitButton')
        self.submitButton.clicked.connect(self.insertMovie)
        #self.submitButton.clicked.connect(self.printSubmission)
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

    def printSubmission(self):
        print("In form validation")
        print("Title: " + self.titleVal.text())
        print("Date: " + self.dateVal.date().toString('yyyy-MM-dd'))
        print("Rating: " + self.ratingVal.currentText())
        print("Genre: " + self.genreVal.currentText())
        if self.theaterChecked.isChecked() == True: #is there a more concise way to handle this?
            print("Location: Theater")
        elif self.homeChecked.isChecked() == True:
            print("Location: Home")
        else:
            print("Location: Not Specified")
        print("Comment: " + self.commentVal.toPlainText())

    def insertMovie(self):
        #Inserts a new movie to the movie list
        if self.validateSubmission() == True:
            sql = "INSERT INTO log (LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS) VALUES (%s, %s, %s, %s, %s, %s)"
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

        return True #Indicates that the entry is good and can be inserted into the table

        
        
