class Token:
    def __init__(self, tipo, valor, linea=1):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self):
        return f"{self.tipo}({self.valor})"


class Lexer:

    PALABRAS = {
        "si",
        "sino",
        "mientras",
        "escribir",
        "cuando",
        "ejecutar",
        "funcion",
        "retornar",
        "para",
        "en",
        "rango",
        "npc",
        "hablar",
        "mover",
        "patrullar",
        "atacar",
        "vida",
        "animar",
        "esperar",
        "ruta",
    }

    OPERADORES = {
        "==", "!=", "<=", ">=",
        "=",
        "<", ">",
        "+", "-", "*", "/"
    }

    SIMBOLOS = {
        "(", ")",
        "[", "]",
        ":",
        ","
    }

    def __init__(self, texto):
        self.texto = texto.replace("\t", "    ")
        self.pos = 0
        self.linea = 1

        self.indent_stack = [0]
        self.inicio_linea = True

    # ---------------------

    def actual(self):
        if self.pos < len(self.texto):
            return self.texto[self.pos]
        return None

    def avanzar(self):
        self.pos += 1

    def mirar(self, n=1):
        return self.texto[self.pos:self.pos+n]

    # ---------------------

    def analizar_con_errores(self):

        tokens = []
        errores = []

        while self.pos < len(self.texto):

            # ---------------- INDENTACIÓN ----------------
            if self.inicio_linea:

                espacios = 0

                while self.actual() == " ":
                    espacios += 1
                    self.avanzar()

                # línea vacía
                if self.actual() == "\n":
                    tokens.append(Token("NEWLINE", "\\n", self.linea))
                    self.linea += 1
                    self.avanzar()
                    continue

                self.inicio_linea = False

                actual_indent = self.indent_stack[-1]

                if espacios > actual_indent:
                    self.indent_stack.append(espacios)
                    tokens.append(Token("INDENT", "INDENT", self.linea))

                elif espacios < actual_indent:
                    while self.indent_stack[-1] > espacios:
                        self.indent_stack.pop()
                        tokens.append(Token("DEDENT", "DEDENT", self.linea))

            # --------------------------------------------

            c = self.actual()

            if c is None:
                break

            # salto línea
            if c == "\n":
                tokens.append(Token("NEWLINE", "\\n", self.linea))
                self.linea += 1
                self.avanzar()
                self.inicio_linea = True
                continue

            # espacios internos
            if c.isspace():
                self.avanzar()
                continue

            # ---------- IDENTIFICADOR ----------
            if c.isalpha():

                inicio = self.pos

                while self.actual() and self.actual().isalnum():
                    self.avanzar()

                palabra = self.texto[inicio:self.pos]

                if palabra in self.PALABRAS:
                    tokens.append(
                        Token("PALABRA_RESERVADA", palabra, self.linea)
                    )
                else:
                    tokens.append(
                        Token("IDENTIFICADOR", palabra, self.linea)
                    )

                continue

            # strings
            if c == '"':
                self.avanzar()
                inicio = self.pos

                while self.actual() and self.actual() != '"':
                    self.avanzar()

                texto = self.texto[inicio:self.pos]

                if self.actual() != '"':
                    errores.append({
                        "linea": self.linea,
                        "error": "Cadena sin cerrar",
                        "detalle": texto,
                        "solucion": 'Cerrar con comillas "'
                    })
                else:
                    self.avanzar()
                    tokens.append(Token("STRING", texto, self.linea))

                continue

            # ---------- NÚMEROS ----------
            if c.isdigit():

                inicio = self.pos

                while self.actual() and self.actual().isdigit():
                    self.avanzar()

                numero = self.texto[inicio:self.pos]

                tokens.append(
                    Token("NUMERO", numero, self.linea)
                )

                continue

            # ---------- OPERADOR DOBLE ----------
            doble = self.mirar(2)

            if doble in self.OPERADORES:
                tokens.append(
                    Token("OPERADOR", doble, self.linea)
                )
                self.pos += 2
                continue

            # ---------- OPERADOR SIMPLE ----------
            if c in self.OPERADORES:
                tokens.append(
                    Token("OPERADOR", c, self.linea)
                )
                self.avanzar()
                continue

            # ---------- SÍMBOLOS ----------
            if c in self.SIMBOLOS:
                tokens.append(
                    Token("SIMBOLO", c, self.linea)
                )
                self.avanzar()
                continue

            # ---------- ERROR ----------
            errores.append({
                "linea": self.linea,
                "error": "Carácter inválido",
                "detalle": c,
                "solucion": "Elimine ese carácter"
            })

            self.avanzar()

        # cerrar indentaciones abiertas
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(Token("DEDENT", "DEDENT", self.linea))

        return tokens, errores


class LexicoModel:
    def analizar(self, codigo):
        lexer = Lexer(codigo)
        return lexer.analizar_con_errores()