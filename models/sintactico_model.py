from models.ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def avanzar(self):
        self.pos += 1

    def match(self, tipo, valor=None):
        tok = self.actual()
        if tok and tok.tipo == tipo:
            if valor is None or tok.valor == valor:
                self.avanzar()
                return tok
        return None

    def parse(self):
        sentencias = []
        while self.actual():
            sentencias.append(self.sentencia())
        return Programa(sentencias)

    def sentencia(self):
        tok = self.actual()

        if tok.valor == "si": #type: ignore
            return self.if_stmt()

        if tok.tipo == "IDENTIFICADOR": #type: ignore
            return self.asignacion()

        raise Exception(f"Error sintáctico en línea {tok.linea}") # type: ignore

    def if_stmt(self):
        self.match("PALABRA_RESERVADA", "si")
        condicion = self.expresion()
        self.match("SIMBOLO", ":")
        cuerpo = [self.sentencia()]
        return If(condicion, cuerpo)

    def asignacion(self):
        nombre = self.match("IDENTIFICADOR").valor #type: ignore
        self.match("OPERADOR", "=")
        valor = self.expresion()
        return Asignacion(nombre, valor)

    def expresion(self):
        izquierda = self.termino()

        tok = self.actual()
        if tok and tok.tipo == "OPERADOR":
            op = tok.valor
            self.avanzar()
            derecha = self.expresion()
            return BinOp(izquierda, op, derecha)

        return izquierda

    def termino(self):
        tok = self.actual()

        if tok.tipo == "NUMERO": #type: ignore
            self.avanzar()
            return Numero(tok.valor) #type: ignore

        if tok.tipo == "IDENTIFICADOR": #type: ignore
            self.avanzar()
            return Identificador(tok.valor) #type: ignore

        raise Exception(f"Error en expresión línea {tok.linea}") #type: ignore