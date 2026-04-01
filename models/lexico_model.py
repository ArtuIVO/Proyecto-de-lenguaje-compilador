class Token:
    def __init__(self, tipo, valor, linea=1):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea


class Lexer:

    PALABRAS_RESERVADAS = {
        "si": "PALABRA_RESERVADA",
        "cuando": "PALABRA_RESERVADA",
        "ejecutar": "PALABRA_RESERVADA"
    }

    OPERADORES = {
        "y": "OPERADOR",
        "o": "OPERADOR",
        "no": "OPERADOR",
        "=": "OPERADOR",
        "<": "OPERADOR",
        ">": "OPERADOR",
        "==": "OPERADOR",
        "!=": "OPERADOR",
        "<=": "OPERADOR",
        ">=": "OPERADOR"
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
        tokens, _ = self.analizar_con_errores()
        return tokens

    def analizar_con_errores(self):
        errores = []
        linea = 1

        while self.pos < len(self.texto):
            char = self.texto[self.pos]

            # salto de línea
            if char == "\n":
                linea += 1
                self.pos += 1
                continue

            # espacios
            if char.isspace():
                self.pos += 1
                continue

            # identificadores o palabras reservadas
            if char.isalpha():
                token = self.identificador(linea)
                self.tokens.append(token)
                continue

            # números o error tipo 3jugador
            if char.isdigit():
                token = self.numero_o_error(linea)
                if token.tipo == "ERROR LEXICO":
                    errores.append({
                        "linea": linea,
                        "error": "Número inválido",
                        "detalle": token.valor,
                        "solucion": "Corrige el número o elimina el carácter no válido"
                    })
                self.tokens.append(token)
                continue

            # operadores compuestos 
            if self.peek(2) in self.OPERADORES:
                op = self.peek(2)
                self.tokens.append(Token("OPERADOR", op, linea))
                self.pos += 2
                continue

            # operadores simples
            if char in self.OPERADORES:
                self.tokens.append(Token("OPERADOR", char, linea))
                self.pos += 1
                continue

            # símbolos
            if char in self.SIMBOLOS:
                self.tokens.append(Token("SIMBOLO", char, linea))
                self.pos += 1
                continue

            # error léxico
            errores.append({
                    "linea": linea,
                    "error": "Carácter no reconocido",
                    "detalle": char,
                    "solucion": "Elimina el carácter o usa uno válido"
                })
            self.tokens.append(Token("ERROR LEXICO", char, linea))
            self.pos += 1

        return self.tokens, errores

    def identificador(self, linea):
        inicio = self.pos

        # solo letras
        while self.pos < len(self.texto) and self.texto[self.pos].isalpha():
            self.pos += 1

        palabra = self.texto[inicio:self.pos]

        # 🚨 ERROR: letras + números (ej: ejecutar3)
        if self.pos < len(self.texto) and self.texto[self.pos].isdigit():
            inicio_error = inicio

            while self.pos < len(self.texto) and self.texto[self.pos].isalnum():
                self.pos += 1

            valor = self.texto[inicio_error:self.pos]
            return Token("ERROR LEXICO", valor, linea)

        if palabra in self.PALABRAS_RESERVADAS:
            return Token("PALABRA_RESERVADA", palabra, linea)

        if palabra in self.OPERADORES:
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