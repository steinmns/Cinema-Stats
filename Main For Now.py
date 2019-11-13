#Imports
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="moviesheet"
)

class Window_Stock(QMainWindow):
    #Constructor Method
    def __init__(self):
        super(Window_Stock, self).__init__()
        self.setGeometry(100, 100, 700, 700)  #Position and size of window. Args are (xposition, yposition, width, height). 0,0 is the top left corner of the screen. Unit is in pixels
        self.setWindowTitle("Cinema Stats")   #Sets the title of the window
      

        #self.insert_Movie("The Godfather", 10)
        #self.initUI

    #def initUI(self):

    #Inserts a new movie to the movie list
    def insertMovie(self):
        sql = "INSERT INTO log (LOG_MOVIE_TITLE, LOG_MOVIE_DATE, LOG_MOVIE_RATING, LOG_MOVIE_GENRE, LOG_MOVIE_LOCATION, LOG_MOVIE_COMMENTS) VALUES (%s, %s, %s, %s, %s, %s)"
        #vals = [self.] FIX THIS AND ADD CONTENTS OF ADD FORM
        mydb.cursor().execute(sql, vals)
        mydb.commit()
                 
def window():
    app = QApplication(sys.argv)    #System configs
    main_window = Window_Stock()
    main_window.show()  #Displays the window
    sys.exit(app.exec_()) #Ensures clean exit when user closes window

window() #Calls window method 