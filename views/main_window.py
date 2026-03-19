from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSplitter, QToolBar
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from views.editor_panel import EditorPanel
from views.results_panel import ResultsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self._setup_window()
        self._setup_actions()
        self._setup_menubar()
        self._setup_toolbar()
        self._setup_central()
        self._setup_statusbar()

    def _setup_window(self):
        self.setWindowTitle("Compilador V1  —  Analizador Léxico")
        self.setMinimumSize(1100, 700)

    def _setup_actions(self):
        self.action_analizar = QAction("Analizar", self)
        self.action_analizar.setShortcut("F1")

        self.action_limpiar = QAction("Limpiar", self)
        self.action_limpiar.setShortcut("Ctrl+L")

    def _setup_menubar(self):
        menubar = self.menuBar()

        archivo = menubar.addMenu("&Archivo")
        archivo.addAction(self.action_limpiar)

        analizadores = menubar.addMenu("&Analizadores")
        analizadores.addAction(self.action_analizar)

    def _setup_toolbar(self):
        toolbar = QToolBar("Principal")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        toolbar.addAction(self.action_analizar)
        toolbar.addSeparator()
        toolbar.addAction(self.action_limpiar)

    def _setup_central(self):
        # splitter es otra onda.
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.editor_panel = EditorPanel()
        self.results_panel = ResultsPanel()

        splitter.addWidget(self.editor_panel)
        splitter.addWidget(self.results_panel)
        splitter.setSizes([550, 550])
        splitter.setChildrenCollapsible(True)

        self.setCentralWidget(splitter)

    def _setup_statusbar(self):
        self.statusBar().showMessage("Listo.")