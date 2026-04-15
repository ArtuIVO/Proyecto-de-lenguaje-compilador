from models.semantico_model import AnalizadorSemantico

class Interprete:
    def ejecutar(self, ast):
        sem = AnalizadorSemantico()
        sem.analizar(ast)
        return sem.salida 