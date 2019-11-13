# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddMovieForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(383, 360)
        self.SubmitButton = QtWidgets.QPushButton(Form)
        self.SubmitButton.setGeometry(QtCore.QRect(270, 310, 81, 23))
        self.SubmitButton.setObjectName("SubmitButton")
        self.MovieTitleLabel = QtWidgets.QLabel(Form)
        self.MovieTitleLabel.setGeometry(QtCore.QRect(20, 20, 61, 16))
        self.MovieTitleLabel.setObjectName("MovieTitleLabel")
        self.DateWatchedLabel = QtWidgets.QLabel(Form)
        self.DateWatchedLabel.setGeometry(QtCore.QRect(20, 50, 81, 21))
        self.DateWatchedLabel.setObjectName("DateWatchedLabel")
        self.DateWatchedEntry = QtWidgets.QDateEdit(Form)
        self.DateWatchedEntry.setGeometry(QtCore.QRect(110, 50, 110, 22))
        self.DateWatchedEntry.setObjectName("DateWatchedEntry")
        self.MovieTitleEntry = QtWidgets.QLineEdit(Form)
        self.MovieTitleEntry.setGeometry(QtCore.QRect(110, 20, 241, 20))
        self.MovieTitleEntry.setObjectName("MovieTitleEntry")
        self.MovieRatingEntry = QtWidgets.QComboBox(Form)
        self.MovieRatingEntry.setGeometry(QtCore.QRect(110, 80, 41, 22))
        self.MovieRatingEntry.setMaxCount(11)
        self.MovieRatingEntry.setObjectName("MovieRatingEntry")
        self.MovieRatingLabel = QtWidgets.QLabel(Form)
        self.MovieRatingLabel.setGeometry(QtCore.QRect(20, 80, 71, 21))
        self.MovieRatingLabel.setObjectName("MovieRatingLabel")
        self.MovieGenreLabel = QtWidgets.QLabel(Form)
        self.MovieGenreLabel.setGeometry(QtCore.QRect(20, 110, 47, 21))
        self.MovieGenreLabel.setObjectName("MovieGenreLabel")
        self.MovieGenreEntry = QtWidgets.QComboBox(Form)
        self.MovieGenreEntry.setGeometry(QtCore.QRect(110, 110, 111, 22))
        self.MovieGenreEntry.setObjectName("MovieGenreEntry")
        self.MovieLocationLabel = QtWidgets.QLabel(Form)
        self.MovieLocationLabel.setGeometry(QtCore.QRect(20, 140, 101, 21))
        self.MovieLocationLabel.setObjectName("MovieLocationLabel")
        self.MovieLocationTheaterEntry = QtWidgets.QRadioButton(Form)
        self.MovieLocationTheaterEntry.setGeometry(QtCore.QRect(130, 140, 82, 21))
        self.MovieLocationTheaterEntry.setObjectName("MovieLocationTheaterEntry")
        self.MovieLocationHomeEntry = QtWidgets.QRadioButton(Form)
        self.MovieLocationHomeEntry.setGeometry(QtCore.QRect(200, 140, 82, 21))
        self.MovieLocationHomeEntry.setObjectName("MovieLocationHomeEntry")
        self.MovieCommentsLabel = QtWidgets.QLabel(Form)
        self.MovieCommentsLabel.setGeometry(QtCore.QRect(20, 170, 61, 21))
        self.MovieCommentsLabel.setObjectName("MovieCommentsLabel")
        self.MovieCommentsEntry = QtWidgets.QPlainTextEdit(Form)
        self.MovieCommentsEntry.setGeometry(QtCore.QRect(110, 170, 241, 121))
        self.MovieCommentsEntry.setObjectName("MovieCommentsEntry")
        self.CancelEntryButton = QtWidgets.QPushButton(Form)
        self.CancelEntryButton.setGeometry(QtCore.QRect(180, 310, 81, 23))
        self.CancelEntryButton.setObjectName("CancelEntryButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.SubmitButton.setText(_translate("Form", "Submit Entry"))
        self.MovieTitleLabel.setText(_translate("Form", "Movie Title:"))
        self.DateWatchedLabel.setText(_translate("Form", "Date Watched:"))
        self.MovieRatingLabel.setText(_translate("Form", "Rating (1-10):"))
        self.MovieGenreLabel.setText(_translate("Form", "Genre:"))
        self.MovieLocationLabel.setText(_translate("Form", "Location Watched:"))
        self.MovieLocationTheaterEntry.setText(_translate("Form", "Theater"))
        self.MovieLocationHomeEntry.setText(_translate("Form", "Home"))
        self.MovieCommentsLabel.setText(_translate("Form", "Comments:"))
        self.CancelEntryButton.setText(_translate("Form", "Cancel Entry"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
