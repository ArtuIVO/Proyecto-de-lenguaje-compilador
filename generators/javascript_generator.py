
class JavaScriptGenerator:

    def __init__(self):
        self.variables = set()
        self.code = []
        self.indent = 0

    # =====================================================
    # HELPERS
    # =====================================================

    def emit(self, linea):

        self.code.append(
            "    " * self.indent + linea
        )

    def get_code(self):

        return "\n".join(self.code)

    # =====================================================
    # GENERATE
    # =====================================================

    def generate(self, nodo):

        metodo = f"generate_{type(nodo).__name__}"

        if not hasattr(self, metodo):
            raise Exception(
                f"Generator no soporta: "
                f"{type(nodo).__name__}"
            )

        return getattr(self, metodo)(nodo)

    # =====================================================
    # PROGRAMA
    # =====================================================

    def generate_Programa(self, nodo):

        for sentencia in nodo.sentencias:
            self.generate(sentencia)

    # =====================================================
    # ASIGNACIÓN
    # =====================================================

    
    def generate_Asignacion(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        if nodo.nombre not in self.variables:

            self.variables.add(
                nodo.nombre
            )

            self.emit(
                f"let {nodo.nombre} = {valor};"
            )

        else:

            self.emit(
                f"{nodo.nombre} = {valor};"
            )



    # =====================================================
    # DECLARACIÓN TIPADA
    # =====================================================

    
    def generate_DeclaracionTipada(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        if nodo.nombre not in self.variables:

            self.variables.add(
                nodo.nombre
            )

            self.emit(
                f"let {nodo.nombre} = {valor};"
            )

        else:

            self.emit(
                f"{nodo.nombre} = {valor};"
            )


    # =====================================================
    # ESCRIBIR
    # =====================================================

    def generate_Escribir(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        self.emit(
            f"console.log({valor});"
        )

    # =====================================================
    # IF
    # =====================================================

    def generate_If(self, nodo):

        condicion = self.generate_expr(
            nodo.condicion
        )

        self.emit(
            f"if ({condicion}) {{"
        )

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate(ins)

        self.indent -= 1

        self.emit("}")

        if nodo.sino:

            self.emit("else {")

            self.indent += 1

            for ins in nodo.sino:
                self.generate(ins)

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
            f"while ({condicion}) {{"
        )

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate(ins)

        self.indent -= 1

        self.emit("}")

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
            f"for (let {nodo.variable} = {inicio}; "
            f"{nodo.variable} < {fin}; "
            f"{nodo.variable}++) {{"
        )

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate(ins)

        self.indent -= 1

        self.emit("}")

    # =====================================================
    # ROMPER Y CONTINUAR
    # =====================================================
    def generate_Romper(self, nodo):

        self.emit(
            f"break;"
        )
    def generate_Continuar(self, nodo):

        self.emit(
            f"continue;"
        )

    # =====================================================
    # FUNCIÓN
    # =====================================================

    def generate_Funcion(self, nodo):

        params = ", ".join(
            nodo.parametros
        )

        self.emit(
            f"function {nodo.nombre}({params}) {{"
        )

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate(ins)

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
    # DICCIONARIO
    # =====================================================
    def generate_Diccionario(self, nodo):

        pares = []

        for clave, valor in nodo.pares:

            clave_gen = self.generate_expr(
                clave
            )

            valor_gen = self.generate_expr(
                valor
            )

            pares.append(
                f"{clave_gen}: {valor_gen}"
            )

        return "{ " + ", ".join(pares) + " }"

    # =====================================================
    # ACCESO
    # =====================================================
    def generate_Acceso(self, nodo):

        objeto = self.generate_expr(
            nodo.objeto
        )

        indice = self.generate_expr(
            nodo.indice
        )

        return f"{objeto}[{indice}]"



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
            return repr(nodo.valor)

        if tipo == "Identificador":
            return nodo.nombre

        if tipo == "Lista":

            elementos = ", ".join([
                self.generate_expr(x)
                for x in nodo.elementos
            ])

            return f"[{elementos}]"


        if tipo == "Diccionario":

            return self.generate_Diccionario(
                nodo
            )

        if tipo == "Acceso":

            return self.generate_Acceso(
                nodo
            )


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

        if nodo.nombre == "tipo":
            return f"typeof({args})"

        if nodo.nombre == "agregar":

            lista = self.generate_expr(
                nodo.argumentos[0]
            )

            valor = self.generate_expr(
                nodo.argumentos[1]
            )

            return f"{lista}.push({valor})"

        if nodo.nombre == "largo":
            return f"{args}.length"

        if nodo.nombre == "mayus":
            return f"{args}.toUpperCase()"

        if nodo.nombre == "minus":
            return f"{args}.toLowerCase()"

        if nodo.nombre == "ordenar":
            return f"{args}.sort()"

        return f"{nodo.nombre}({args})"

