from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem,
    QListWidget, QTreeWidget, QTreeWidgetItem, QPushButton
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView

class ResultsPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modo_ast = "visual"
        self._setup_ui()
        

    def toggle_ast(self):
        self.modo_ast = "tecnico" if self.modo_ast == "visual" else "visual"

        # cambiar texto botón
        if self.modo_ast == "visual":
            self.btn_toggle_ast.setText("Vista AST: Visual")
        else:
            self.btn_toggle_ast.setText("Vista AST: Técnico")

        # recargar árbol
        if hasattr(self, "ultimo_ast"):
            self.load_ast(self.ultimo_ast)

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
        # TRAZA
        self.traza_list = QListWidget()
        self.tabs.addTab(self.traza_list, "Análisis")

        # TABLA SIMBOLOS
        self.simbolos_table = QTableWidget(0, 4)
        self.simbolos_table.setHorizontalHeaderLabels(
            ["Nombre", "Tipo", "Valor", "Línea"]
        )
        self.tabs.addTab(self.simbolos_table, "Tabla de Símbolos (Semántico)")
        # BOTÓN TOGGLE AST
        self.btn_toggle_ast = QPushButton("Vista AST: Visual")
        self.btn_toggle_ast.clicked.connect(self.toggle_ast)
        layout.addWidget(self.btn_toggle_ast)
        # TOKENS
        self.token_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.token_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # ERRORES
        self.error_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # RESULTADOS
        self.resultados_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # TRAZA
        self.traza_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # AST
        self.ast_tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ast_tree.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # TABLA DE SÍMBOLOS
        self.simbolos_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.simbolos_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

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
        self.ultimo_ast = ast 
        self.ast_tree.clear()

        if getattr(self, "modo_ast", "visual") == "tecnico":
            root = self._crear_item_tecnico(ast)
            self._cargar_hijos_tecnico(root, ast)
        else:
            root = self._crear_item_visual(ast)

        self.ast_tree.addTopLevelItem(root)
        self.ast_tree.expandAll()
        self.tabs.setCurrentIndex(3)

    def load_traza(self, datos):
        self.traza_list.clear()

        for x in datos:
            texto = f"L{x['linea']} → {x['accion']}"

            if "Asignación" in x["accion"]:
                texto = "[SEM] " + texto
            else:
                texto = "[SYN] " + texto

            if "valor" in x:
                texto += f" = {x['valor']}"

            if not x["valido"]:
                texto += " X"

            self.traza_list.addItem(texto)


    def load_simbolos(self, tabla):
        self.simbolos_table.setRowCount(0)

        for nombre, simbolo in tabla.items():
            row = self.simbolos_table.rowCount()
            self.simbolos_table.insertRow(row)

            self.simbolos_table.setItem(row, 0, QTableWidgetItem(nombre))
            self.simbolos_table.setItem(row, 1, QTableWidgetItem(simbolo.tipo))
            self.simbolos_table.setItem(row, 2, QTableWidgetItem(str(simbolo.valor)))
            self.simbolos_table.setItem(row, 3, QTableWidgetItem(str(simbolo.linea)))
        
    def _crear_item_visual(self, nodo):

        from models.ast_nodes import Programa, Asignacion, If, While, Para, Funcion, Retornar, Escribir, BinOp, Lista, AccesoLista, Numero, Cadena, Identificador

        # PROGRAMA
        if isinstance(nodo, Programa):
            item = QTreeWidgetItem(["Programa"])
            for s in nodo.sentencias:
                item.addChild(self._crear_item_visual(s))
            return item

        # ASIGNACION
        if isinstance(nodo, Asignacion):
            item = QTreeWidgetItem(["Asignación"])

            item.addChild(QTreeWidgetItem([f"Variable: {nodo.nombre}"]))
            item.addChild(self._crear_item_visual(nodo.valor))

            return item

        # IF
        if isinstance(nodo, If):
            item = QTreeWidgetItem(["Condicional"])

            cond = QTreeWidgetItem(["Condición"])
            cond.addChild(self._crear_item_visual(nodo.condicion))

            cuerpo = QTreeWidgetItem(["Cuerpo"])
            for ins in nodo.cuerpo:
                cuerpo.addChild(self._crear_item_visual(ins))

            item.addChild(cond)
            item.addChild(cuerpo)

            if nodo.sino:
                sino = QTreeWidgetItem(["Sino"])
                for ins in nodo.sino:
                    sino.addChild(self._crear_item_visual(ins))
                item.addChild(sino)

            return item

        # WHILE
        if isinstance(nodo, While):
            item = QTreeWidgetItem(["While"])

            cond = QTreeWidgetItem(["Condición"])
            cond.addChild(self._crear_item_visual(nodo.condicion))

            cuerpo = QTreeWidgetItem(["Cuerpo"])
            for ins in nodo.cuerpo:
                cuerpo.addChild(self._crear_item_visual(ins))

            item.addChild(cond)
            item.addChild(cuerpo)

            return item

        # FOR
        if isinstance(nodo, Para):
            item = QTreeWidgetItem([f"For ({nodo.variable})"])

            rango = QTreeWidgetItem(["Rango"])
            rango.addChild(self._crear_item_visual(nodo.inicio))
            rango.addChild(self._crear_item_visual(nodo.fin))

            cuerpo = QTreeWidgetItem(["Cuerpo"])
            for ins in nodo.cuerpo:
                cuerpo.addChild(self._crear_item_visual(ins))

            item.addChild(rango)
            item.addChild(cuerpo)

            return item

        # FUNCION
        if isinstance(nodo, Funcion):
            item = QTreeWidgetItem([f"Función {nodo.nombre}"])

            params = QTreeWidgetItem(["Parámetros"])
            for p in nodo.parametros:
                params.addChild(QTreeWidgetItem([p]))

            cuerpo = QTreeWidgetItem(["Cuerpo"])
            for ins in nodo.cuerpo:
                cuerpo.addChild(self._crear_item_visual(ins))

            item.addChild(params)
            item.addChild(cuerpo)

            return item

        # RETORNAR
        if isinstance(nodo, Retornar):
            item = QTreeWidgetItem(["Retornar"])
            item.addChild(self._crear_item_visual(nodo.valor))
            return item

        # ESCRIBIR
        if isinstance(nodo, Escribir):
            item = QTreeWidgetItem(["Salida"])
            item.addChild(self._crear_item_visual(nodo.valor))
            return item

        # BINOP
        if isinstance(nodo, BinOp):
            item = QTreeWidgetItem([f"Operación {nodo.op}"])
            item.addChild(self._crear_item_visual(nodo.izquierda))
            item.addChild(self._crear_item_visual(nodo.derecha))
            return item

        # LISTA
        if isinstance(nodo, Lista):
            item = QTreeWidgetItem(["Lista"])
            for e in nodo.elementos:
                item.addChild(self._crear_item_visual(e))
            return item

        # ACCESO LISTA
        if isinstance(nodo, AccesoLista):
            item = QTreeWidgetItem([f"Acceso {nodo.nombre}"])
            item.addChild(self._crear_item_visual(nodo.indice))
            return item

        # TERMINALES
        if isinstance(nodo, Numero):
            return QTreeWidgetItem([f"Número: {nodo.valor}"])

        if isinstance(nodo, Cadena):
            return QTreeWidgetItem([f"Texto: {nodo.valor}"])

        if isinstance(nodo, Identificador):
            return QTreeWidgetItem([f"Variable: {nodo.nombre}"])

        return QTreeWidgetItem([type(nodo).__name__])

    def _crear_item_tecnico(self, nodo):
        return QTreeWidgetItem([type(nodo).__name__])


    def _cargar_hijos_tecnico(self, padre, nodo):

        # 🔥 SI NO ES NODO → detener
        if not hasattr(nodo, "__dict__"):
            return

        for clave, valor in nodo.__dict__.items():

            # LISTAS
            if isinstance(valor, list):

                rama = QTreeWidgetItem([clave])
                padre.addChild(rama)

                for elem in valor:

                    # 🔥 SI ES NODO
                    if hasattr(elem, "__dict__"):
                        hijo = self._crear_item_tecnico(elem)
                        rama.addChild(hijo)
                        self._cargar_hijos_tecnico(hijo, elem)

                    # 🔥 SI ES DATO SIMPLE (string, int, etc)
                    else:
                        rama.addChild(
                            QTreeWidgetItem([str(elem)])
                        )

            # NODO INTERNO
            elif hasattr(valor, "__dict__"):

                rama = QTreeWidgetItem([clave])
                padre.addChild(rama)

                hijo = self._crear_item_tecnico(valor)
                rama.addChild(hijo)

                self._cargar_hijos_tecnico(hijo, valor)

            # 🔥 DATO SIMPLE
            else:
                padre.addChild(
                    QTreeWidgetItem([f"{clave}: {valor}"])
                )

    def _cargar_hijos(self, padre, nodo):

        if not hasattr(nodo, "__dict__"):
            return

        for clave, valor in nodo.__dict__.items():

            # LISTAS
            if isinstance(valor, list):

                rama = QTreeWidgetItem([clave])
                padre.addChild(rama)

                for elem in valor:

                    # si es nodo
                    if hasattr(elem, "__dict__"):
                        hijo = self._crear_item(elem)
                        rama.addChild(hijo)
                        self._cargar_hijos(hijo, elem)

                    # si es texto / número
                    else:
                        rama.addChild(
                            QTreeWidgetItem([str(elem)])
                        )

            # NODO INTERNO
            elif hasattr(valor, "__dict__"):

                rama = QTreeWidgetItem([clave])
                padre.addChild(rama)

                hijo = self._crear_item(valor)
                rama.addChild(hijo)

                self._cargar_hijos(hijo, valor)

            # DATO SIMPLE
            else:
                hoja = QTreeWidgetItem(
                    [f"{clave}: {valor}"]
                )
                padre.addChild(hoja)

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

        # agregar esto
        self.traza_list.clear()
        self.simbolos_table.setRowCount(0)