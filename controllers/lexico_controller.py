from PyQt6.QtCore import QTimer
from models.lexico_model import Lexer, Token


class LexicoController:
    def __init__(self, window):
        self.window = window
        self._connect_signals()

    def _connect_signals(self):
        self.window.action_analizar.triggered.connect(self.analizar)
        self.window.action_limpiar.triggered.connect(self.limpiar)

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
            self.window.statusBar().showMessage("Análisis terminado")
            return

        char = self.lexer.texto[self.lexer.pos]
        linea = self.lexer.texto[:self.lexer.pos].count("\n") + 1

        # mover cursor visual
        self.window.editor_panel.highlight_position(self.lexer.pos)

        # espacios
        if char.isspace():
            self.lexer.pos += 1
            return

        # identificadores
        if char.isalpha():
            token = self.lexer.identificador(linea)
            self.tokens.append(token)

            # 🚨 DETECTAR ERROR
            if token.tipo == "ERROR LEXICO":
                self.timer.stop()
                self.window.results_panel.show_error({
                    "linea": linea,
                    "error": "Identificador inválido",
                    "detalle": token.valor,
                    "solucion": "Usa solo letras (ej: ejecutar, enemigo)"
                })
                self.window.statusBar().showMessage("❌ Error encontrado")
                return

            self.window.results_panel.add_token(token)
            return

        # números
        if char.isdigit():
            token = self.lexer.numero_o_error(linea)
            self.tokens.append(token)

            if token.tipo == "ERROR LEXICO":
                self.timer.stop()
                self.window.results_panel.show_error({
                    "linea": linea,
                    "error": "Número mal formado",
                    "detalle": token.valor,
                    "solucion": "No mezcles números con letras"
                })
                self.window.statusBar().showMessage("Error encontrado")
                return

            self.window.results_panel.add_token(token)
            return

        # operadores compuestos
        op2 = self.lexer.peek(2)
        if op2 in self.lexer.OPERADORES:
            token = Token("OPERADOR", op2, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 2
            return

        # operadores simples
        if char in self.lexer.OPERADORES:
            token = Token("OPERADOR", char, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 1
            return

        # símbolos
        if char in self.lexer.SIMBOLOS:
            token = Token("SIMBOLO", char, linea)
            self.tokens.append(token)
            self.window.results_panel.add_token(token)
            self.lexer.pos += 1
            return

        # error
        self.timer.stop()
        self.window.results_panel.show_error({
            "linea": linea,
            "error": "Carácter no reconocido",
            "detalle": char,
            "solucion": "Elimina o reemplaza el carácter"
        })
        self.window.statusBar().showMessage("Error encontrado")

    def limpiar(self):
        if hasattr(self, "timer"):
            self.timer.stop()

        self.window.editor_panel.clear()
        self.window.results_panel.clear()
        self.window.statusBar().showMessage("Listo.")