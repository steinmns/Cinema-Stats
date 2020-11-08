from PyQt5 import QtCore, QtWidgets

#Class skeleton courtesy of @Musicamante on StackOverflow: https://bit.ly/2LNoafQ

class QToaster(QtWidgets.QFrame):
    closed = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QToaster, self).__init__(*args, **kwargs)
        QtWidgets.QHBoxLayout(self)

        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, 
                           QtWidgets.QSizePolicy.Maximum)

     
        self.setAutoFillBackground(True)
        self.setFrameShape(self.Box)

        self.timer = QtCore.QTimer(singleShot=True, timeout=self.hide)

        self.opacity = QtWidgets.QGraphicsOpacityEffect(opacity=0)
        self.setGraphicsEffect(self.opacity)
        self.opacityAni = QtCore.QPropertyAnimation(self.opacity, b'opacity')
        self.opacityAni.setStartValue(0.)
        self.opacityAni.setEndValue(1.)
        self.opacityAni.setDuration(100)
        self.opacityAni.finished.connect(self.checkClosed)

    def checkClosed(self):
        # if we have been fading out, we're closing the notification
        if self.opacityAni.direction() == self.opacityAni.Backward:
            self.close()

    def enterEvent(self, event):
        # do not close the notification if the mouse is in
        self.timer.stop()
        # also, stop the animation if it's fading out...
        self.opacityAni.stop()
        # ...and restore the opacity
        self.opacity.setOpacity(1)

    def hide(self):
        # start hiding
        self.opacityAni.setDirection(self.opacityAni.Backward)
        self.opacityAni.setDuration(500)
        self.opacityAni.start()

    def leaveEvent(self, event):
        self.timer.start()

    def closeEvent(self, event):
        super(QToaster, self).closeEvent(event)
        # we don't need the notification anymore, delete it!
        self.deleteLater()

    @staticmethod
    def showMessage(parent, message, 
                    icon=QtWidgets.QStyle.SP_MessageBoxInformation, 
                    corner=QtCore.Qt.TopLeftCorner, margin=10, closable=True, 
                    timeout=5000, parentWindow=True):
        # use the top level window?
        if parentWindow:
            parent = parent.window()
        self = QToaster(parent)
        self.timer.setInterval(timeout)

        # use Qt standard icon pixmaps; see:
        # https://doc.qt.io/qt-5/qstyle.html#StandardPixmap-enum
        if isinstance(icon, QtWidgets.QStyle.StandardPixmap):
            labelIcon = QtWidgets.QLabel()
            self.layout().addWidget(labelIcon)
            icon = self.style().standardIcon(icon)
            size = self.style().pixelMetric(QtWidgets.QStyle.PM_SmallIconSize)
            labelIcon.setPixmap(icon.pixmap(size))

        self.label = QtWidgets.QLabel(message)
        self.layout().addWidget(self.label)

        if closable:
            self.closeButton = QtWidgets.QToolButton()
            self.layout().addWidget(self.closeButton)
            closeIcon = self.style().standardIcon(
                QtWidgets.QStyle.SP_TitleBarCloseButton)
            self.closeButton.setIcon(closeIcon)
            self.closeButton.setAutoRaise(True)
            self.closeButton.clicked.connect(self.close)

        self.timer.start()

        # raise the widget, adjust its size to the minimum and show it
        self.raise_()
        self.adjustSize()
        self.show()
        self.opacityAni.start()

        geo = self.geometry()
        # now the widget should have the correct size hints, let's move it to the
        # right place
        if corner == QtCore.Qt.TopLeftCorner:
            geo.moveTopLeft(
                parent.rect().topLeft() + QtCore.QPoint(margin, margin))
        elif corner == QtCore.Qt.TopRightCorner:
            geo.moveTopRight(
                parent.rect().topRight() + QtCore.QPoint(-margin, margin))
        elif corner == QtCore.Qt.BottomRightCorner:
            geo.moveBottomRight(
                parent.rect().bottomRight() + QtCore.QPoint(-margin, -margin))
        else:
            geo.moveBottomLeft(
                parent.rect().bottomLeft() + QtCore.QPoint(margin, -margin))
        self.setGeometry(geo)
