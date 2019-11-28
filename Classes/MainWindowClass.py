from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from Classes.AddWindowClass import AddForm_Win
from Classes.SettingsWindowClass import Settings_Win
import qtawesome as qta #Possibly make this only material icons at some point
import mysql.connector

#Database Credentials
dbConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="moviesheet"
)

class Main_Win(QMainWindow):
    
    def __init__(self):
        #Constructor Method
        super(Main_Win, self).__init__()
        self.ui = uic.loadUi('UI Files/MainWindowV1.ui', self)   #Loads Main Menu Window

        plus_icon = qta.icon('mdi.plus')
        self.Addbutton = self.findChild(QtWidgets.QPushButton, 'AddMediaButton') 
        self.Addbutton.setIcon(plus_icon)
        self.Addbutton.clicked.connect(self.displayAddMovieForm) 
        
        settings_icon = qta.icon('mdi.settings-outline')
        self.Settingsbutton = self.findChild(QtWidgets.QPushButton, 'SettingsButton') 
        self.Settingsbutton.setIcon(settings_icon)
        self.Settingsbutton.clicked.connect(self.displaySettingsMenu)

    def displayAddMovieForm(self):
        # Displays the Add Movie Form when the AddMediaButton is pressed
        #print('ADD BUTTON TEST')
        addForm = AddForm_Win(self)
        if addForm.exec_():
            print("Success!")
        else:
            #self.refreshLastTenTable()
            print("Closing Add Form")
            #Possibly have values from form grabbed here

    def displaySettingsMenu(self):
        # Displays the Settings Menu when the SettingsButton is pressed
        #print('SETTINGS BUTTON TEST')
        settingsMenu = Settings_Win(self)
        if settingsMenu.exec_():
            print("Success!")
        else:
            print("Closing Settings Menu")

    def validateInsertVals(self, vals):
        #if(self.)
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
        #self.LastTenTable.setRowCount(0)
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