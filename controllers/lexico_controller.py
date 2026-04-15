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

            # VALIDAR ERRORES LÉXICOS
            errores_lexicos = [t for t in self.tokens if t.tipo == "ERROR LEXICO"]

            if errores_lexicos:
                err = errores_lexicos[0]
                self.window.results_panel.show_error({
                    "linea": err.linea,
                    "error": "Error léxico",
                    "detalle": err.valor,
                    "solucion": "Corrige el token inválido"
                })
                return

            # 🔥 COMPILACIÓN
            try:
                parser = Parser(self.tokens)
                ast = parser.parse()

                self.window.results_panel.show_ast(ast)

                interprete = Interprete()
                resultado = interprete.ejecutar(ast)

                self.window.results_panel.show_result(resultado)

                self.window.statusBar().showMessage("Compilación completa ✅")

            except Exception as e:
                self.window.results_panel.show_error({
                    "linea": 0,
                    "error": "Error sintáctico/semántico",
                    "detalle": str(e),
                    "solucion": "Revisa la estructura del código"
                })

            return

        # ===== ANÁLISIS NORMAL =====

        char = self.lexer.texto[self.lexer.pos]
        linea = self.lexer.texto[:self.lexer.pos].count("\n") + 1

        self.window.editor_panel.highlight_position(self.lexer.pos)

        if char.isspace():
            self.lexer.pos += 1
            return

        if char.isalpha():
            token = self.lexer.identificador(linea)
            self.tokens.append(token)

            if token.tipo == "ERROR LEXICO":
                self.timer.stop()
                self.window.results_panel.show_error({
                    "linea": linea,
                    "error": "Identificador inválido",
                    "detalle": token.valor,
                    "solucion": "Solo letras permitidas"
                })
                return

            self.window.results_panel.add_token(token)
            return

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

        op2 = self.lexer.peek(2)
        if op2 in self.lexer.OPERADORES:
            token = Token("OPERADOR", op2, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 2
            return

        if char in self.lexer.OPERADORES:
            token = Token("OPERADOR", char, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 1
            return

        if char in self.lexer.SIMBOLOS:
            token = Token("SIMBOLO", char, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 1
            return

        self.timer.stop()
        self.window.results_panel.show_error({
            "linea": linea,
            "error": "Carácter no reconocido",
            "detalle": char,
            "solucion": "Elimina ese carácter"
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