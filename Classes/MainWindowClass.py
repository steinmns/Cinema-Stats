#PyQT Dependencies
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout

#External Classes
from Classes.AddWindowClass import AddForm_Win
from Classes.SettingsWindowClass import Settings_Win
from Classes.HelpWindowClass import Help_Win
from Classes.EditWindowClass import EditForm_Win
from Classes.QToasterClass import QToaster

#Icon and Styling Dependencies
import qtawesome as qta #Possibly make this only material icons at some point

#Database Dependencies
import mysql.connector

#Graphing Dependencies
import matplotlib
matplotlib.rcParams.update({'figure.autolayout': True}) #Fixes Graph Scaling issues --> replaces plt.tight_layout()
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

#Other Dependencies
import time
from datetime import datetime
import math

#Necessary Functionality
#TODO: Add another theme
#TODO: Add more graphs

#Bugs

#Nice to Haves (Lower Priority)
#TODO: Add dynamic scaling aka some sort of layout
#TODO: Adhere to a variable/class naming protocol and generally organize code further
#TODO: Add more powerful features into the settings page (delete all data, load test data set)

class Main_Win(QMainWindow):
    
    def __init__(self):
        #Constructor Method
        super(Main_Win, self).__init__()
        self.ui = uic.loadUi('UI Files/MainWindowV1.ui', self)   #Loads Main Menu Window

        #Database Credentials
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234",
            database="moviesheet"
        )

        #Tab Icons
        hometab_icon = qta.icon('mdi.home-outline')
        logtab_icon = qta.icon('mdi.file-document-box-outline') #mdi.folder-text-outline
        insighttab_icon = qta.icon('mdi.chart-line')
        importtab_icon = qta.icon('mdi.upload')
        self.MainTabMenu.setTabIcon(0, hometab_icon)
        self.MainTabMenu.setTabIcon(1, logtab_icon)
        self.MainTabMenu.setTabIcon(2, insighttab_icon)
        self.MainTabMenu.setTabIcon(3, importtab_icon)

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

        #Refresh Recent Button Setup
        refresh_icon = qta.icon('mdi.refresh')
        self.RefreshRecentButton = self.findChild(QtWidgets.QPushButton, 'RefreshRecentButton')
        self.RefreshRecentButton.setIcon(refresh_icon)
        self.RefreshRecentButton.clicked.connect(self.refreshLastTen)
        
        #Settings
        appSettings = Settings_Win(self).getSettings()
        matplotlib.style.use(appSettings[0][2])

        #Graph Generation
        layoutGP = QtWidgets.QVBoxLayout(self.GenrePiePlaceholder) 
        dynCanvasGP = FigureCanvas(Figure())
        layoutGP.addWidget(dynCanvasGP)
        self.dynAxGP = dynCanvasGP.figure.subplots()

        layoutMPM = QtWidgets.QVBoxLayout(self.TotalsGraphPlaceholder) 
        dynCanvasMPM = FigureCanvas(Figure())
        layoutMPM.addWidget(dynCanvasMPM)
        self.dynAxMPM = dynCanvasMPM.figure.subplots()

        #Update Flag
        self.changed = False

    def startup(self):
        #Methods that need to run right when the UI opens
        self.loadLastTenTable()
        self.loadMainLogTable()
        entriesCount = self.getAllTimeCount()   #Probably could make this a one liner, but not sure how yet
        if(entriesCount[0][0] != 0):
            self.updateStats()

    def displayAddMovieForm(self):
        # Displays the Add Movie Form when the AddMediaButton is pressed
        addForm = AddForm_Win(self)
        if addForm.exec_():
            print("Success!")
        else:
            print("Closing Add Form")
            if(self.changed == True):   #Only updates if an entry has actually been added
                self.refreshLastTen()
                self.refreshMainLog()
                self.updateStats()

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
        if(len(self.MainLogTable.selectedItems()) > 0):
            entryID = self.MainLogTable.item(self.MainLogTable.currentRow(), 0).text()
            title = self.MainLogTable.item(self.MainLogTable.currentRow(), 1).text()
            date = self.MainLogTable.item(self.MainLogTable.currentRow(), 2).text()
            rating = self.MainLogTable.item(self.MainLogTable.currentRow(), 3).text()
            genre = self.MainLogTable.item(self.MainLogTable.currentRow(), 4).text()
            location = self.MainLogTable.item(self.MainLogTable.currentRow(), 5).text()
            comments = self.MainLogTable.item(self.MainLogTable.currentRow(), 6).text()
            
            editWin = EditForm_Win(self, entryID, title, date, rating, genre, location, comments, self.MainLogTable.currentRow())
            if editWin.exec_():
                print("Success!")
            else:
                print("Closing Edit Window")
                if(self.changed == True):   #Only updates if an entry has actually been edited
                    self.refreshLastTen()
                    self.refreshMainLog()
                    self.updateStats()
        else:
            QToaster.showMessage(self, 'Please Select a Row', corner=QtCore.Qt.BottomRightCorner)

    def loadLastTenTable(self):
        #Loads table with last ten movies watched
        sql = "SELECT * FROM log ORDER BY LOG_MOVIE_DATE desc LIMIT 0, 10" #Selects top 10 results from the table
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        header = ["ID","Title", "Date", "Rating", "Genre", "Location", "Comments"]
        self.LastTenTable.setColumnCount(7) #Sets column count to 7
        self.LastTenTable.setColumnHidden(0, True)
        self.LastTenTable.setColumnWidth(1, 220)
        self.LastTenTable.setColumnWidth(2, 75)
        self.LastTenTable.setColumnWidth(3, 50)
        self.LastTenTable.setColumnWidth(4, 90)
        self.LastTenTable.setColumnWidth(5, 65)
        self.LastTenTable.setColumnWidth(6, 307)
        self.LastTenTable.setHorizontalHeaderLabels(header) #Sets Column headings
        for row_number, row_data in enumerate(myresult):    #Adds data from select statement to the table
            self.LastTenTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.LastTenTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))

    def getAllMovies(self):
        #Returns all of the movies logged
        sql = "SELECT * FROM log ORDER BY LOG_MOVIE_DATE desc"    #Selects all entries 
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def refreshLastTen(self):
        #Refreshes the table of recently watched movies after a new entry is added or a change
        #print('Refreshing Last10 Table') #For Debugging Purposes
        self.LastTenTable.clearContents()

        sql = "SELECT * FROM log ORDER BY LOG_MOVIE_DATE desc LIMIT 0, 10" #Selects top 10 results from the table
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        newTen = cursor.fetchall()
        cursor.close()

        for row_number, row_data in enumerate(newTen):    #Adds data from select statement to the table
            for column_number, data in enumerate(row_data):
                self.LastTenTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
                
    def refreshMainLog(self):
        #Refreshes the table of watched movies after a new entry is added or a change
        #print('Refreshing MainLog Table') #For Debugging Purposes
        self.MainLogTable.clearContents()

        sql = "SELECT * FROM log ORDER BY LOG_MOVIE_DATE desc" #Selects top 10 results from the table
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        newTen = cursor.fetchall()
        cursor.close()

        for row_number, row_data in enumerate(newTen):    #Adds data from select statement to the table
            for column_number, data in enumerate(row_data):
                self.MainLogTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))

    def loadMainLogTable(self):
        #Loads table with all movies logged
        movies = self.getAllMovies()
        header = ["ID","Title", "Date", "Rating", "Genre", "Location", "Comments"]
        self.MainLogTable.setColumnCount(7) #Sets column count to 7
        self.MainLogTable.setColumnHidden(0, True)  #Hides ID column because it clutters the table in the UI -> used exclusively for edit and delete operations
        self.MainLogTable.setColumnWidth(1, 220)
        self.MainLogTable.setColumnWidth(2, 75)
        self.MainLogTable.setColumnWidth(3, 50)
        self.MainLogTable.setColumnWidth(4, 90)
        self.MainLogTable.setColumnWidth(5, 65)
        self.MainLogTable.setColumnWidth(6, 307)
        self.MainLogTable.setHorizontalHeaderLabels(header) #Sets Column headings
        for row_number, row_data in enumerate(movies):    #Adds data from select statement to the table
            self.MainLogTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.MainLogTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))

    def deleteEntry(self):
        #Deletes a selected entry from the table
        if(len(self.MainLogTable.selectedItems()) > 0):
            entryID = self.MainLogTable.item(self.MainLogTable.currentRow(), 0).text()
            sql = "DELETE FROM log WHERE LOG_ID = %s"
            vals = [entryID]
            cursor = self.dbConnection.cursor()
            cursor.execute(sql, vals)
            self.dbConnection.commit()
            cursor.close()

            #Deleting from MainLogTable
            self.MainLogTable.removeRow(self.MainLogTable.currentRow())

            QToaster.showMessage(self, 'Entry Deleted', corner=QtCore.Qt.BottomRightCorner)
            
            self.refreshLastTen()
            self.refreshMainLog()
            self.updateStats()
        else:
            QToaster.showMessage(self, 'Please Select a Row', corner=QtCore.Qt.BottomRightCorner)

    def updateGPGraph(self):
        #Creates a pie chart of most watched genres
        self.dynAxGP.clear()
        sql = "SELECT LOG_MOVIE_GENRE FROM log"
        cursor = self.dbConnection.cursor()
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

        self.dynAxGP.pie(counts, explode=None, labels=genreLabels, startangle=90)
        self.dynAxGP.figure.canvas.draw()
   
    def getAllTimeMinRating(self):
        #Gets the Lowest Rating Logged
        sql = "SELECT MIN(LOG_MOVIE_RATING) FROM log"
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def getAllTimeMaxRating(self):
        #Gets the Highest Rating Logged
        sql = "SELECT MAX(LOG_MOVIE_RATING) FROM log"
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def getAllTimeAvgRating(self):
        #Gets the Average rating of all movies logged
        sql = "SELECT AVG(LOG_MOVIE_RATING) FROM log"
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def getAllTimeCount(self):
        #Gets the Count of all movies logged
        sql = "SELECT COUNT(LOG_ID) FROM log"
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def getAllTimeFavGenre(self):
        #Gets the Genre with the highest average rating
        #Drama 0 Romance 1 Documentary 2 Animated 3 Fantasy 4 Horror 5 Comedy 6 Thriller 7 Crime 8 Western 9 Adventure 10 Action 11 War 12 Biography 13 Sci-Fi 14 Musical 15
        sql = "SELECT LOG_MOVIE_RATING, LOG_MOVIE_GENRE FROM log ORDER BY LOG_MOVIE_GENRE ASC"
        cursor = self.dbConnection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        moviecount = self.getAllTimeCount()[0][0]
        threshold = int(moviecount/10)
        indexnumber = 0
        counts = [[0,'Drama'],[0,'Romance'],[0,'Documentary'],[0,'Animated'],[0,'Fantasy'],[0,'Horror'],[0,'Comedy'],[0,'Thriller'],[0,'Crime'],[0,'Western'],[0,'Adventure'],[0,'Action'],[0,'War'],[0,'Biography'],[0,'Sci-Fi'],[0,'Musical']]
        ratetotals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        while indexnumber < moviecount:
            if myresult[indexnumber][1] == 'Drama':
                counts[0][0] += 1
                ratetotals[0] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Romance':
                counts[1][0] += 1
                ratetotals[1] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Documentary':
                counts[2][0] += 1
                ratetotals[2] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Animated':
                counts[3][0] += 1
                ratetotals[3] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Fantasy':
                counts[4][0] += 1
                ratetotals[4] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Horror':
                counts[5][0] += 1
                ratetotals[5] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Comedy':
                counts[6][0] += 1
                ratetotals[6] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Thriller':
                counts[7][0] += 1
                ratetotals[7] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Crime':
                counts[8][0] += 1
                ratetotals[8] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Western':
                counts[9][0] += 1
                ratetotals[9] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Adventure':
                counts[10][0] += 1
                ratetotals[10] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Action':
                counts[11][0] += 1
                ratetotals[11] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'War':
                counts[12][0] += 1
                ratetotals[12] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Biography':
                counts[13][0] += 1
                ratetotals[13] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Sci-Fi':
                counts[14][0] += 1
                ratetotals[14] += myresult[indexnumber][0]
            elif myresult[indexnumber][1] == 'Musical':
                counts[15][0] += 1
                ratetotals[15] += myresult[indexnumber][0]
            indexnumber += 1
        avgbyGenre = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        countnumber = 0
        if moviecount > 25:
            while countnumber < len(counts):
                if counts[countnumber][0] < threshold:
                    del counts[countnumber]
                else:
                    avgbyGenre[countnumber] = (ratetotals[countnumber] / counts[countnumber][0])
        else:
            while countnumber < len(counts):
                if counts[countnumber][0] == 0:
                    avgbyGenre[countnumber] = 0
                else:
                    avgbyGenre[countnumber] = (ratetotals[countnumber] / counts[countnumber][0])
                countnumber += 1
        favGenreMax = max(avgbyGenre)
        favGenreIndex = avgbyGenre.index(favGenreMax) 
        return(counts[favGenreIndex][1])    

    def updateStats(self):
        #Gets the main page stats and displays them
        moviesWatched = self.getAllTimeCount()
        averageRating = self.getAllTimeAvgRating()
        highestRated = self.getAllTimeMaxRating()
        lowestRated = self.getAllTimeMinRating()
        favoriteGenre = self.getAllTimeFavGenre()
        self.updateMPMGraph()
        self.updateGPGraph()
        self.MoviesWatchedLabel.setText('Movies Watched: ' + str(moviesWatched[0][0])) 
        self.AverageRatingLabel.setText('Average Rating: ' + str(int(averageRating[0][0])) + '/10') #Make this have one or two decimal points eventually
        self.HighestRatingLabel.setText('Highest Rating: ' + str(highestRated[0][0]) + '/10')
        self.LowestRatingLabel.setText('Lowest Rating: ' + str(lowestRated[0][0]) + '/10')
        self.FavoriteGenreLabel.setText('Favorite Genre: ' + str(favoriteGenre))

    def getYearsMovies(self, year):
        #Gets all of the movies watched in a given year (Movies logged between Jan 1st and Dec 31st). Year should be all 4 digits
        sql = "SELECT LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS FROM log WHERE LOG_MOVIE_DATE BETWEEN %s AND %s ORDER BY LOG_MOVIE_DATE desc"    #Selects all entries 
        yearMin = year + '-01-01'
        yearMax = year + '-12-31'
        vals = [yearMin, yearMax]
        cursor = self.dbConnection.cursor()
        cursor.execute(sql,vals)
        myresult = cursor.fetchall()
        cursor.close()
        return myresult

    def updateMPMGraph(self, year = str(datetime.today().year)):
        #Generates graph to display how many movies are watched each month of the year. Year is optional and defaults to current year
        self.dynAxMPM.clear()
        annualMovies = self.getYearsMovies(year)
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        counts = [0,0,0,0,0,0,0,0,0,0,0,0]
        for movie in annualMovies:
            if movie[1].month == 1:
                counts[0] += 1
            elif movie[1].month == 2:
                counts[1] += 1
            elif movie[1].month == 3:
                counts[2] += 1
            elif movie[1].month == 4:
                counts[3] += 1
            elif movie[1].month == 5:
                counts[4] += 1
            elif movie[1].month == 6:
                counts[5] += 1
            elif movie[1].month == 7:
                counts[6] += 1
            elif movie[1].month == 8:
                counts[7] += 1
            elif movie[1].month == 9:
                counts[8] += 1
            elif movie[1].month == 10:
                counts[9] += 1
            elif movie[1].month == 11:
                counts[10] += 1
            elif movie[1].month == 12:
                counts[11] += 1

        self.dynAxMPM.set(xlabel='Month', ylabel='Movies Watched', title='Movies Per Month')
        self.dynAxMPM.plot(months, counts)
        self.dynAxMPM.grid(True)
        yRange = range(min(counts), math.ceil(max(counts))+1)       #Averages counts values for axis labels and prevents decimal values
        self.dynAxMPM.set_yticks(yRange)
        self.dynAxMPM.set_xticklabels(months, rotation='vertical')  #Makes tick labels vertical to save space
        self.dynAxMPM.figure.canvas.draw()                          #Refreshes Canvas
