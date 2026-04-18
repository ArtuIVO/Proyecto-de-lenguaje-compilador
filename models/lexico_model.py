class Token:
    def __init__(self, tipo, valor, linea=1):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea


class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea


class Lexer:

    PALABRAS = {"si", "escribir", "cuando", "ejecutar"}

    OPERADORES = {
        "==", "!=", "<=", ">=",
        "=",
        "<", ">"
    }

    SIMBOLOS = {"(", ")", ":"}

    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.linea = 1

    def actual(self):
        if self.pos < len(self.texto):
            return self.texto[self.pos]
        return None

    def avanzar(self):
        self.pos += 1

    def analizar_con_errores(self):
        tokens = []
        errores = []

        while self.pos < len(self.texto):

            c = self.actual()

            if c == "\n":
                self.linea += 1
                self.avanzar()
                continue

            if c.isspace():
                self.avanzar()
                continue

            # letras
            if c.isalpha():
                inicio = self.pos

                while self.actual() and self.actual().isalnum():
                    self.avanzar()

                palabra = self.texto[inicio:self.pos]

                if palabra in self.PALABRAS:
                    tokens.append(Token("PALABRA_RESERVADA", palabra, self.linea))
                else:
                    tokens.append(Token("IDENTIFICADOR", palabra, self.linea))

                continue

            # numeros
            if c.isdigit():
                inicio = self.pos

                while self.actual() and self.actual().isdigit():
                    self.avanzar()

                numero = self.texto[inicio:self.pos]
                tokens.append(Token("NUMERO", numero, self.linea))
                continue

            # operadores dobles
            doble = self.texto[self.pos:self.pos+2]

            if doble in self.OPERADORES:
                tokens.append(Token("OPERADOR", doble, self.linea))
                self.pos += 2
                continue

            # operadores simples
            if c in self.OPERADORES:
                tokens.append(Token("OPERADOR", c, self.linea))
                self.avanzar()
                continue

            # símbolos
            if c in self.SIMBOLOS:
                tokens.append(Token("SIMBOLO", c, self.linea))
                self.avanzar()
                continue

            errores.append({
                "linea": self.linea,
                "error": "Carácter inválido",
                "detalle": c,
                "solucion": "Elimine ese carácter"
            })

            self.avanzar()

        return tokens, errores

    def identificador(self, linea):
        inicio = self.pos

        while self.pos < len(self.texto) and self.texto[self.pos].isalpha():
            self.pos += 1

        palabra = self.texto[inicio:self.pos]

        # error tipo ejecutar3
        if self.pos < len(self.texto) and self.texto[self.pos].isdigit():

            while self.pos < len(self.texto) and self.texto[self.pos].isalnum():
                self.pos += 1

            valor = self.texto[inicio:self.pos]
            return Token("ERROR LEXICO", valor, linea)

        if palabra in self.PALABRAS_RESERVADAS:
            return Token("PALABRA_RESERVADA", palabra, linea)

        if palabra in self.OPERADORES_PALABRA:
            return Token("OPERADOR", palabra, linea)

        return Token("IDENTIFICADOR", palabra, linea)

    def numero_o_error(self, linea):
        inicio = self.pos

        while self.pos < len(self.texto) and self.texto[self.pos].isdigit():
            self.pos += 1

        
        if self.pos < len(self.texto) and self.texto[self.pos].isalpha():
            while self.pos < len(self.texto) and self.texto[self.pos].isalnum():
                self.pos += 1

            valor = self.texto[inicio:self.pos]
            return Token("ERROR LEXICO", valor, linea)

        return Token("NUMERO", self.texto[inicio:self.pos], linea)

    def peek(self, n):
        return self.texto[self.pos:self.pos + n]


class LexicoModel:
    def analizar(self, codigo: str):
        lexer = Lexer(codigo)
        return lexer.analizar_con_errores()