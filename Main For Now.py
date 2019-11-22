#Imports
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import sys
import mysql.connector

#Database Credentials
dbConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="moviesheet"
)

class Diag_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(Diag_Win, self).__init__(*args, **kwargs)

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
        #print('ADD BUTTON TEST')
        addForm = Diag_Win(self)
        addForm.ui = uic.loadUi('AddMovieForm.ui', addForm)   #Loads Add Movie Form Window
        if addForm.exec_():
            print("Success!")
        else:
            print("Closing Add Form")
            #Possibly have values from form grabbed here

    def displaySettingsMenu(self):
        # Displays the Settings Menu when the SettingsButton is pressed
        #print('SETTINGS BUTTON TEST')
        settingsMenu = Diag_Win(self)
        settingsMenu.ui = uic.loadUi('SettingsMenu.ui', settingsMenu)   #Loads Settings Menu
        if settingsMenu.exec_():
            print("Success!")
        else:
            print("Closing Settings Menu")

    def insertMovie(self):
        #Inserts a new movie to the movie list
        sql = "INSERT INTO log (LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS) VALUES (%s, %s, %s, %s, %s, %s)"
        #vals = [self.] FIX THIS AND ADD CONTENTS OF ADD FORM
        #mydb.cursor().execute(sql, vals)
        #mydb.commit()

    def validateInsertVals(self, vals):
        if(self.)
        print("This Will validate the form eventually")
    
    def refreshLastTenTable(self):
        #Refreshes table with last ten movies watched
        #Should be called every time the insertMovie() is successfully called if the current tab is "Home"
        sql = "SELECT LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS FROM log LIMIT 0, 10" #Selects top 10 results from the table
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        #print(myresult)
        #print(cursor.rowcount)
        header = ["Title", "Date", "Rating", "Genre", "Location", "Comments"]
        self.LastTenTable.setColumnCount(6) #Sets column count to 6
        self.LastTenTable.setHorizontalHeaderLabels(header) #Sets Column headings
        for row_number, row_data in enumerate(myresult):    #Adds data from select statement to the table
            self.LastTenTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.LastTenTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))

    def refreshMainLogTable(self):
        #Refreshes table with last ten movies watched
        sql = "SELECT LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS FROM log"    #Selects all entries 
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        header = ["Title", "Date", "Rating", "Genre", "Location", "Comments"]
        self.MainLogTable.setColumnCount(7) #Sets column count to 6
        self.MainLogTable.setHorizontalHeaderLabels(header) #Sets Column headings
        for row_number, row_data in enumerate(myresult):    #Adds data from select statement to the table
            self.MainLogTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.MainLogTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))



def startup():
    app = QApplication(sys.argv)    #System configs
    main_window = Main_Win()
    main_window.show()  #Displays the window
    main_window.refreshLastTenTable()
    sys.exit(app.exec_()) #Ensures clean exit when user closes window
    

startup() 