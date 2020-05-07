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

            #Inserting into Main Log Table
            self.parent().MainLogTable.insertRow(self.parent().MainLogTable.rowCount()) #Using rowcount val since arrays start at 0 
            i = 1
            newRow = self.parent().MainLogTable.rowCount() - 1
            vals.pop() #Removes the IDVal from the list so it doesn't interfere with updating the Main Log table -> ID should never be updated
            for data in enumerate(vals):
                self.parent().MainLogTable.setItem(newRow, i, QtWidgets.QTableWidgetItem(str(data[1])))
                if(i < 6):
                    i += 1

            QToaster.showMessage(self.parent(), 'Entry Added', corner=QtCore.Qt.BottomRightCorner)
            self.close()
        else:
            print("Error: " + self.errorMessage)

    def validateSubmission(self):
        #Ensures that there are not errors with the movie entry being added
        if self.titleVal.text() == "" or self.titleVal.text() == None:
            self.errorMessage = "Please Enter a Title"
            QToaster.showMessage(self.parent(), self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.dateVal.date().toString() == None:
            self.errorMessage = "Please Enter a Date"
            QToaster.showMessage(self.parent(), self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.ratingVal.currentText() == None:
            self.errorMessage = "Please Enter a Rating"
            QToaster.showMessage(self.parent(), self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.genreVal.currentText() == None:
            self.errorMessage = "Please Enter a Genre"
            QToaster.showMessage(self.parent(), self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False

        if self.theaterChecked.isChecked() == True: 
            self.locationVal = "Theater"
        elif self.homeChecked.isChecked() == True:
            self.locationVal = "Home"
        else:
            self.locationVal = None

        return True #Indicates that the entry is good and can be inserted into the table

        
        
