class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
        self.linea = 1

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

class _LexerCapturador(Lexer):
    def analizar_con_errores(self) -> tuple[list[Token], list[str]]:
        errores = []
        linea_actual = 1

        while self.pos < len(self.texto):
            char = self.texto[self.pos]

            if char == "\n":
                linea_actual += 1
                self.pos += 1
            elif char.isspace():
                self.pos += 1
            elif char.isalpha():
                t = self.identificador()
                t.linea = linea_actual
                self.tokens.append(t)
            elif char.isdigit():
                t = self.numero()
                t.linea = linea_actual
                self.tokens.append(t)
            elif char in self.SIMBOLOS:
                t = Token(self.SIMBOLOS[char], char)
                t.linea = linea_actual
                self.tokens.append(t)
                self.pos += 1
            else:
                errores.append(
                    f"Línea {linea_actual}: carácter no reconocido '{char}'"
                )
                self.pos += 1

        return self.tokens, errores


class LexicoModel:
    def analizar(self, codigo: str) -> tuple[list[Token], list[str]]:
        lexer = _LexerCapturador(codigo)
        return lexer.analizar_con_errores()