
from PyQt6.QtWidgets import QFileDialog

from generators.javascript_generator import JavaScriptGenerator
from models.lexico_model import Lexer
from models.sintactico_model import Parser
from models.semantico_model import AnalizadorSemantico
from models.error import CompilerError
from generators.python_generator import PythonGenerator
from generators.javascript_generator import JavaScriptGenerator
from generators.csharp_generator import CSharpGenerator

class CompilerController:

    def __init__(self, window):

        self.window = window

        # lenguaje actual del compilador
        self.current_language = "EduLang"

        self._connect_signals()

    # =====================================================
    # SIGNALS
    # =====================================================

    def _connect_signals(self):

        self.window.action_analizar.triggered.connect(
            self.compilar
        )

        self.window.action_limpiar.triggered.connect(
            self.limpiar
        )

        self.window.action_abrir.triggered.connect(
            self.abrir_archivo
        )
        self.window.action_exportar_python.triggered.connect(
            self.exportar_python
        )
        self.window.action_exportar_javascript.triggered.connect(
            self.exportar_javascript
        )
        self.window.action_exportar_csharp.triggered.connect(
            self.exportar_csharp
        )
    # =====================================================
    # IMPORTAR 
    # =====================================================
    def importar_codigo(self): # type: ignore
        pass
    #======================================================
    # EXPORTAR
    #======================================================
    
    def exportar_python(self):

        codigo = self.window.editor_panel.get_code()

        if not codigo.strip():

            self.window.statusBar().showMessage(
                "No hay código para exportar"
            )

            return

        try:

            # =============================================
            # COMPILAR
            # =============================================

            lexer = Lexer(codigo)

            tokens, errores = lexer.analizar_con_errores()

            if errores:

                self.window.results_panel.show_error(
                    errores[0]
                )

                return

            parser = Parser(tokens)

            ast = parser.parse()

            # =============================================
            # GENERAR PYTHON
            # =============================================

            generator = PythonGenerator()

            generator.generate(ast)

            codigo_python = generator.get_code()

            # =============================================
            # GUARDAR ARCHIVO
            # =============================================

            file_path, _ = QFileDialog.getSaveFileName(
                self.window,
                "Exportar Python",
                "programa.py",
                "Python Files (*.py)"
            )

            if not file_path:
                return

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(codigo_python)

            self.window.statusBar().showMessage(
                f"Python exportado: {file_path}"
            )

        except CompilerError as e:

            self.window.results_panel.show_error({
                "linea": e.linea,
                "error": "Error exportando Python",
                "detalle": e.mensaje,
                "solucion": "Corrige el código antes de exportar"
            })

        except Exception as e:

            self.window.results_panel.show_error({
                "linea": 0,
                "error": "Error crítico",
                "detalle": str(e),
                "solucion": "Error interno del exportador"
            })

    # =====================================================
    # EXPORTAR JAVASCRIPT
    # =====================================================
   
    def exportar_javascript(self):

        codigo = self.window.editor_panel.get_code()

        if not codigo.strip():

            self.window.statusBar().showMessage(
                "No hay código para exportar"
            )

            return

        try:

            # =============================================
            # LEXER
            # =============================================

            lexer = Lexer(codigo)

            tokens, errores = lexer.analizar_con_errores()

            if errores:

                self.window.results_panel.show_error(
                    errores[0]
                )

                return

            # =============================================
            # PARSER
            # =============================================

            parser = Parser(tokens)

            ast = parser.parse()

            # =============================================
            # GENERATOR JS
            # =============================================

            generator = JavaScriptGenerator()

            generator.generate(ast)

            codigo_js = generator.get_code()

            # =============================================
            # GUARDAR ARCHIVO
            # =============================================

            file_path, _ = QFileDialog.getSaveFileName(
                self.window,
                "Exportar JavaScript",
                "programa.js",
                "JavaScript Files (*.js)"
            )

            if not file_path:
                return

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(codigo_js)

            self.window.statusBar().showMessage(
                f"JavaScript exportado: {file_path}"
            )

        except CompilerError as e:

            self.window.results_panel.show_error({

                "linea": e.linea,

                "error": "Error exportando JavaScript",

                "detalle": e.mensaje,

                "solucion": (
                    "Corrige el código "
                    "antes de exportar"
                )
            })

        except Exception as e:

            self.window.results_panel.show_error({

                "linea": 0,

                "error": "Error crítico",

                "detalle": str(e),

                "solucion": (
                    "Error interno del exportador"
                )
            })

    # =====================================================
    # EXPORTAR C#
    # =====================================================
    def exportar_csharp(self):

        codigo = self.window.editor_panel.get_code()

        if not codigo.strip():

            self.window.statusBar().showMessage(
                "No hay código para exportar"
            )

            return

        try:

            # =============================================
            # LEXER
            # =============================================

            lexer = Lexer(codigo)

            tokens, errores = lexer.analizar_con_errores()

            if errores:

                self.window.results_panel.show_error(
                    errores[0]
                )

                return

            # =============================================
            # PARSER
            # =============================================

            parser = Parser(tokens)

            ast = parser.parse()

            # =============================================
            # GENERATOR C#
            # =============================================

            generator = CSharpGenerator()

            generator.generate(ast)

            codigo_cs = generator.get_code()

            # =============================================
            # GUARDAR ARCHIVO
            # =============================================

            file_path, _ = QFileDialog.getSaveFileName(
                self.window,
                "Exportar C#",
                "programa.cs",
                "C# Files (*.cs)"
            )

            if not file_path:
                return

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(codigo_cs)

            self.window.statusBar().showMessage(
                f"C# exportado: {file_path}"
            )

        except CompilerError as e:

            self.window.results_panel.show_error({

                "linea": e.linea,

                "error": "Error exportando C#",

                "detalle": e.mensaje,

                "solucion": (
                    "Corrige el código "
                    "antes de exportar"
                )
            })

        except Exception as e:

            self.window.results_panel.show_error({

                "linea": 0,

                "error": "Error crítico",

                "detalle": str(e),

                "solucion": (
                    "Error interno del exportador"
                )
            })



    # =====================================================
    # ARCHIVOS
    # =====================================================

    def abrir_archivo(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Abrir Archivo",
            "",
            "Archivos (*.txt *.edu *.py *.js *.cs)"
        )

        if not file_path:
            return

        try:

            with open(file_path, "r", encoding="utf-8") as f:
                contenido = f.read()

            self.window.editor_panel.set_code(contenido)

            self.window.statusBar().showMessage(
                f"Archivo cargado: {file_path}"
            )

        except Exception as e:

            self.window.results_panel.show_error({
                "linea": 0,
                "error": "Error al abrir archivo",
                "detalle": str(e),
                "solucion": "Verifica el archivo"
            })

    # =====================================================
    # COMPILACIÓN
    # =====================================================

    def compilar(self):

        codigo = self.window.editor_panel.get_code()

        if not codigo.strip():

            self.window.statusBar().showMessage(
                "Editor vacío"
            )

            return

        self.window.results_panel.clear()

        try:

            # =================================================
            # LÉXICO
            # =================================================

            lexer = Lexer(codigo)

            tokens, errores = lexer.analizar_con_errores()

            if errores:

                self.window.results_panel.show_error(
                    errores[0]
                )

                return

            for token in tokens:
                self.window.results_panel.add_token(token)

            # =================================================
            # SINTÁCTICO
            # =================================================

            parser = Parser(tokens)

            ast = parser.parse()

            self.window.results_panel.load_ast(ast)

            # =================================================
            # SEMÁNTICO
            # =================================================

            semantic = AnalizadorSemantico()

            semantic.analizar(ast)
           
            # =================================================
            # GENERAR PYTHON
            # =================================================

            python_generator = PythonGenerator()

            python_generator.generate(ast)

            codigo_python = python_generator.get_code()

            print("\n===== PYTHON GENERADO =====\n")

            print(codigo_python)

            # =================================================
            # GENERAR JAVASCRIPT
            # =================================================

            js_generator = JavaScriptGenerator()

            js_generator.generate(ast)

            codigo_js = js_generator.get_code()

            print("\n===== JAVASCRIPT GENERADO =====\n")

            print(codigo_js)

            # =================================================
            # GENERAR C#
            # =================================================

            cs_generator = CSharpGenerator()

            cs_generator.generate(ast)

            codigo_cs = cs_generator.get_code()

            print("\n===== C# GENERADO =====\n")

            print(codigo_cs)

            # =================================================
            # RESULTADOS
            # =================================================

            salida = [
                str(x) for x in semantic.salida
            ]

            if not salida:
                salida = ["(Sin salida)"]

            self.window.results_panel.load_resultados(
                salida
            )

            # =================================================
            # TRAZA
            # =================================================

            traza_total = []

            if hasattr(parser, "traza"):
                traza_total.extend(parser.traza)

            if hasattr(semantic, "traza"):
                traza_total.extend(semantic.traza)

            self.window.results_panel.load_traza(
                traza_total
            )

            # =================================================
            # TABLA DE SÍMBOLOS
            # =================================================

            if hasattr(semantic, "scopes"):

                self.window.results_panel.load_simbolos(
                    semantic.scopes[0]
                )

            # =================================================
            # FINAL
            # =================================================

            self.window.statusBar().showMessage(
                "Compilación exitosa"
            )

        # =====================================================
        # ERRORES DEL COMPILADOR
        # =====================================================

        except CompilerError as e:

            self.window.results_panel.show_error({
                "linea": e.linea,
                "error": "Error de compilación",
                "detalle": e.mensaje,
                "solucion": "Revisa la sintaxis o semántica"
            })

        # =====================================================
        # ERRORES CRÍTICOS
        # =====================================================

        except Exception as e:

            self.window.results_panel.show_error({
                "linea": 0,
                "error": "Error crítico",
                "detalle": str(e),
                "solucion": "Error interno del compilador"
            })

    # =====================================================
    # LIMPIAR
    # =====================================================

    def limpiar(self):

        self.window.editor_panel.clear()

        self.window.results_panel.clear()

        self.window.statusBar().showMessage(
            "Editor limpiado"
        )

    # =====================================================
    # FUTURO
    # =====================================================

    def exportar_codigo(self):
        pass

    def importar_codigo(self):
        pass
