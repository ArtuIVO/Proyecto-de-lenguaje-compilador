from PyQt6.QtWidgets import (
    QMainWindow, QSplitter, QToolBar
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from views.editor_panel import EditorPanel
from views.results_panel import ResultsPanel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Compilador V1")
        self.resize(1200, 700)

        self._crear_acciones()
        self._crear_toolbar()
        self._crear_central()
        self.statusBar().showMessage("Listo")

    def _crear_acciones(self):
        self.action_analizar = QAction("Analizar", self)
        self.action_analizar.setShortcut("F1")

        self.action_limpiar = QAction("Limpiar", self)
        self.action_limpiar.setShortcut("Ctrl+L")

        self.action_abrir = QAction("Abrir", self)
        self.action_abrir.setShortcut("Ctrl+O")

    def _crear_menu(self):
        menu = self.menuBar()

        archivo = menu.addMenu("Archivo")
        archivo.addAction(self.action_abrir)
        archivo.addAction(self.action_limpiar)

        compilar = menu.addMenu("Compilar")
        compilar.addAction(self.action_analizar)

    def _crear_toolbar(self):
        bar = QToolBar()
        self.addToolBar(bar)

        bar.addAction(self.action_analizar)
        bar.addAction(self.action_abrir)
        bar.addAction(self.action_limpiar)

    def _crear_central(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.editor_panel = EditorPanel()
        self.results_panel = ResultsPanel()

        splitter.addWidget(self.editor_panel)
        splitter.addWidget(self.results_panel)
        splitter.setSizes([600, 600])

        self.setCentralWidget(splitter)