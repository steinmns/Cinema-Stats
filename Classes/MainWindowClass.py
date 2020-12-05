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
import calendar

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
            rewatch = self.MainLogTable.item(self.MainLogTable.currentRow(), 7).text()
            
            editWin = EditForm_Win(self, entryID, title, date, rating, genre, location, comments, rewatch, self.MainLogTable.currentRow())
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
        header = ["ID","Title", "Date", "Rating", "Genre", "Location", "Comments", "Rewatch"]
        self.LastTenTable.setColumnCount(8) #Sets column count to 7
        self.LastTenTable.setColumnHidden(0, True)
        self.LastTenTable.setColumnWidth(1, 220)
        self.LastTenTable.setColumnWidth(2, 75)
        self.LastTenTable.setColumnWidth(3, 50)
        self.LastTenTable.setColumnWidth(4, 90)
        self.LastTenTable.setColumnWidth(5, 65)
        self.LastTenTable.setColumnWidth(6, 307)
        self.LastTenTable.setColumnWidth(7, 60.5)
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
        header = ["ID","Title", "Date", "Rating", "Genre", "Location", "Comments", "Rewatch"]
        self.MainLogTable.setColumnCount(8) #Sets column count to 8
        self.MainLogTable.setColumnHidden(0, True)  #Hides ID column because it clutters the table in the UI -> used exclusively for edit and delete operations
        self.MainLogTable.setColumnWidth(1, 220)
        self.MainLogTable.setColumnWidth(2, 75)
        self.MainLogTable.setColumnWidth(3, 50)
        self.MainLogTable.setColumnWidth(4, 90)
        self.MainLogTable.setColumnWidth(5, 65)
        self.MainLogTable.setColumnWidth(6, 307)
        self.MainLogTable.setColumnWidth(7, 63)
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
            
            entriesCount = self.getAllTimeCount()   #Probably could make this a one liner, but not sure how yet
            if(entriesCount[0][0] != 0):
                self.updateStats()
                self.refreshLastTen()
                self.refreshMainLog()
            
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
        genreDict = {'Drama':0, 'Romance':0, 'Documentary':0, 'Animated':0, 'Fantasy':0, 'Horror':0, 'Comedy':0, 'Thriller':0, 'Crime':0,
         'Western':0, 'Adventure':0, 'Action':0, 'War':0, 'Biography':0, 'Sci-Fi':0, 'Musical':0}
        for row_data in enumerate(genres):
            if row_data[1][0] in genreDict:
                genreDict[row_data[1][0]] +=1
            else:
                print('Bad genre data: ' + str(row_data[1]))

        genreDict = {key:val for key,val in genreDict.items() if val!=0}

        self.dynAxGP.pie(genreDict.values(), explode=None, labels=genreDict.keys(), startangle=90)
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
        movies = cursor.fetchall()
        cursor.close()
        threshold = int(len(movies)/10)
        genreCounts = {'Drama':0, 'Romance':0, 'Documentary':0, 'Animated':0, 'Fantasy':0, 'Horror':0, 'Comedy':0, 'Thriller':0, 'Crime':0,
         'Western':0, 'Adventure':0, 'Action':0, 'War':0, 'Biography':0, 'Sci-Fi':0, 'Musical':0}
        genreTotals = {'Drama':0, 'Romance':0, 'Documentary':0, 'Animated':0, 'Fantasy':0, 'Horror':0, 'Comedy':0, 'Thriller':0, 'Crime':0,
         'Western':0, 'Adventure':0, 'Action':0, 'War':0, 'Biography':0, 'Sci-Fi':0, 'Musical':0}
        for movie in movies:
            if movie[1] in genreCounts:
                genreCounts[movie[1]] +=1
                genreTotals[movie[1]] += movie[0]
      
        avgbyGenre = {'Drama':0, 'Romance':0, 'Documentary':0, 'Animated':0, 'Fantasy':0, 'Horror':0, 'Comedy':0, 'Thriller':0, 'Crime':0,
         'Western':0, 'Adventure':0, 'Action':0, 'War':0, 'Biography':0, 'Sci-Fi':0, 'Musical':0}

        if len(movies) > 25:
            for genre in genreCounts.items():
                if genre[1] < threshold:
                    avgbyGenre[genre[0]] = 0
                else:
                    avgbyGenre[genre[0]] = (genreTotals[genre[0]] / genre[1])   
        else:
            for genre in genreCounts.items():
                if genre[1] == 0:
                    avgbyGenre[genre[0]] = 0
                else:
                    avgbyGenre[genre[0]] = (genreTotals[genre[0]] / genre[1])

        avgByGenre = list(avgbyGenre.items())
        oldMax = ['',0] 
        for avg in avgByGenre:
            if(avg[1] > oldMax[1]):
                oldMax = avg
        return(oldMax[0])    

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
        monthDict = {'January':0, 'February':0, 'March':0,'April':0,'May':0,'June':0,'July':0,'August':0,
        'September':0,'October':0,'November':0,'December':0}

        for movie in annualMovies:
            monthDict[calendar.month_name[movie[1].month]] += 1

        counts = list(monthDict.values())   #Converting to a list makes this hashable so the plot can work
        months = list(monthDict.keys())
        self.dynAxMPM.set(xlabel='Month', ylabel='Movies Watched', title='Movies Per Month')
        self.dynAxMPM.plot(months, counts)
        self.dynAxMPM.grid(True)
        yRange = range(min(counts), math.ceil(max(counts))+1)       #Averages counts values for axis labels and prevents decimal values
        self.dynAxMPM.set_yticks(yRange)
        self.dynAxMPM.set_xticklabels(months, rotation='vertical')  #Makes tick labels vertical to save space
        self.dynAxMPM.figure.canvas.draw()                          #Refreshes Canvas
