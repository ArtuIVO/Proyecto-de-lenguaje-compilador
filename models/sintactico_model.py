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

        raise Exception("Sintaxis inválida")

    def saltar_newlines(self):
        while self.actual() and self.actual().tipo == "NEWLINE":
            self.avanzar()

    # ----------------------------------

    def parse(self):

        sentencias = []

        self.saltar_newlines()

        while self.actual():
            sentencias.append(self.sentencia())
            self.saltar_newlines()

        return Programa(sentencias)

    # ----------------------------------

    def sentencia(self):

        tok = self.actual()

        if tok.valor == "funcion":
            return self.funcion_stmt()

        if tok.valor == "retornar":
            return self.retornar_stmt()

        if tok.valor == "escribir":
            return self.escribir()

        if tok.valor == "si":
            return self.if_stmt()

        if tok.valor == "mientras":
            return self.while_stmt()

        if tok.valor == "para":
            return self.para_stmt()

        if tok.tipo == "IDENTIFICADOR":
            return self.asignacion()

        raise Exception("Sentencia inválida")
    
    # ----------------------------------
    def para_stmt(self):

        self.match("PALABRA_RESERVADA", "para")

        variable = self.match("IDENTIFICADOR").valor

        self.match("PALABRA_RESERVADA", "en")

        self.match("PALABRA_RESERVADA", "rango")

        self.match("SIMBOLO", "(")

        inicio = self.expresion()

        self.match("SIMBOLO", ",")

        fin = self.expresion()

        self.match("SIMBOLO", ")")

        self.match("SIMBOLO", ":")

        self.match("NEWLINE")

        cuerpo = self.bloque()

        return Para(variable, inicio, fin, cuerpo)

    def bloque(self):

        sentencias = []

        self.match("INDENT")

        self.saltar_newlines()

        while self.actual() and self.actual().tipo != "DEDENT":
            sentencias.append(self.sentencia())
            self.saltar_newlines()

        self.match("DEDENT")

        return sentencias

    # ----------------------------------

    def funcion_stmt(self):

        self.match("PALABRA_RESERVADA", "funcion")

        nombre = self.match("IDENTIFICADOR").valor

        self.match("SIMBOLO", "(")

        parametros = []

        if self.actual().tipo == "IDENTIFICADOR":
            parametros.append(self.match("IDENTIFICADOR").valor)

            while self.actual().valor == ",":
                self.match("SIMBOLO", ",")
                parametros.append(
                    self.match("IDENTIFICADOR").valor
                )

        self.match("SIMBOLO", ")")

        self.match("SIMBOLO", ":")

        self.match("NEWLINE")

        cuerpo = self.bloque()

        return Funcion(nombre, parametros, cuerpo)

    # ----------------------------------

    def retornar_stmt(self):

        self.match("PALABRA_RESERVADA", "retornar")

        valor = self.expresion()

        return Retornar(valor)

    # ----------------------------------

    def asignacion(self):

        nombre = self.match("IDENTIFICADOR").valor

        self.match("OPERADOR", "=")

        valor = self.expresion()

        return Asignacion(nombre, valor)

    def escribir(self):

        self.match("PALABRA_RESERVADA", "escribir")
        self.match("SIMBOLO", "(")

        valor = self.expresion()

        self.match("SIMBOLO", ")")

        return Escribir(valor)

    # ----------------------------------

    def if_stmt(self):

        self.match("PALABRA_RESERVADA", "si")

        condicion = self.expresion()

        self.match("SIMBOLO", ":")

        self.match("NEWLINE")

        cuerpo = self.bloque()

        sino = []

        self.saltar_newlines()

        if self.actual() and self.actual().valor == "sino":

            self.match("PALABRA_RESERVADA", "sino")
            self.match("SIMBOLO", ":")
            self.match("NEWLINE")

            sino = self.bloque()

        return If(condicion, cuerpo, sino)

    def while_stmt(self):

        self.match("PALABRA_RESERVADA", "mientras")

        condicion = self.expresion()

        self.match("SIMBOLO", ":")

        self.match("NEWLINE")

        cuerpo = self.bloque()

        return While(condicion, cuerpo)

    # ----------------------------------

    def expresion(self):
        return self.comparacion()

    def comparacion(self):

        nodo = self.aritmetica()

        while self.actual() and self.actual().valor in (
            "==", "!=", "<", ">", "<=", ">="
        ):
            op = self.match("OPERADOR").valor
            derecho = self.aritmetica()
            nodo = BinOp(nodo, op, derecho)

        return nodo

    def aritmetica(self):

        nodo = self.termino()

        while self.actual() and self.actual().valor in ("+", "-"):
            op = self.match("OPERADOR").valor
            derecho = self.termino()
            nodo = BinOp(nodo, op, derecho)

        return nodo

    def termino(self):

        nodo = self.factor()

        while self.actual() and self.actual().valor in ("*", "/"):
            op = self.match("OPERADOR").valor
            derecho = self.factor()
            nodo = BinOp(nodo, op, derecho)

        return nodo

    def factor(self):

        tok = self.actual()

        if tok.tipo == "STRING":
            self.avanzar()
            return Cadena(tok.valor)
        

        # número
        if tok.tipo == "NUMERO":
            self.avanzar()
            return Numero(tok.valor)

        # lista literal [1,2,3]
        if tok.valor == "[":
            return self.lista_literal()

        # identificador
        if tok.tipo == "IDENTIFICADOR":

            # acceso lista nums[0]
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].valor == "["
            ):
                return self.acceso_lista()

            # llamada función
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].valor == "("
            ):
                return self.llamada()

            self.avanzar()
            return Identificador(tok.valor)

        # paréntesis
        if tok.valor == "(":
            self.match("SIMBOLO", "(")
            expr = self.expresion()
            self.match("SIMBOLO", ")")
            return expr

        raise Exception("Expresión inválida")
    # ----------------------------------

    def llamada(self):

        nombre = self.match("IDENTIFICADOR").valor

        self.match("SIMBOLO", "(")

        argumentos = []

        if self.actual().valor != ")":
            argumentos.append(self.expresion())

            while self.actual().valor == ",":
                self.match("SIMBOLO", ",")
                argumentos.append(self.expresion())

        self.match("SIMBOLO", ")")

        return Llamada(nombre, argumentos)
    
    def lista(self):

        self.match("SIMBOLO", "[")

        elementos = []

        if self.actual().valor != "]":

            elementos.append(self.expresion())

            while self.actual().valor == ",":
                self.match("SIMBOLO", ",")
                elementos.append(self.expresion())

        self.match("SIMBOLO", "]")

        return Lista(elementos)
    
    def lista_literal(self):

        self.match("SIMBOLO", "[")

        elementos = []

        if self.actual().valor != "]":

            elementos.append(self.expresion())

            while self.actual().valor == ",":
                self.match("SIMBOLO", ",")
                elementos.append(self.expresion())

        self.match("SIMBOLO", "]")

        return Lista(elementos)
    
    def acceso_lista(self):

        nombre = self.match("IDENTIFICADOR").valor

        self.match("SIMBOLO", "[")

        indice = self.expresion()

        self.match("SIMBOLO", "]")

        return AccesoLista(nombre, indice)