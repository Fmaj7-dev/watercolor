
import sys
from color import run
from PySide6 import QtCore, QtWidgets, QtGui, QtUiTools
import numpy as np

class PaletteWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print("PaletteWidget::init()")
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click meeee!")
        self.text = QtWidgets.QLabel("Hello Worldddd", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

class ImageWidget(QtWidgets.QGraphicsView):
    def __init__(self):
        print("ImageWidget::init()")
        super(ImageWidget, self).__init__()
        self.scene = QtWidgets.QGraphicsScene(self)

        self.background = QtGui.QPixmap("./palette.jpg")
        self.scene.addPixmap(self.background)

        self.setScene( self.scene )
        self.setCacheMode( QtWidgets.QGraphicsView.CacheBackground )
        self.setViewportUpdateMode( QtWidgets.QGraphicsView.BoundingRectViewportUpdate )
        self.setRenderHint( QtGui.QPainter.Antialiasing )
        self.setTransformationAnchor( QtWidgets.QGraphicsView.AnchorUnderMouse )
        self.setResizeAnchor( QtWidgets.QGraphicsView.AnchorViewCenter )

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

"""
        self.paletteWidget = PaletteWidget()
        self.imageWidget = ImageWidget()

        self.paletteWidget.show()
        self.imageWidget.show()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.paletteWidget)
        self.layout.addWidget(self.imageWidget)
"""
        #self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(QtGui.QPalette.Window, QtGui.QColor(int(color[0]),int(color[1]),int(color[2]),255))
        #self.setPalette(p)

class MyWidget(QtWidgets.QWidget):
    def __init__(self, app):
        super(MyWidget, self).__init__()

        self.app = app

        # load widget
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile("./mainwindow.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(file, self)
        file.close()

        # configure graphics
        self.background = QtGui.QPixmap("./palette.jpg")
        
        self.scene = QtWidgets.QGraphicsScene(self.widget.graphicsView)
        self.scene.addPixmap(self.background)
        self.widget.graphicsView.resize(self.background.size().width(), self.background.size().height() )
        self.widget.graphicsView.setScene(self.scene)
        self.widget.resize(self.background.size().width(), self.background.size().height() )

        # colors
        self.widget.color1.setStyleSheet("background-color:rgb(255,0,0)")
        self.widget.color2.setStyleSheet("background-color:rgb(255,255,0)")

    def run(self):
        self.widget.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    """color = run( int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) )
    print("color:")
    print(color)"""

    app = QtWidgets.QApplication([])
    myWidget = MyWidget(app)
    myWidget.run()
