from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QListWidget
)


class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        # TAB TOKENS
        self.token_table = QTableWidget(0, 3)
        self.token_table.setHorizontalHeaderLabels(["Lexema", "Token", "Línea"])
        self.tabs.addTab(self.token_table, " Tokens")

        # TAB ERRORES
        self.error_list = QListWidget()
        self.tabs.addTab(self.error_list, " Errores")

        layout.addWidget(self.tabs)

    def add_token(self, token):
        row = self.token_table.rowCount()
        self.token_table.insertRow(row)

        self.token_table.setItem(row, 0, QTableWidgetItem(token.valor))
        self.token_table.setItem(row, 1, QTableWidgetItem(token.tipo))
        self.token_table.setItem(row, 2, QTableWidgetItem(str(token.linea)))

        self.token_table.scrollToBottom()

    def show_error(self, err):
        self.error_list.clear()

        texto = (
            f"Línea {err['linea']}\n"
            f"Error: {err['error']}\n"
            f"Detalle: {err['detalle']}\n"
            f"Posible Solución: {err['solucion']}"
        )

        self.error_list.addItem(texto)
        self.tabs.setCurrentIndex(1)

    def clear(self):
        self.token_table.setRowCount(0)
        self.error_list.clear()