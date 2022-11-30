import sys

from PySide6.QtWidgets import QApplication

from qt_gui.gui import *


if __name__ == "__main__":
    
    app = QApplication()
    gui = MainWindow()

    gui.show()
    app.exec()
