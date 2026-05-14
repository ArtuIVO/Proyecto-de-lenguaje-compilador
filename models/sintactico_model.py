from models.ast_nodes import *
from models.error import CompilerError

class Parser:

    def __init__(self, tokens):
        self.traza = []
        self.tokens = tokens
        self.pos = 0

    # ---------------------

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

                self.traza.append({
                    "linea": tok.linea,
                    "token": tok.valor,
                    "accion": f"Match {tipo}",
                    "valido": True
                })

                self.avanzar()
                return tok

        linea = tok.linea if tok else 0

        self.traza.append({
            "linea": linea,
            "token": tok.valor if tok else "EOF",
            "accion": "Error sintáctico",
            "valido": False
        })

        raise CompilerError("Sintaxis inválida", linea)

    def saltar_newlines(self):
        while self.actual() and self.actual().tipo == "NEWLINE":
            self.avanzar()

    # ---------------------

    def parse(self):
        sentencias = []

        self.saltar_newlines()

        while self.actual():
            sentencias.append(self.sentencia())
            self.saltar_newlines()

        return Programa(sentencias)

    # ---------------------

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

        if tok.valor == "romper":

            self.avanzar()

            return Romper(tok.linea)


        if tok.valor == "continuar":

            self.avanzar()

            return Continuar(tok.linea)


        if tok.valor == "nulo":

            self.avanzar()

            return Nulo(tok.linea)

        TIPOS = {
            "entero",
            "decimal",
            "texto",
            "booleano",
            "lista"
        }

        if tok.valor in TIPOS:
            return self.declaracion_tipada()



        if tok.tipo == "IDENTIFICADOR":
             # 🔥 SI ES LLAMADA A FUNCIÓN
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].valor == "("
            ):
                return self.llamada()

            # 🔥 SI NO → ASIGNACIÓN
            return self.asignacion()

        raise CompilerError("Sentencia inválida", tok.linea if tok else 0)

    # ---------------------
    # BLOQUES (INDENT / DEDENT)

    def bloque(self):

        sentencias = []

        # ignorar líneas vacías
        while (
            self.actual()
            and self.actual().tipo == "NEWLINE"
        ):
            self.avanzar()

        self.match("INDENT")

        while self.actual():

            # ignorar líneas vacías internas
            while (
                self.actual()
                and self.actual().tipo == "NEWLINE"
            ):
                self.avanzar()

            if (
                self.actual()
                and self.actual().tipo == "DEDENT"
            ):
                break

            sentencias.append(
                self.sentencia()
            )

        self.match("DEDENT")

        return sentencias


    # ---------------------
    # SENTENCIAS

    def asignacion(self):
        tok = self.match("IDENTIFICADOR")
        nombre = tok.valor

        self.match("OPERADOR", "=")
        valor = self.expresion()

        return Asignacion(nombre, valor, tok.linea)
    
    def declaracion_tipada(self):

        tipo_tok = self.match(
            "PALABRA_RESERVADA"
        )

        tipo = tipo_tok.valor

        nombre = self.match(
            "IDENTIFICADOR"
        ).valor

        self.match("OPERADOR", "=")

        valor = self.expresion()

        return DeclaracionTipada(
            tipo,
            nombre,
            valor,
            tipo_tok.linea
        )
    
    def escribir(self):
        tok = self.match("PALABRA_RESERVADA", "escribir")

        self.match("SIMBOLO", "(")
        valor = self.expresion()
        self.match("SIMBOLO", ")")

        return Escribir(valor, tok.linea)

    # ---------------------

    def funcion_stmt(self):
        tok = self.match("PALABRA_RESERVADA", "funcion")

        nombre = self.match("IDENTIFICADOR").valor

        self.match("SIMBOLO", "(")

        parametros = []

        if self.actual().tipo == "IDENTIFICADOR":
            parametros.append(self.match("IDENTIFICADOR").valor)

            while self.actual().valor == ",":
                self.match("SIMBOLO", ",")
                parametros.append(self.match("IDENTIFICADOR").valor)

        self.match("SIMBOLO", ")")
        self.match("SIMBOLO", ":")
        self.match("NEWLINE")

        cuerpo = self.bloque()

        return Funcion(nombre, parametros, cuerpo, tok.linea)

    def retornar_stmt(self):
        tok = self.match("PALABRA_RESERVADA", "retornar")
        valor = self.expresion()
        return Retornar(valor, tok.linea)

    # ---------------------

    def if_stmt(self):
        tok = self.match("PALABRA_RESERVADA", "si")

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

        return If(condicion, cuerpo, sino, tok.linea)

    # ---------------------

    def while_stmt(self):
        tok = self.match("PALABRA_RESERVADA", "mientras")

        condicion = self.expresion()

        self.match("SIMBOLO", ":")
        self.match("NEWLINE")

        cuerpo = self.bloque()

        return While(condicion, cuerpo, tok.linea)

    # ---------------------

    def para_stmt(self):
        tok = self.match("PALABRA_RESERVADA", "para")

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

        return Para(variable, inicio, fin, cuerpo, tok.linea)

    # ---------------------
    # EXPRESIONES

    def expresion(self):
        return self.expresion_logica()

    def expresion_logica(self):

        nodo = self.comparacion()

        while (
            self.actual()
            and self.actual().valor in [
                "y",
                "o"
            ]
        ):

            op = self.actual()

            self.avanzar()

            derecho = self.comparacion()

            nodo = LogicalOp(
                nodo,
                op.valor,
                derecho,
                op.linea
            )

        return nodo

    def comparacion(self):
        nodo = self.aritmetica()

        while self.actual() and self.actual().valor in (
            "==", "!=", "<", ">", "<=", ">="
        ):
            op = self.match("OPERADOR")
            derecho = self.aritmetica()
            nodo = BinOp(nodo, op.valor, derecho, op.linea)

        return nodo

    def aritmetica(self):
        nodo = self.termino()

        while self.actual() and self.actual().valor in ("+", "-"):
            op = self.match("OPERADOR")
            derecho = self.termino()
            nodo = BinOp(nodo, op.valor, derecho, op.linea)

        return nodo

    def termino(self):
        nodo = self.factor()

        while self.actual() and self.actual().valor in ("*", "/"):
            op = self.match("OPERADOR")
            derecho = self.factor()
            nodo = BinOp(nodo, op.valor, derecho, op.linea)

        return nodo

    # ---------------------

    def factor(self):
        tok = self.actual()

        if tok.valor in ("+","-","no"):
            self.avanzar()
            valor = self.factor()
            return UnaryOp(tok.valor, valor, tok.linea)
        
        if (tok.tipo == "PALABRA_RESERVADA" and tok.valor == "nulo"):
            self.avanzar()
            return Nulo(tok.linea)
        
        if tok.tipo == "NUMERO":
            self.avanzar()
            return Numero(tok.valor, tok.linea)

        if tok.tipo == "STRING":
            self.avanzar()
            return Cadena(tok.valor, tok.linea)

        if tok.valor == "[":
            return self.lista_literal()
        
        if (
            tok.tipo == "PALABRA_RESERVADA"
            and tok.valor in ("verdadero", "falso")
        ):
            self.avanzar()
            return Booleano(tok.valor == "verdadero", tok.linea)
        

        if tok.tipo == "IDENTIFICADOR":

            # acceso lista
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
            return Identificador(tok.valor, tok.linea)

        if tok.valor == "(":
            self.match("SIMBOLO", "(")
            expr = self.expresion()
            self.match("SIMBOLO", ")")
            return expr

        raise CompilerError("Expresión inválida", tok.linea if tok else 0)

    # ---------------------

    def llamada(self):
        tok = self.match("IDENTIFICADOR")
        nombre = tok.valor

        self.match("SIMBOLO", "(")

        args = []

        if self.actual().valor != ")":
            args.append(self.expresion())

            while self.actual().valor == ",":
                self.match("SIMBOLO", ",")
                args.append(self.expresion())

        self.match("SIMBOLO", ")")

        return Llamada(nombre, args, tok.linea)

    # ---------------------

    def lista_literal(self):
        tok = self.match("SIMBOLO", "[")

        elementos = []

        if self.actual().valor != "]":
            elementos.append(self.expresion())

            while self.actual().valor == ",":
                self.match("SIMBOLO", ",")
                elementos.append(self.expresion())

        self.match("SIMBOLO", "]")

        return Lista(elementos, tok.linea)

    # ---------------------

    def acceso_lista(self):
        tok = self.match("IDENTIFICADOR")
        nombre = tok.valor

        self.match("SIMBOLO", "[")

        indice = self.expresion()

        self.match("SIMBOLO", "]")

        return AccesoLista(nombre, indice, tok.linea)