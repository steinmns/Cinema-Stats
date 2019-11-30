#PyQT Dependencies
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

#External Classes
from Classes.AddWindowClass import AddForm_Win
from Classes.SettingsWindowClass import Settings_Win

#Icon and Styling Dependencies
import qtawesome as qta #Possibly make this only material icons at some point

#Database Dependencies
import mysql.connector

#Graphing Dependencies
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#Database Credentials
dbConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="moviesheet"
)
#TODO: Add Pie chart widget to insights page
#TODO: Format columns in tables
#TODO: Add edit and delete buttons
#TODO: Add automatic table refreshing
#TODO: Add another theme
#TODO: Add more graphs
#TODO: Add graph styling

class Main_Win(QMainWindow):
    
    def __init__(self):
        #Constructor Method
        super(Main_Win, self).__init__()
        self.ui = uic.loadUi('UI Files/MainWindowV1.ui', self)   #Loads Main Menu Window

        #Tab Icons
        hometab_icon = qta.icon('mdi.home-outline')
        logtab_icon = qta.icon('mdi.file-document-box-outline') #mdi.folder-text-outline
        insighttab_icon = qta.icon('mdi.chart-line')
        self.MainTabMenu.setTabIcon(0, hometab_icon)
        self.MainTabMenu.setTabIcon(1, logtab_icon)
        self.MainTabMenu.setTabIcon(2, insighttab_icon)

        #Table column default sizing ON HOLD FOR NOW
        #self.LastTenTable.setColumnWidth(1, 80)
        #self.LastTenTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        #Add Button Setup
        plus_icon = qta.icon('mdi.plus')
        self.Addbutton = self.findChild(QtWidgets.QPushButton, 'AddMediaButton') 
        self.Addbutton.setIcon(plus_icon)
        self.Addbutton.clicked.connect(self.displayAddMovieForm) 
        
        #Settings Button Setup
        settings_icon = qta.icon('mdi.settings-outline')
        self.Settingsbutton = self.findChild(QtWidgets.QPushButton, 'SettingsButton') 
        self.Settingsbutton.setIcon(settings_icon)
        self.Settingsbutton.clicked.connect(self.displaySettingsMenu)

    def displayAddMovieForm(self):
        # Displays the Add Movie Form when the AddMediaButton is pressed
        addForm = AddForm_Win(self)
        if addForm.exec_():
            print("Success!")
        else:
            #self.refreshLastTenTable()
            print("Closing Add Form")

    def displaySettingsMenu(self):
        # Displays the Settings Menu when the SettingsButton is pressed
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
        sql = "SELECT LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS FROM log ORDER BY LOG_MOVIE_DATE desc LIMIT 0, 10" #Selects top 10 results from the table
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        #self.LastTenTable.setRowCount(0)
        header = ["Title", "Date", "Rating", "Genre", "Location", "Comments"]
        self.LastTenTable.setColumnCount(6) #Sets column count to 6
        self.LastTenTable.setHorizontalHeaderLabels(header) #Sets Column headings
        for row_number, row_data in enumerate(myresult):    #Adds data from select statement to the table
            self.LastTenTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.LastTenTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))

    def getAllMovies(self):
        #Returns all of the movies logged
        sql = "SELECT LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS FROM log ORDER BY LOG_MOVIE_DATE desc"    #Selects all entries 
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def refreshMainLogTable(self):
        #Refreshes table with all movies logged
        movies = self.getAllMovies()
        header = ["Title", "Date", "Rating", "Genre", "Location", "Comments"]
        self.MainLogTable.setColumnCount(6) #Sets column count to 6
        self.MainLogTable.setHorizontalHeaderLabels(header) #Sets Column headings
        for row_number, row_data in enumerate(movies):    #Adds data from select statement to the table
            self.MainLogTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.MainLogTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))

    #def generateMoviesVersusTime(self):
        

    def generateGenrePie(self):
        sql = "SELECT LOG_MOVIE_GENRE FROM log"
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        genres = cursor.fetchall()
        cursor.close()
        counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        genreLabels = ['Drama', 'Romance', 'Documentary', 'Animated', 'Fantasy', 'Horror', 'Comedy', 'Thriller', 'Crime', 'Western', 'Adventure', 'Action', 'War', 'Biography', 'Sci-Fi', 'Musical']
        for row_data in enumerate(genres):
            if row_data[1][0] == 'Drama':
                counts[0] += 1
            elif row_data[1][0] == 'Romance':
                counts[1] += 1
            elif row_data[1][0] == 'Documentary':
                counts[2] += 1
            elif row_data[1][0] == 'Animated':
                counts[3] += 1
            elif row_data[1][0] == 'Fantasy':
                counts[4] += 1
            elif row_data[1][0] == 'Horror':
                counts[5] += 1
            elif row_data[1][0] == 'Comedy':
                counts[6] += 1
            elif row_data[1][0] == 'Thriller':
                counts[7] += 1
            elif row_data[1][0] == 'Crime':
                counts[8] += 1
            elif row_data[1][0] == 'Western':
                counts[9] += 1
            elif row_data[1][0] == 'Adventure':
                counts[10] += 1
            elif row_data[1][0] == 'Action':
                counts[11] += 1
            elif row_data[1][0] == 'War':
                counts[12] += 1
            elif row_data[1][0] == 'Biography':
                counts[13][0] += 1
            elif row_data[1][0] == 'Sci-Fi':
                counts[14] += 1
            elif row_data[1][0] == 'Musical':
                counts[15] += 1
            else:
                print('Bad genre data: ' + str(row_data[1]))
        fig1, ax1 = plt.subplots()
        ax1.pie(counts, explode=None, labels=genreLabels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()