from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QListWidget
)


class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def show_result(self, data):
        self.result_list.clear()

        for k, v in data.items():
            self.result_list.addItem(f"{k} = {v}")

        self.tabs.setCurrentIndex(2)

    def show_ast(self, nodo, nivel=0):
        if nivel == 0:
            self.ast_view.clear()

        indent = "│   " * nivel + "├── "

        nombre = type(nodo).__name__

        # mostrar info útil
        extra = ""
        if hasattr(nodo, "nombre"):
            extra = f" ({nodo.nombre})"
        if hasattr(nodo, "valor"):
            extra = f" ({nodo.valor})"

        self.ast_view.addItem(f"{indent}{nombre}{extra}")

        for attr in vars(nodo).values():
            if isinstance(attr, list):
                for item in attr:
                    if hasattr(item, "__dict__"):
                        self.show_ast(item, nivel + 1)
            elif hasattr(attr, "__dict__"):
                self.show_ast(attr, nivel + 1)

        if nivel == 0:
            self.tabs.setCurrentIndex(3)

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.result_list = QListWidget()
        self.tabs.addTab(self.result_list, "Resultados")
        # TAB AST (ÁRBOL SINTÁCTICO)
        self.ast_view = QListWidget()
        self.tabs.addTab(self.ast_view, "AST")

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

        if hasattr(self, "result_list"):
            self.result_list.clear()

        if hasattr(self, "ast_view"):
            self.ast_view.clear()