
class PythonGenerator:

    def __init__(self):

        self.code = []
        self.indent = 0

    # =====================================================
    # GENERAR
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
    # HELPERS
    # =====================================================

    def emit(self, linea):

        self.code.append(
            "    " * self.indent + linea
        )

    def get_code(self):

        return "\n".join(self.code)

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

        valor = self.generate_expr(nodo.valor)

        self.emit(
            f"{nodo.nombre} = {valor}"
        )

    # =====================================================
    # DECLARACIÓN TIPADA
    # =====================================================
    
    def generate_DeclaracionTipada(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        tipos_python = {

            "entero": "int",

            "decimal": "float",

            "texto": "str",

            "booleano": "bool",

            "lista": "list",
        }

        tipo = tipos_python.get(
            nodo.tipo,
            "Any"
        )

        self.emit(
            f"{nodo.nombre}: {tipo} = {valor}"
        )


    # =====================================================
    # ESCRIBIR
    # =====================================================

    def generate_Escribir(self, nodo):

        valor = self.generate_expr(nodo.valor)

        self.emit(
            f"print({valor})"
        )

    # =====================================================
    # IF
    # =====================================================

    def generate_If(self, nodo):

        condicion = self.generate_expr(
            nodo.condicion
        )

        self.emit(
            f"if {condicion}:"
        )

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate(ins)

        self.indent -= 1

        if nodo.sino:

            self.emit("else:")

            self.indent += 1

            for ins in nodo.sino:
                self.generate(ins)

            self.indent -= 1

    # =====================================================
    # WHILE
    # =====================================================

    def generate_While(self, nodo):

        condicion = self.generate_expr(
            nodo.condicion
        )

        self.emit(
            f"while {condicion}:"
        )

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate(ins)

        self.indent -= 1

    # =====================================================
    # FUNCIÓN
    # =====================================================

    def generate_Funcion(self, nodo):

        params = ", ".join(
            nodo.parametros
        )

        self.emit(
            f"def {nodo.nombre}({params}):"
        )

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate(ins)

        self.indent -= 1

    # =====================================================
    # RETORNO
    # =====================================================

    def generate_Retornar(self, nodo):

        valor = self.generate_expr(
            nodo.valor
        )

        self.emit(
            f"return {valor}"
        )
    # =====================================================
    # ROMPER Y CONTINUAR
    # =====================================================
    def generate_Romper(self, nodo):

        self.emit(
            f"break"
        )
    def generate_Continuar(self, nodo):

        self.emit(
            f"continue"
        )

    # =====================================================
    # LLAMADAS
    # =====================================================

    def generate_Llamada(self, nodo):

        args = ", ".join([
            self.generate_expr(a)
            for a in nodo.argumentos
        ])

        # builtins
        if nodo.nombre == "escribir":
            self.emit(f"print({args})")
            return

        self.emit(
            f"{nodo.nombre}({args})"
        )

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
            f"for {nodo.variable} in range({inicio}, {fin}):"
        )

        self.indent += 1

        for ins in nodo.cuerpo:
            self.generate(ins)

        self.indent -= 1

    # =====================================================
    # EXPRESIONES
    # =====================================================

    def generate_expr(self, nodo):

        tipo = type(nodo).__name__

        if tipo == "Numero":
            return str(nodo.valor)
        
        if tipo == "Booleano":
            return "True" if nodo.valor else "False"
        
        if tipo == "Nulo":
            return "None"
        
        if tipo == "Diccionario":

            return self.generate_Diccionario(
                nodo
            )

        if tipo == "Acceso":

            return self.generate_Acceso(
                nodo
            )



        if tipo == "LogicalOp":

            izq = self.generate_expr(
                nodo.izquierda
            )

            der = self.generate_expr(
                nodo.derecha
            )

            operadores = {

                "y": "and",

                "o": "or"
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

                return f"not {valor}"

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

            # traducción builtins
            traducciones = {
                "largo": "len",
                "mayus": "str.upper",
                "minus": "str.lower",
                "tipo": "type",
                "agregar": "append",
                "ordenar": "sorted", 
            }

            nombre = traducciones.get(
                nodo.nombre,
                nodo.nombre
            )

            return f"{nombre}({args})"

        return "None"
    
    # ======================
    # DICCIONARIO
    # ======================
   
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
    
    # ======================
    # ACCESO
    # ======================

    def generate_Acceso(self, nodo):

        objeto = self.generate_expr(
            nodo.objeto
        )

        indice = self.generate_expr(
            nodo.indice
        )

        return f"{objeto}[{indice}]"

