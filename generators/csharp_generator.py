
class CSharpGenerator:

    def __init__(self):

        self.code = []
        self.indent = 0

    # =====================================================
    # HELPERS
    # =====================================================

    def emit(self, linea=""):

        self.code.append(
            "    " * self.indent + linea
        )

    def get_code(self):

        return "\n".join(self.code)

    # =====================================================
    # GENERATE
    # =====================================================

    def generate(self, nodo):

        # encabezado C#
        self.emit("using System;")
        self.emit()

        self.emit("class Program")
        self.emit("{")

        self.indent += 1

        self.emit("static void Main()")
        self.emit("{")

        self.indent += 1

        # generar programa
        metodo = f"generate_{type(nodo).__name__}"

        getattr(self, metodo)(nodo)

        self.indent -= 1

        self.emit("}")

        self.indent -= 1

        self.emit("}")

    # =====================================================
    # PROGRAMA
    # =====================================================

    def generate_Programa(self, nodo):

        for sentencia in nodo.sentencias:
            self.generate_statement(sentencia)

    # =====================================================
    # STATEMENTS
    # =====================================================

    def generate_statement(self, nodo):

        metodo = f"generate_{type(nodo).__name__}"

        return getattr(self, metodo)(nodo)

    # =====================================================
    # ASIGNACIÓN
    # =====================================================

    def generate_Asignacion(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        self.emit(
            f"var {nodo.nombre} = {valor};"
        )

    # =====================================================
    # DECLARACIÓN TIPADA
    # =====================================================

    def generate_DeclaracionTipada(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        tipos = {

            "entero": "int",

            "decimal": "double",

            "texto": "string",

            "booleano": "bool",

            "lista": "var"
        }

        tipo = tipos.get(
            nodo.tipo,
            "var"
        )

        self.emit(
            f"{tipo} {nodo.nombre} = {valor};"
        )

    # =====================================================
    # ESCRIBIR
    # =====================================================

    def generate_Escribir(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        self.emit(
            f"Console.WriteLine({valor});"
        )

    # =====================================================
    # IF
    # =====================================================

    def generate_If(self, nodo):

        condicion = self.generate_expr(
            nodo.condicion
        )

        self.emit(
            f"if ({condicion})"
        )

        self.emit("{")

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate_statement(ins)

        self.indent -= 1

        self.emit("}")

        if nodo.sino:

            self.emit("else")
            self.emit("{")

            self.indent += 1

            for ins in nodo.sino:
                self.generate_statement(ins)

            self.indent -= 1

            self.emit("}")

    # =====================================================
    # WHILE
    # =====================================================

    def generate_While(self, nodo):

        condicion = self.generate_expr(
            nodo.condicion
        )

        self.emit(
            f"while ({condicion})"
        )

        self.emit("{")

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate_statement(ins)

        self.indent -= 1

        self.emit("}")

    # =====================================================
    # ROMPER Y CONTINUAR
    # =====================================================
    def generate_Romper(self, nodo):

        self.emit("break;")

    def generate_Continuar(self, nodo):

        self.emit("continue;")

    # =====================================================
    # FOR
    # =====================================================

    def generate_Para(self, nodo):

        inicio = self.generate_expr(
            nodo.inicio
        )

        fin = self.generate_expr(
            nodo.fin
        )

        self.emit(
            f"for (int {nodo.variable} = {inicio}; "
            f"{nodo.variable} < {fin}; "
            f"{nodo.variable}++)"
        )

        self.emit("{")

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate_statement(ins)

        self.indent -= 1

        self.emit("}")

    # =====================================================
    # RETORNO
    # =====================================================

    def generate_Retornar(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        self.emit(
            f"return {valor};"
        )

    # =====================================================
    # FUNCIONES
    # =====================================================

    def generate_Funcion(self, nodo):

        params = ", ".join([
            f"dynamic {p}"
            for p in nodo.parametros
        ])

        self.emit(
            f"static dynamic {nodo.nombre}({params})"
        )

        self.emit("{")

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate_statement(ins)

        self.indent -= 1

        self.emit("}")

    # =====================================================
    # LLAMADAS
    # =====================================================

    def generate_Llamada(self, nodo):

        args = ", ".join([
            self.generate_expr(a)
            for a in nodo.argumentos
        ])

        self.emit(
            f"{nodo.nombre}({args});"
        )

    # =====================================================
    # EXPRESIONES
    # =====================================================

    def generate_expr(self, nodo):

        tipo = type(nodo).__name__

        if tipo == "Numero":
            return str(nodo.valor)
        
        if tipo == "Booleano":
            return "true" if nodo.valor else "false"
        
        if tipo == "Nulo":
            return "null"
        
        if tipo == "LogicalOp":

            izq = self.generate_expr(
                nodo.izquierda
            )

            der = self.generate_expr(
                nodo.derecha
            )

            operadores = {

                "y": "&&",

                "o": "||"
            }

            op = operadores.get(
                nodo.op,
                nodo.op
            )

            return f"{izq} {op} {der}"


        if tipo == "UnaryOp":

            valor = self.generate_expr(
                nodo.valor
            )

            if nodo.op == "no":

                return f"!{valor}"

            return f"{nodo.op}{valor}"



        if tipo == "Cadena":
            return f'"{nodo.valor}"'

        if tipo == "Identificador":
            return nodo.nombre

        if tipo == "Lista":

            elementos = ", ".join([
                self.generate_expr(x)
                for x in nodo.elementos
            ])

            return f"new[] {{ {elementos} }}"

        if tipo == "AccesoLista":

            indice = self.generate_expr(
                nodo.indice
            )

            return f"{nodo.nombre}[{indice}]"

        if tipo == "BinOp":

            izq = self.generate_expr(
                nodo.izquierda
            )

            der = self.generate_expr(
                nodo.derecha
            )

            return f"{izq} {nodo.op} {der}"

        if tipo == "Llamada":

            args = ", ".join([
                self.generate_expr(a)
                for a in nodo.argumentos
            ])

            if nodo.nombre == "largo":
                return f"{args}.Length"

            if nodo.nombre == "mayus":
                return f"{args}.ToUpper()"

            if nodo.nombre == "minus":
                return f"{args}.ToLower()"

            return f"{nodo.nombre}({args})"

        return "null"
