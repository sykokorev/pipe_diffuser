import pyqtgraph as pg

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QGridLayout, QWidget, QTabWidget, QLabel,
    QLineEdit
)
from PySide6.QtCore import QRect, QSize, Qt


from .color import Color


class Label(QLabel):
    def __init__(self, text: str, geometry: list, alignment: Qt.AlignmentFlag=Qt.AlignCenter):
        super(Label, self).__init__()

        self.setText(text)
        rect = QRect(*geometry)
        self.setGeometry(rect)
        self.setAlignment(alignment)


class TabWidget(QTabWidget):
    def __init__(self, widgets: list, position: QTabWidget=QTabWidget.West, isMovable: bool=True):
        super().__init__()
        
        self.setTabPosition(position)
        self.setMovable(isMovable)

        for n, (widget, label) in enumerate(widgets):
            self.addTab(widget, label)


class LineEdit(QLineEdit):
    def __init__(self, **kwargs):
        super().__init__()

        width = kwargs.get('width', 64)
        height = kwargs.get('height', 12)
        placeholder = kwargs.get('placeholder', None)
        alignment = kwargs.get('alignment', Qt.AlignmentFlag.AlignCenter)

        if not isinstance(width, int):
            width = 64
        if not isinstance(height, int):
            height = 12
        # self.resize(QSize(width, height))
        self.setFixedSize(QSize(width, height))
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setAlignment(alignment)


class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Pipe Diffuser Designer")
        self.resize(1024, 728)

        labels_indata = kwargs.get('labels', None)
        if not labels_indata:
            labels_indata = {
                'Number of Pipes': [2, 2, 20, 5],
                'Del L star': [10, 10, 20, 5],
                'L star': [18, 18, 20, 5]
            }
        enters_indata = kwargs.get('enters', None)
        if not enters_indata:
            enters_indata = {
                'Number of Pipes': [128, 24],
                'Delta L Star': [128, 24],
                'L Star': [128, 24]
            }

        main_layout = QGridLayout()

        ingraphs = [
            (Color('red'), 'Red'), (Color('yellow'), 'Yellow'), 
            (Color('green'), 'Green'), (Color('blue'), 'Blue')
        ]
        outgraph = [
            (Color('purple'), 'purple'), (Color('yellow'), 'Yellow'), 
            (Color('green'), 'Green'), (Color('blue'), 'Blue')
        ]
        ingraph_tabs = TabWidget(widgets=ingraphs)
        outgraph_tabs = TabWidget(widgets=outgraph)

        # Setting Indata Layout
        indata_layout = QGridLayout()
        indata_layout.setSpacing(10)
        main_layout.addLayout(indata_layout, 0, 0)
        for row, ((label, lgeom), (placeholder, egeom)) in enumerate(zip(labels_indata.items(), enters_indata.items())):
            if not row % 2:
                c, r, alignment = 0, row, Qt.AlignmentFlag.AlignLeft
            else:
                c, r, alignment = 2, row - 1, Qt.AlignmentFlag.AlignLeft
            lbl = Label(text=label, geometry=lgeom)
            indata_layout.addWidget(lbl, r, c)
            indata_layout.setAlignment(lbl, alignment)
            line_edit = LineEdit(placeholder=placeholder, width=egeom[0], height=egeom[1], 
                                 alignment=Qt.AlignmentFlag.AlignCenter)
            indata_layout.addWidget(line_edit, r, c+1)
            indata_layout.setAlignment(line_edit, alignment)

        empty_widget = QWidget()
        indata_layout.addWidget(empty_widget, 0, 3)
        indata_layout.setColumnStretch(3, 100)

        main_layout.addWidget(ingraph_tabs, 1, 0)
        main_layout.addWidget(outgraph_tabs, 0, 1, 0, 1)
        main_layout.setSpacing(20)

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)
