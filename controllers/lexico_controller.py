from PyQt6.QtCore import QTimer
from models.lexico_model import Lexer, Token
from models.sintactico_model import Parser
from models.interprete import Interprete

class LexicoController:
    def __init__(self, window):
        self.window = window
        self._connect_signals()

    def _connect_signals(self):
        self.window.action_analizar.triggered.connect(self.analizar)
        self.window.action_limpiar.triggered.connect(self.limpiar)
        self.window.load_file.triggered.connect(self.cargar_archivo)

    def analizar(self):
        codigo = self.window.editor_panel.get_code()

        if not codigo.strip():
            self.window.statusBar().showMessage("El editor está vacío.")
            return

        self.window.statusBar().showMessage("Analizando en tiempo real...")

        self.lexer = Lexer(codigo)
        self.tokens = []

        self.window.results_panel.clear()

        self.timer = QTimer()
        self.timer.timeout.connect(self._procesar_paso)
        self.timer.start(120)

    def _procesar_paso(self):
        if self.lexer.pos >= len(self.lexer.texto):
            self.timer.stop()

            # VALIDAR ERRORES LÉXICOS ANTES
            errores_lexicos = [t for t in self.tokens if t.tipo == "ERROR LEXICO"]

            if errores_lexicos:
                err = errores_lexicos[0]
                self.window.results_panel.show_error({
                    "linea": err.linea,
                    "error": "Error léxico",
                    "detalle": err.valor,
                    "solucion": "Corrige el token inválido antes de continuar"
                })
                self.window.statusBar().showMessage("Error léxico encontrado")
                return

            # COMPILACIÓN COMPLETA
            try:
                from models.sintactico_model import Parser
                from models.interprete import Interprete

                parser = Parser(self.tokens)
                ast = parser.parse()

                #  AST
                self.window.results_panel.show_ast(ast)

                #  SEMÁNTICO + EJECUCIÓN
                interprete = Interprete()
                resultado = interprete.ejecutar(ast)

                self.window.results_panel.show_result(resultado)

                self.window.statusBar().showMessage("Compilación completa")

            except Exception as e:
                self.window.results_panel.show_error({
                    "linea": 0,
                    "error": "Error sintáctico o semántico",
                    "detalle": str(e),
                    "solucion": "Verifica estructura (si, :, =) y variables definidas"
                })
                self.window.statusBar().showMessage("Error en compilación")

            return
        char = self.lexer.texto[self.lexer.pos]
        linea = self.lexer.texto[:self.lexer.pos].count("\n") + 1

        self.window.editor_panel.highlight_position(self.lexer.pos)

        if char.isspace():
            self.lexer.pos += 1
            return

        # IDENTIFICADORES
        if char.isalpha():
            token = self.lexer.identificador(linea)
            self.tokens.append(token)

            if token.tipo == "ERROR LEXICO":
                self.timer.stop()
                self.window.results_panel.show_error({
                    "linea": linea,
                    "error": "Identificador inválido",
                    "detalle": token.valor,
                    "solucion": "Usa solo letras sin números"
                })
                return

            self.window.results_panel.add_token(token)
            return

        # NÚMEROS
        if char.isdigit():
            token = self.lexer.numero_o_error(linea)
            self.tokens.append(token)

            if token.tipo == "ERROR LEXICO":
                self.timer.stop()
                self.window.results_panel.show_error({
                    "linea": linea,
                    "error": "Número inválido",
                    "detalle": token.valor,
                    "solucion": "No mezclar números con letras"
                })
                return

            self.window.results_panel.add_token(token)
            return

        # OPERADORES COMPUESTOS
        op2 = self.lexer.peek(2)
        if op2 in self.lexer.OPERADORES:
            from models.lexico_model import Token
            token = Token("OPERADOR", op2, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 2
            return

        # OPERADORES SIMPLES
        if char in self.lexer.OPERADORES:
            from models.lexico_model import Token
            token = Token("OPERADOR", char, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 1
            return

        # SÍMBOLOS
        if char in self.lexer.SIMBOLOS:
            from models.lexico_model import Token
            token = Token("SIMBOLO", char, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 1
            return

        # ERROR DESCONOCIDO
        self.timer.stop()
        self.window.results_panel.show_error({
            "linea": linea,
            "error": "Carácter no reconocido",
            "detalle": char,
            "solucion": "Elimina o reemplaza el carácter"
        })

    def limpiar(self):
        if hasattr(self, "timer"):
            self.timer.stop()

        self.window.editor_panel.clear()
        self.window.results_panel.clear()
        self.window.statusBar().showMessage("Listo.")

    def cargar_archivo(self):
        from PyQt6.QtWidgets import QFileDialog

        file, _ = QFileDialog.getOpenFileName(
            self.window,
            "Abrir archivo",
            "",
            "Archivos de texto (*.txt);;Todos (*.*)"
        )

        if file:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    self.window.editor_panel.editor.setPlainText(contenido)
                    self.window.statusBar().showMessage(f"Archivo cargado: {file}")
            except Exception as e:
                self.window.statusBar().showMessage("Error al cargar archivo")