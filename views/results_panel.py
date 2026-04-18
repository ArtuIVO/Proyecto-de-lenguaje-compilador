from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem,
    QListWidget, QTreeWidget, QTreeWidgetItem
)


class ResultsPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        # TOKENS
        self.token_table = QTableWidget(0, 3)
        self.token_table.setHorizontalHeaderLabels(
            ["Lexema", "Token", "Línea"]
        )
        self.tabs.addTab(self.token_table, "Tokens")

        # ERRORES
        self.error_list = QListWidget()
        self.tabs.addTab(self.error_list, "Errores")

        # RESULTADOS
        self.resultados_list = QListWidget()
        self.tabs.addTab(self.resultados_list, "Resultados")

        # AST
        self.ast_tree = QTreeWidget()
        self.ast_tree.setHeaderLabel("Árbol AST")
        self.tabs.addTab(self.ast_tree, "AST")

        layout.addWidget(self.tabs)

    def add_token(self, token):
        row = self.token_table.rowCount()
        self.token_table.insertRow(row)

        self.token_table.setItem(row, 0, QTableWidgetItem(token.valor))
        self.token_table.setItem(row, 1, QTableWidgetItem(token.tipo))
        self.token_table.setItem(row, 2, QTableWidgetItem(str(token.linea)))

    def show_error(self, err):
        self.error_list.clear()

        texto = (
            f"Línea {err['linea']}\n"
            f"Error: {err['error']}\n"
            f"Detalle: {err['detalle']}\n"
            f"Solución: {err['solucion']}"
        )

        self.error_list.addItem(texto)
        self.tabs.setCurrentIndex(1)

    def load_resultados(self, datos):
        self.resultados_list.clear()

        for x in datos:
            self.resultados_list.addItem(str(x))

        self.tabs.setCurrentIndex(2)

    def load_ast(self, ast):
        self.ast_tree.clear()

        root = QTreeWidgetItem([type(ast).__name__])
        self.ast_tree.addTopLevelItem(root)

        self._agregar_nodos(root, ast)
        self.ast_tree.expandAll()

    def _agregar_nodos(self, padre, nodo):
        if not hasattr(nodo, "__dict__"):
            return

        for k, v in nodo.__dict__.items():

            if isinstance(v, list):
                lista = QTreeWidgetItem([k])
                padre.addChild(lista)

                for item in v:
                    hijo = QTreeWidgetItem([type(item).__name__])
                    lista.addChild(hijo)
                    self._agregar_nodos(hijo, item)

            elif hasattr(v, "__dict__"):
                hijo = QTreeWidgetItem([k])
                padre.addChild(hijo)

                sub = QTreeWidgetItem([type(v).__name__])
                hijo.addChild(sub)

                self._agregar_nodos(sub, v)

            else:
                padre.addChild(QTreeWidgetItem([f"{k}: {v}"]))

    def clear(self):
        self.token_table.setRowCount(0)
        self.error_list.clear()
        self.resultados_list.clear()
        self.ast_tree.clear()