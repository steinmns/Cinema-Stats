#PyQT Dependencies
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout

#External Classes
from Classes.AddWindowClass import AddForm_Win
from Classes.SettingsWindowClass import Settings_Win
from Classes.HelpWindowClass import Help_Win
from Classes.EditWindowClass import EditForm_Win

#Icon and Styling Dependencies
import qtawesome as qta #Possibly make this only material icons at some point

#Database Dependencies
import mysql.connector

#Graphing Dependencies
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
matplotlib.style.use('ggplot')

#Database Credentials
dbConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="moviesheet"
)
#TODO: Add Pie chart widget to insights page
#TODO: Add edit and delete buttons
#TODO: Add automatic table refreshing
#TODO: Add another theme
#TODO: Add more graph theme options
#TODO: Add more graphs
#TODO: Need confirmation/error messages to indicate the status of an action (ex: Movie added successfully!)
#TODO: Add dynamic scaling aka some sort of layout
#TODO: Adhere to a variable/class naming protocol and generally organize code further
#TODO: Add table sorting info to help page
#TODO: Add more powerful features into the settings page (delete all data, load test data set)
#TODO: Edit and delete button will only work on "recent" page since they pull from that table, would be more useful on main log page for now, but will need a current tab finder eventually

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

        #Delete Button Setup
        delete_icon = qta.icon("mdi.trash-can-outline")
        self.DeleteButton = self.findChild(QtWidgets.QPushButton, 'DeleteButton')
        self.DeleteButton.setIcon(delete_icon)
        self.DeleteButton.clicked.connect(self.deleteEntry)

        #Edit Button Setup
        edit_icon = qta.icon('mdi.table-edit')
        self.EditButton = self.findChild(QtWidgets.QPushButton, 'EditButton')
        self.EditButton.setIcon(edit_icon)
        self.EditButton.clicked.connect(self.displayEditWindow)

        #Help Button Setup
        help_icon = qta.icon('mdi.help-circle-outline')
        self.HelpButton = self.findChild(QtWidgets.QPushButton, 'HelpButton')
        self.HelpButton.setIcon(help_icon)
        self.HelpButton.clicked.connect(self.displayHelpWindow)

        #layout = QVBoxLayout()  #DELETE ME
        #self.figure = plt.figure()
        #self.canvas = FigureCanvas(self.figure)
        self.generateGenrePie()
        #layout.addWidget(self.canvas)   #DELETE ME
        #self.setLayout(layout)  #DELETE ME

    def startup(self):
        self.refreshLastTenTable()
        self.refreshMainLogTable()
        entriesCount = self.getAllTimeCount()   #Probably could make this a one liner, but not sure how yet
        if(entriesCount[0][0] != 0):
            self.updateStats()

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

    def displayHelpWindow(self):
        #Displays the Help Window when the HelpButton is pressed
        helpWindow = Help_Win(self)
        if helpWindow.exec_():
            print("Success!")
        else:
            print("Closing Help Menu")

    def displayEditWindow(self):
        #Displays the Edit Window when the EditButton is pressed
        title = self.LastTenTable.item(self.LastTenTable.currentRow(), 0).text()
        date = self.LastTenTable.item(self.LastTenTable.currentRow(), 1).text()
        rating = self.LastTenTable.item(self.LastTenTable.currentRow(), 2).text()
        genre = self.LastTenTable.item(self.LastTenTable.currentRow(), 3).text()
        location = self.LastTenTable.item(self.LastTenTable.currentRow(), 4).text()
        comments = self.LastTenTable.item(self.LastTenTable.currentRow(), 5).text()
        
        editWin = EditForm_Win(self, title, date, rating, genre, location, comments) #, rating, genre, location, comments)
        #editWin = EditForm_Win(self, title)
        if editWin.exec_():
            print("Success!")
        else:
            print("Closing Edit Window") 

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
        self.LastTenTable.setColumnWidth(0, 220)
        self.LastTenTable.setColumnWidth(1, 75)
        self.LastTenTable.setColumnWidth(2, 50)
        self.LastTenTable.setColumnWidth(3, 90)
        self.LastTenTable.setColumnWidth(4, 65)
        self.LastTenTable.setColumnWidth(5, 307)
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
        self.MainLogTable.setColumnWidth(0, 220)
        self.MainLogTable.setColumnWidth(1, 75)
        self.MainLogTable.setColumnWidth(2, 50)
        self.MainLogTable.setColumnWidth(3, 90)
        self.MainLogTable.setColumnWidth(4, 65)
        self.MainLogTable.setColumnWidth(5, 307)
        self.MainLogTable.setHorizontalHeaderLabels(header) #Sets Column headings
        for row_number, row_data in enumerate(movies):    #Adds data from select statement to the table
            self.MainLogTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.MainLogTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))

    def deleteEntry(self):
        #Deletes a selected entry from the table
        title = self.LastTenTable.item(self.LastTenTable.currentRow(), 0).text()
        date = self.LastTenTable.item(self.LastTenTable.currentRow(), 1).text()
        #sql = "DELETE FROM log WHERE LOG_MOVIE_TITLE = %s AND WHERE LOG_MOVIE_DATE = %s"
        #vals = [title, date]
        sql = "DELETE FROM log WHERE LOG_MOVIE_TITLE = %s"
        vals = [title]
        cursor = dbConnection.cursor()
        cursor.execute(sql, vals)
        dbConnection.commit()
        cursor.close()

    def generateGenrePie(self):
        #Creates a pie chart of most watched genres
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
                counts[13] += 1
            elif row_data[1][0] == 'Sci-Fi':
                counts[14] += 1
            elif row_data[1][0] == 'Musical':
                counts[15] += 1
            else:
                print('Bad genre data: ' + str(row_data[1]))

        #Don't judge me for this -> this should remove the entries that have a count of zero so that they don't clutter the pie chart
        length = len(counts)
        for i in range(length):
            if(counts[i] == 0):
                genreLabels[i] = ""

        counts.remove(0)
        genreLabels.remove("")

        fig1, ax1 = plt.subplots()
        ax1.pie(counts, explode=None, labels=genreLabels, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        #plt.show()
        #self.figure.clear()
        #ax = self.figure.add_subplot(111)
        #ax.pie(counts, explode=None, labels=genreLabels)
        #ax.axis('equal')
        #self.canvas.draw()
        

    def getAllTimeMinRating(self):
        #Gets the Lowest Rating Logged
        sql = "SELECT MIN(LOG_MOVIE_RATING) FROM log"
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def getAllTimeMaxRating(self):
        #Gets the Highest Rating Logged
        sql = "SELECT MAX(LOG_MOVIE_RATING) FROM log"
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def getAllTimeAvgRating(self):
        #Gets the Average rating of all movies logged
        sql = "SELECT AVG(LOG_MOVIE_RATING) FROM log"
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def getAllTimeCount(self):
        #Gets the Count of all movies logged
        sql = "SELECT COUNT(LOG_ID) FROM log"
        cursor = dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def updateStats(self):
        #Gets the main page stats and displays them
        moviesWatched = self.getAllTimeCount()
        averageRating = self.getAllTimeAvgRating()
        highestRated = self.getAllTimeMaxRating()
        lowestRated = self.getAllTimeMinRating()
        self.MoviesWatchedLabel.setText('Movies Watched: ' + str(moviesWatched[0][0])) 
        self.AverageRatingLabel.setText('Average Rating: ' + str(int(averageRating[0][0])) + '/10') #Make this have one or two decimal points eventually
        self.HighestRatingLabel.setText('Highest Rating: ' + str(highestRated[0][0]) + '/10')
        self.LowestRatingLabel.setText('Lowest Rating: ' + str(lowestRated[0][0]) + '/10')
