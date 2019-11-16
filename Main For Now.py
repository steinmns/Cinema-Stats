#Imports
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import sys
import mysql.connector

#Database Credentials
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="moviesheet"
)

class Diag_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(Diag_Win, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('AddMovieForm.ui', self)   #Loads Add Movie Form Window

class Main_Win(QMainWindow):
    
    def __init__(self):
        #Constructor Method
        super(Main_Win, self).__init__()
        self.ui = uic.loadUi('MainWindowV1.ui', self)   #Loads Main Menu Window

        self.button = self.findChild(QtWidgets.QPushButton, 'AddMediaButton') 
        self.button.clicked.connect(self.displayAddMovieForm) 
        self.button = self.findChild(QtWidgets.QPushButton, 'SettingsButton') 
        self.button.clicked.connect(self.displaySettingsMenu)

    def displayAddMovieForm(self):
        # Displays the Add Movie Form when the AddMediaButton is pressed
        print('ADD BUTTON TEST')
        form1 = Diag_Win(self)
        if form1.exec_():
            print("Success!")
        else:
            print("Closing Add Form")

    def displaySettingsMenu(self):
        # Displays the Settings Menu when the SettingsButton is pressed
        print('SETTINGS BUTTON TEST')

    def insertMovie(self):
        #Inserts a new movie to the movie list
        sql = "INSERT INTO log (LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS) VALUES (%s, %s, %s, %s, %s, %s)"
        #vals = [self.] FIX THIS AND ADD CONTENTS OF ADD FORM
        mydb.cursor().execute(sql, vals)
        mydb.commit()




def startup():
    app = QApplication(sys.argv)    #System configs
    main_window = Main_Win()
    main_window.show()  #Displays the window
    sys.exit(app.exec_()) #Ensures clean exit when user closes window

startup() 