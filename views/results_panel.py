from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel,
    QTableWidget, QTableWidgetItem, QListWidget
)
from PyQt6.QtGui import QColor


class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()

        # Tab 1: Tokens
        self.token_table = QTableWidget(0, 3)
        self.token_table.setHorizontalHeaderLabels(["Lexema", "Token", "Línea"])
        self.token_table.horizontalHeader().setStretchLastSection(True) # type: ignore
        self.token_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.token_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabs.addTab(self.token_table, "Tokens")

        # Tab 2: Sintáctico
        self.sintactico_label = QLabel("Esperando análisis...")
        self.sintactico_label.setWordWrap(True)
        self.sintactico_label.setStyleSheet("padding: 12px; font-size: 13px;")
        # self.tabs.addTab(self.sintactico_label, "Sintáctico")

        # Tab 3: Errores
        self.error_list = QListWidget()
        self.tabs.addTab(self.error_list, "Errores")

        layout.addWidget(self.tabs)

    def load_tokens(self, tokens: list[tuple]):
        """tokens: lista de (lexema, tipo, linea)"""
        self.token_table.setRowCount(0)
        for lexema, tipo, linea in tokens:
            row = self.token_table.rowCount()
            self.token_table.insertRow(row)
            self.token_table.setItem(row, 0, QTableWidgetItem(str(lexema)))
            self.token_table.setItem(row, 1, QTableWidgetItem(str(tipo)))
            self.token_table.setItem(row, 2, QTableWidgetItem(str(linea)))
        self.tabs.setCurrentIndex(0)

    def set_sintactico(self, state: str, message: str):
        """
        estado: 'ok' | 'error' | 'omitido'
        colors = {
            "ok":      "#7ee787",   # verde
            "error":   "#f85149",   # rojo
            "omitido": "#e3b341",   # amarillo
        }
        color = colors.get(state, "#c9d1d9")
        self.sintactico_label.setText(message or "")
        self.sintactico_label.setStyleSheet(
            f"padding: 12px; font-size: 13px; color: {color};"
        )
        """
        pass

    def load_errors(self, errors: list[str]):
        self.error_list.clear()
        for error in errors:
            self.error_list.addItem(error)
        if errors:
            self.tabs.setCurrentIndex(2)

    def clear(self):
        self.token_table.setRowCount(0)
        self.error_list.clear()
        # self.sintactico_label.setText("Esperando análisis...")
        # self.sintactico_label.setStyleSheet("padding: 12px; font-size: 13px;")
        