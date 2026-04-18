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

        esperado = valor if valor else tipo
        linea = tok.linea if tok else "-"
        raise Exception(f"Se esperaba {esperado} en línea {linea}")

    def parse(self):
        sentencias = []

        while self.actual():
            sentencias.append(self.sentencia())

        return Programa(sentencias)

    def sentencia(self):
        tok = self.actual()

        if tok.valor == "si":
            return self.if_stmt()

        if tok.valor == "escribir":
            return self.escribir()

        if tok.tipo == "IDENTIFICADOR":
            return self.asignacion()

        raise Exception(f"Sentencia inválida en línea {tok.linea}")

    def if_stmt(self):
        self.match("PALABRA_RESERVADA", "si")
        condicion = self.expresion()
        self.match("SIMBOLO", ":")

        cuerpo = []
        while self.actual():
            cuerpo.append(self.sentencia())
            break

        return If(condicion, cuerpo)

    def escribir(self):
        self.match("PALABRA_RESERVADA", "escribir")
        self.match("SIMBOLO", "(")
        valor = self.expresion()
        self.match("SIMBOLO", ")")
        return Escribir(valor)

    def asignacion(self):
        nombre = self.match("IDENTIFICADOR").valor
        self.match("OPERADOR", "=")

        tok = self.actual()

        if tok.tipo == "NUMERO":
            self.avanzar()
            valor = Numero(tok.valor)
        elif tok.tipo == "IDENTIFICADOR":
            self.avanzar()
            valor = Identificador(tok.valor)
        else:
            raise Exception(f"Valor inválido línea {tok.linea}")

        return Asignacion(nombre, valor)

    def expresion(self):
        return self.comparacion()

    def comparacion(self):
        nodo = self.termino()

        while self.actual() and self.actual().valor in (
            "==", "!=", "<", ">", "<=", ">="
        ):
            op = self.match("OPERADOR").valor
            derecho = self.termino()
            nodo = BinOp(nodo, op, derecho)

        return nodo

    def termino(self):
        tok = self.actual()

        if tok.tipo == "NUMERO":
            self.avanzar()
            return Numero(tok.valor)

        if tok.tipo == "IDENTIFICADOR":
            self.avanzar()
            return Identificador(tok.valor)

        if tok.valor == "(":
            self.match("SIMBOLO", "(")
            expr = self.expresion()
            self.match("SIMBOLO", ")")
            return expr

        raise Exception(f"Expresión inválida en línea {tok.linea}")