
class CSharpGenerator:

    def __init__(self):
        self.variables = set()
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

        self.emit("using System;")
        self.emit("using System.Collections.Generic;")
        self.emit()

        self.emit("class Program")
        self.emit("{")

        self.indent += 1

        self.emit("static void Main()")
        self.emit("{")

        self.indent += 1

        self.generate_statement(nodo)

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

        if not hasattr(self, metodo):

            raise Exception(
                f"CSharpGenerator no soporta: "
                f"{type(nodo).__name__}"
            )

        return getattr(self, metodo)(nodo)

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
                f"var {nodo.nombre} = {valor};"
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

        if nodo.nombre not in self.variables:

            self.variables.add(
                nodo.nombre
            )

            self.emit(
                f"{tipo} {nodo.nombre} = {valor};"
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
                f"{{ {clave_gen}, {valor_gen} }}"
            )

        return (
            "new Dictionary<string, object> "
            "{ "
            + ", ".join(pares)
            + " }"
        )

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

        llamada = self.generate_expr(nodo)

        self.emit(f"{llamada};")
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

            valor_tipo = type(nodo.valor).__name__

            if nodo.op == "no":

                if valor_tipo == "Identificador":
                    return f"{valor} == null"
                if "== 0" in valor:
                    return valor.replace(
                        "== 0",
                        "!= 0"
                    )

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

            return (
                "new List<object> "
                "{ "
                + elementos
                + " }"
            )

        
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

            # =====================================================
            # BUILTINS CORE
            # =====================================================

            if nodo.nombre == "tipo":
                return f"{args}.GetType().Name"

            if nodo.nombre == "agregar":

                lista = self.generate_expr(
                    nodo.argumentos[0]
                )

                valor = self.generate_expr(
                    nodo.argumentos[1]
                )

                return f"{lista}.Add({valor})"

            if nodo.nombre == "ordenar":
                return f"{args}.Sort()"

            if nodo.nombre == "eliminar":

                lista = self.generate_expr(
                    nodo.argumentos[0]
                )

                valor = self.generate_expr(
                    nodo.argumentos[1]
                )

                return f"{lista}.Remove({valor})"

            if nodo.nombre == "insertar":

                lista = self.generate_expr(
                    nodo.argumentos[0]
                )

                indice = self.generate_expr(
                    nodo.argumentos[1]
                )

                valor = self.generate_expr(
                    nodo.argumentos[2]
                )

                return (
                    f"{lista}.Insert("
                    f"{indice}, {valor})"
                )

            if nodo.nombre == "contiene":

                lista = self.generate_expr(
                    nodo.argumentos[0]
                )

                valor = self.generate_expr(
                    nodo.argumentos[1]
                )

                return f"{lista}.Contains({valor})"

            if nodo.nombre == "vacio":
                return f"{args}.Count == 0"

            if nodo.nombre == "limpiar":
                return f"{args}.Clear()"

            if nodo.nombre == "largo":
                return f"{args}.Count"

            if nodo.nombre == "mayus":
                return f"{args}.ToUpper()"

            if nodo.nombre == "minus":
                return f"{args}.ToLower()"

            if nodo.nombre == "convertir_texto":
                return f"{args}.ToString()"

            if nodo.nombre == "convertir_entero":
                return f"Convert.ToInt32({args})"

            if nodo.nombre == "convertir_decimal":
                return f"Convert.ToDouble({args})"

            if nodo.nombre == "convertir_booleano":
                return f"Convert.ToBoolean({args})"

            return f"{nodo.nombre}({args})"
        return "null"
