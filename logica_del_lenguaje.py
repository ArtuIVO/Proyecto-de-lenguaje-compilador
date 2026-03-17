class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor


class Lexer:

    PALABRAS_RESERVADAS = {
        "si": "PALABRA_RESERVADA",
        "cuando": "PALABRA_RESERVADA",
        "ejecutar": "PALABRA_RESERVADA"
    }

    OPERADORES = {
        "y": "OPERADOR",
        "o": "OPERADOR",
        "no": "OPERADOR"
    }

    SIMBOLOS = {
        "(": "SIMBOLO",
        ")": "SIMBOLO",
        ":": "SIMBOLO",
        ",": "SIMBOLO"
    }

    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.tokens = []

    def analizar(self):
        while self.pos < len(self.texto):
            char = self.texto[self.pos]

            if char.isspace():
                self.pos += 1

            elif char.isalpha():
                self.tokens.append(self.identificador())

            elif char.isdigit():
                self.tokens.append(self.numero())

            elif char in self.SIMBOLOS:
                self.tokens.append(Token(self.SIMBOLOS[char], char))
                self.pos += 1

            else:
                print(f"{char} -> ERROR LEXICO")
                self.pos += 1

        return self.tokens

    def identificador(self):
        inicio = self.pos

        while self.pos < len(self.texto) and self.texto[self.pos].isalnum():
            self.pos += 1

        palabra = self.texto[inicio:self.pos]

        if palabra in self.PALABRAS_RESERVADAS:
            return Token("PALABRA_RESERVADA", palabra)

        elif palabra in self.OPERADORES:
            return Token("OPERADOR", palabra)

        return Token("IDENTIFICADOR", palabra)

    def numero(self):
        inicio = self.pos

        while self.pos < len(self.texto) and self.texto[self.pos].isdigit():
            self.pos += 1

        return Token("NUMERO", self.texto[inicio:self.pos])


# =========================
# PARSER
# =========================

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self, valor=None, tipo=None):
        token = self.actual()

        if token is None:
            raise SyntaxError("Fin inesperado")

        if valor and token.valor != valor:
            raise SyntaxError(f"Se esperaba '{valor}'")

        if tipo and token.tipo != tipo:
            raise SyntaxError(f"Se esperaba tipo {tipo}")

        self.pos += 1
        return token

    def parse(self):
        while self.actual() is not None:
            self.regla()

    def regla(self):
        token = self.actual()

        if token.valor == "si": # type: ignore
            self.regla_si()

        elif token.valor == "cuando": # type: ignore
            self.regla_cuando()

        else:
            raise SyntaxError("Regla inválida")

    def regla_si(self):
        self.consumir(valor="si")
        self.consumir(valor="(")
        self.estado()
        self.consumir(valor=")")
        self.consumir(valor=":")
        self.consumir(valor="ejecutar")
        self.lista_acciones()

    def regla_cuando(self):
        self.consumir(valor="cuando")
        self.consumir(tipo="IDENTIFICADOR")
        self.consumir(valor=":")
        self.consumir(valor="ejecutar")
        self.lista_acciones()

    def estado(self):
        self.consumir(tipo="IDENTIFICADOR")
        self.consumir(tipo="IDENTIFICADOR")
        self.consumir(tipo="IDENTIFICADOR")

    def lista_acciones(self):
        self.accion()

        while self.actual() and self.actual().valor == ",": # type: ignore
            self.consumir(valor=",")
            self.accion()

    def accion(self):
        self.consumir(tipo="IDENTIFICADOR")

        if self.actual() and self.actual().tipo == "IDENTIFICADOR": # type: ignore
            self.consumir(tipo="IDENTIFICADOR")

        elif self.actual() and self.actual().tipo == "NUMERO": # type: ignore
            self.consumir(tipo="NUMERO")