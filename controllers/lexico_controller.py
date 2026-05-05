import ast

from PyQt6.QtWidgets import QFileDialog

from models.lexico_model import Lexer
from models.sintactico_model import Parser
from models.semantico_model import AnalizadorSemantico

from npc.npc_parser import NPCParser
from npc.npc_semantic import NPCSemantic

from models.error import CompilerError

class LexicoController:

    def __init__(self, window):
        self.window = window
        self._connect_signals()

    def _connect_signals(self): 
        self.window.action_analizar.triggered.connect(self.analizar)
        self.window.action_limpiar.triggered.connect(self.limpiar)
        self.window.action_abrir.triggered.connect(self.abrir_archivo)

    def abrir_archivo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Abrir Archivo",
            "",
            "Archivos (*.txt)"
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.window.editor_panel.set_code(f.read())

    def analizar(self):
        codigo = self.window.editor_panel.get_code()

        if not codigo.strip():
            self.window.statusBar().showMessage("Editor vacío")
            return

        self.window.results_panel.clear()


        try:
            # LEXICO
            lexer = Lexer(codigo)
            tokens, errores = lexer.analizar_con_errores()

            if errores:
                self.window.results_panel.show_error(errores[0])
                return

            for token in tokens:
                self.window.results_panel.add_token(token)

            # Selección inteligente de lenguaje

            if "npc " in codigo:
                parser = NPCParser(tokens)
                sem = NPCSemantic()
            else:
                parser = Parser(tokens)
                sem = AnalizadorSemantico()
            # SINTÁCTICO
            ast = parser.parse()
            # MOSTRAR AST SIEMPRE
            self.window.results_panel.load_ast(ast)

            # SEMÁNTICO
            sem.analizar(ast)

            # RESULTADOS
            self.window.results_panel.load_resultados(
                [str(x) for x in sem.salida]
            )
            if not sem.salida:
                self.window.results_panel.load_resultados(
                    ["(Sin salida)"]
                )

            # NUEVO — TRAZA + TABLA DE SÍMBOLOS
            traza_total = []

            if hasattr(parser, "traza"):
                traza_total += parser.traza

            if hasattr(sem, "traza"):
                traza_total += sem.traza

            self.window.results_panel.load_traza(traza_total)

            
            # 🔥 NUEVO — TABLA DE SÍMBOLOS (scope global)
            if hasattr(sem, "scopes"):
                self.window.results_panel.load_simbolos(sem.scopes[0])

            # fallback (por compatibilidad con NPC viejo)
            elif hasattr(sem, "tabla_simbolos"):
                self.window.results_panel.load_simbolos(sem.tabla_simbolos)

            self.window.statusBar().showMessage("Compilación exitosa")

        

        except CompilerError as e:
            self.window.results_panel.show_error({
                "linea": e.linea,
                "error": "Error sintáctico/semántico",
                "detalle": e.mensaje,
                "solucion": "Revisa la estructura del código"
            })

        except Exception as e:
            self.window.results_panel.show_error({
                "linea": 0,
                "error": "Error crítico",
                "detalle": str(e),
                "solucion": "Error interno del compilador"
            })

    def limpiar(self):
        self.window.editor_panel.clear()
        self.window.results_panel.clear()
        self.window.statusBar().showMessage("Listo")