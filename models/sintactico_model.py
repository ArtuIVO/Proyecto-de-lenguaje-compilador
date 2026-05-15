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
        while self.actual() and self.actual().tipo == "NEWLINE": #type: ignore
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

        if tok.valor == "funcion": #type: ignore
            return self.funcion_stmt()

        if tok.valor == "retornar": #type: ignore
            return self.retornar_stmt()

        if tok.valor == "escribir": #type: ignore
            return self.escribir()

        if tok.valor == "si": #type: ignore
            return self.if_stmt()

        if tok.valor == "mientras": #type: ignore
            return self.while_stmt()

        if tok.valor == "para": #type: ignore
            return self.para_stmt()

        if tok.valor == "romper": #type: ignore

            self.avanzar()

            return Romper(tok.linea)#type: ignore


        if tok.valor == "continuar": #type: ignore

            self.avanzar()

            return Continuar(tok.linea) #type: ignore

        TIPOS = {
            "entero",
            "decimal",
            "texto",
            "booleano",
            "lista"
        }

        if tok.valor in TIPOS: #type: ignore
            return self.declaracion_tipada()



        if tok.tipo == "IDENTIFICADOR": #type: ignore
             # SI ES LLAMADA A FUNCIÓN
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].valor == "("
            ):
                return self.expresion()

            # SI NO → ASIGNACIÓN
            return self.asignacion()

        raise CompilerError("Sentencia inválida", tok.linea if tok else 0)

    # ---------------------
    # BLOQUES (INDENT / DEDENT)

    def bloque(self):

        sentencias = []

        # ignorar líneas vacías
        while (
            self.actual()
            and self.actual().tipo == "NEWLINE" #type: ignore
        ):
            self.avanzar()

        self.match("INDENT")

        while self.actual():

            # ignorar líneas vacías internas
            while (
                self.actual()
                and self.actual().tipo == "NEWLINE" #type: ignore
            ):
                self.avanzar()

            if (
                self.actual()
                and self.actual().tipo == "DEDENT" #type: ignore
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

        if self.actual().tipo == "IDENTIFICADOR": #type: ignore
            parametros.append(self.match("IDENTIFICADOR").valor)

            while self.actual().valor == ",": #type: ignore
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

        if self.actual() and self.actual().valor == "sino": #type: ignore
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
            and self.actual().valor in [ #type: ignore
                "y",
                "o"
            ]
        ):

            op = self.actual()

            self.avanzar()

            derecho = self.comparacion()

            nodo = LogicalOp(
                nodo,
                op.valor, #type: ignore
                derecho,
                op.linea #type: ignore
            )

        return nodo

    def comparacion(self):
        nodo = self.aritmetica()

        while self.actual() and self.actual().valor in ( #type: ignore
            "==", "!=", "<", ">", "<=", ">="
        ):
            op = self.match("OPERADOR")
            derecho = self.aritmetica()
            nodo = BinOp(nodo, op.valor, derecho, op.linea)

        return nodo

    def aritmetica(self):
        nodo = self.termino()

        while self.actual() and self.actual().valor in ("+", "-"): #type: ignore
            op = self.match("OPERADOR")
            derecho = self.termino()
            nodo = BinOp(nodo, op.valor, derecho, op.linea)

        return nodo

    def termino(self):
        nodo = self.factor()

        while self.actual() and self.actual().valor in ("*", "/"): #type: ignore
            op = self.match("OPERADOR")
            derecho = self.factor()
            nodo = BinOp(nodo, op.valor, derecho, op.linea)

        return nodo

    # ---------------------

    def factor(self):
        tok = self.actual()

        if tok.valor in ("+","-","no"): #type: ignore
            self.avanzar() 
            valor = self.factor()
            return UnaryOp(tok.valor, valor, tok.linea) #type: ignore
        
        if (tok.tipo == "PALABRA_RESERVADA" and tok.valor == "nulo"): #type: ignore
            self.avanzar()
            return Nulo(tok.linea) #type: ignore
        
        if tok.tipo == "NUMERO": #type: ignore
            self.avanzar()
            return Numero(tok.valor, tok.linea) #type: ignore

        if tok.tipo == "STRING": #type: ignore
            self.avanzar()
            return Cadena(tok.valor, tok.linea) #type: ignore

        if tok.valor == "[": #type: ignore
            return self.lista_literal()
  
        if tok.valor == "{": #type: ignore

            return self.diccionario()

        if (
            tok.tipo == "PALABRA_RESERVADA" #type: ignore
            and tok.valor in ("verdadero", "falso") #type: ignore
        ):
            self.avanzar()
            return Booleano(tok.valor == "verdadero", tok.linea) #type: ignore
        

       
        if tok.tipo == "IDENTIFICADOR": #type: ignore

            self.avanzar()

            nodo = Identificador(
                tok.valor, #type: ignore
                tok.linea #type: ignore
            )

            while self.actual():

                # ========================================
                # LLAMADA
                # ========================================

                if self.actual().valor == "(": #type: ignore

                    nodo = self.llamada_desde(
                        nodo
                    )

                # ========================================
                # ACCESO []
                # ========================================

                elif self.actual().valor == "[": #type: ignore

                    self.avanzar()

                    indice = self.expresion()

                    self.match(
                        "SIMBOLO",
                        "]"
                    )

                    nodo = Acceso(
                        nodo,
                        indice,
                        tok.linea #type: ignore
                    )

                else:

                    break

            return nodo


        if tok.valor == "(": #type: ignore
            self.match("SIMBOLO", "(")
            expr = self.expresion()
            self.match("SIMBOLO", ")")
            return expr

        raise CompilerError("Expresión inválida", tok.linea if tok else 0)

    # ---------------------

    def llamada_desde(self, nodo_base):

        self.match(
            "SIMBOLO",
            "("
        )

        argumentos = []

        while (
            self.actual()
            and self.actual().valor != ")" #type: ignore
        ):

            argumentos.append(
                self.expresion()
            )

            if (
                self.actual()
                and self.actual().valor == "," #type: ignore
            ):

                self.avanzar()

        self.match(
            "SIMBOLO",
            ")"
        )

        return Llamada(
            nodo_base.nombre,
            argumentos,
            nodo_base.linea
        )


    def diccionario(self):

        pares = []

        llave = self.match(
            "SIMBOLO",
            "{"
        )

        while (
            self.actual()
            and self.actual().valor != "}" #type: ignore
        ):
            while (
                self.actual()
                and self.actual().tipo == "NEWLINE" # type: ignore
            ):
                self.avanzar()



            # ============================================
            # CLAVE
            # ============================================

            clave = self.expresion()

            # ============================================
            # :
            # ============================================

            self.match(
                "SIMBOLO",
                ":"
            )

            # ============================================
            # VALOR
            # ============================================

            valor = self.expresion()

            pares.append(
                (clave, valor)
            )

            # ============================================
            # ,
            # ============================================

            if (
                self.actual()
                and self.actual().valor == "," #type: ignore
            ):

                self.avanzar()
                while (
                    self.actual()
                    and self.actual().tipo == "NEWLINE" # type: ignore
                ):
                    self.avanzar()
                


        self.match(
            "SIMBOLO",
            "}"
        )

        return Diccionario(
            pares,
            llave.linea
        )


    # ---------------------
    def lista_literal(self):

        tok = self.match("SIMBOLO", "[")

        elementos = []

        while (
            self.actual()
            and self.actual().tipo == "NEWLINE" # type: ignore
        ):
            self.avanzar()

        if self.actual().valor != "]": # type: ignore

            elementos.append(
                self.expresion()
            )

            while self.actual().valor == ",": # type: ignore

                self.match("SIMBOLO", ",")

                while (
                    self.actual()
                    and self.actual().tipo == "NEWLINE" # type: ignore
                ):
                    self.avanzar()

                elementos.append(
                    self.expresion()
                )

        self.match("SIMBOLO", "]")

        return Lista(
            elementos,
            tok.linea
        )
