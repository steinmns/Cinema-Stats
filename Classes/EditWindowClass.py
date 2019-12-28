from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from Classes.QToasterClass import QToaster
from datetime import datetime
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
        super(EditForm_Win, self).__init__()    #*args and *kwargs removed from super init
        self.ui = uic.loadUi('UI Files/EditMovieForm.ui', self)   #Loads Edit Movie Form Window

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

        #Populates edit form with current entry info
        self.parentWin = args[0]
        self.oldTitleVal = args[1]  #Used in where clause to find the correct movie in the log to update -> only necessary until I get this updating on ID
        self.titleVal.setText(args[1])
        self.dateVal.setDate((datetime.strptime(args[2], '%Y-%m-%d')).date())  #Converts date string to date object
        self.ratingVal.setCurrentText(args[3])
        self.genreVal.setCurrentText(args[4])
        self.locationVal = args[5]
        self.commentVal.setPlainText(args[6])
        self.curRow = args[7]
        if(self.locationVal == 'Home'):
            self.homeChecked.setChecked(True)
        elif(self.locationVal == 'Theater'):
            self.theaterChecked.setChecked(True)

    def updateMovie(self):
        #Updates a movie entry
        #THIS NEEDS A WAY TO GET MOVIE BY ID BECAUSE IT CANNOT HANDLE DUPLICATES CURRENTLY
        if self.validateSubmission() == True:
            sql = "UPDATE log SET LOG_MOVIE_TITLE = %s, LOG_MOVIE_DATE = %s, LOG_MOVIE_RATING = %s, LOG_MOVIE_GENRE = %s, LOG_MOVIE_LOCATION = %s, LOG_MOVIE_COMMENTS = %s WHERE LOG_MOVIE_TITLE = %s"
            vals = [self.titleVal.text(), self.dateVal.date().toString('yyyy-MM-dd'), self.ratingVal.currentText(), self.genreVal.currentText(), self.locationVal, self.commentVal.toPlainText(), self.oldTitleVal ] 
            cursor = dbConnection.cursor()
            cursor.execute(sql, vals)
            dbConnection.commit()
            cursor.close()
            
            #Updating Main Log Table
            i = 0
            vals.pop() #Removes the old title from the list so it doesn't interfere with updating the Main Log table
            for data in enumerate(vals):
                self.parentWin.MainLogTable.setItem(self.curRow, i, QtWidgets.QTableWidgetItem(data[1]))
                if(i < 5):
                    i += 1

            QToaster.showMessage(self.parentWin, 'Entry Updated', corner=QtCore.Qt.BottomRightCorner)
            self.close()
        else:
            print("Error: " + self.errorMessage)

    def validateSubmission(self):
        #Ensures that there are not errors with the movie entry being edited
        if self.titleVal.text() == "" or self.titleVal.text() == None:
            self.errorMessage = "Please Enter a Title"
            QToaster.showMessage(self.parentWin, self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.dateVal.date().toString() == None:
            self.errorMessage = "Please Enter a Date"
            QToaster.showMessage(self.parentWin, self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.ratingVal.currentText() == None:
            self.errorMessage = "Please Enter a Rating"
            QToaster.showMessage(self.parentWin, self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.genreVal.currentText() == None:
            self.errorMessage = "Please Enter a Genre"
            QToaster.showMessage(self.parentWin, self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False

        if self.theaterChecked.isChecked() == True: 
            self.locationVal = "Theater"
        elif self.homeChecked.isChecked() == True:
            self.locationVal = "Home"
        else:
            self.locationVal = None

        return True 

        
        
