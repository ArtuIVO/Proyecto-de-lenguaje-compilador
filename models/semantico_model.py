from models.error import CompilerError


class Simbolo:
    def __init__(self, nombre, tipo, valor, linea, scope="global"):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.scope = scope


class RetornoFuncion(Exception):
    def __init__(self, valor):
        self.valor = valor


class AnalizadorSemantico:

    def __init__(self):
        self.tabla_simbolos = {}
        self.funciones = {}
        self.salida = []
        self.traza = []

    # ----------------------

    def analizar(self, nodo):
        metodo = f"visitar_{type(nodo).__name__}"
        return getattr(self, metodo)(nodo)

    # ----------------------

    def visitar_Programa(self, nodo):
        for sentencia in nodo.sentencias:
            self.analizar(sentencia)

    # ----------------------

    def visitar_Numero(self, nodo):
        return int(nodo.valor)

    def visitar_Cadena(self, nodo):
        return nodo.valor

    # ----------------------

    def visitar_Identificador(self, nodo):

        if nodo.nombre in self.tabla_simbolos:
            valor = self.tabla_simbolos[nodo.nombre].valor

            self.traza.append({
                "linea": nodo.linea,
                "accion": f"Uso variable '{nodo.nombre}'",
                "valor": valor,
                "valido": True
            })

            return valor

        self.traza.append({
            "linea": nodo.linea,
            "accion": f"Variable no definida '{nodo.nombre}'",
            "valido": False
        })

        raise CompilerError(
            f"Variable no definida: {nodo.nombre}",
            nodo.linea
        )

    # ----------------------

    def visitar_Asignacion(self, nodo):

        valor = self.analizar(nodo.valor)
        tipo = type(valor).__name__

        # 🔥 si ya existe la variable → validar tipo
        if nodo.nombre in self.tabla_simbolos:
            tipo_anterior = self.tabla_simbolos[nodo.nombre].tipo

            if tipo != tipo_anterior:
                raise CompilerError(
                    f"Error de tipo: '{nodo.nombre}' era {tipo_anterior} y ahora {tipo}",
                    nodo.linea
                )

        self.tabla_simbolos[nodo.nombre] = Simbolo(
            nodo.nombre,
            tipo,
            valor,
            nodo.linea
        )

        self.traza.append({
            "linea": nodo.linea,
            "accion": f"Asignación '{nodo.nombre}' ({tipo})",
            "valor": valor,
            "valido": True
        })
    # ----------------------

    def visitar_Escribir(self, nodo):
        valor = self.analizar(nodo.valor)

        self.traza.append({
            "linea": nodo.linea,
            "accion": "Salida",
            "valor": valor,
            "valido": True
        })

        self.salida.append(valor)

    # ----------------------

    def visitar_Funcion(self, nodo):
        self.funciones[nodo.nombre] = nodo

    # ----------------------

    def visitar_Llamada(self, nodo):

        # -------- BUILTINS --------

        if nodo.nombre == "largo":
            valor = self.analizar(nodo.argumentos[0])
            return len(valor)

        if nodo.nombre == "mayus":
            valor = self.analizar(nodo.argumentos[0])
            return str(valor).upper()

        if nodo.nombre == "minus":
            valor = self.analizar(nodo.argumentos[0])
            return str(valor).lower()

        if nodo.nombre == "tipo":
            valor = self.analizar(nodo.argumentos[0])
            return type(valor).__name__

        # -------- FUNCIONES USUARIO --------

        if nodo.nombre not in self.funciones:
            raise CompilerError(
                f"Función no definida: {nodo.nombre}",
                nodo.linea
            )

        funcion = self.funciones[nodo.nombre]

        respaldo = self.tabla_simbolos.copy()

        for i in range(len(funcion.parametros)):
            nombre = funcion.parametros[i]
            valor = self.analizar(nodo.argumentos[i])

            self.tabla_simbolos[nombre] = Simbolo(
                nombre,
                type(valor).__name__,
                valor,
                nodo.linea,
                "local"
            )

        try:
            for ins in funcion.cuerpo:
                self.analizar(ins)

        except RetornoFuncion as r:
            self.tabla_simbolos = respaldo
            return r.valor

        self.tabla_simbolos = respaldo
        return None

    # ----------------------

    def visitar_Retornar(self, nodo):
        valor = self.analizar(nodo.valor)
        raise RetornoFuncion(valor)

    # ----------------------
    # 🔥 IF

    def visitar_If(self, nodo):

        condicion = self.analizar(nodo.condicion)

        self.traza.append({
            "linea": nodo.linea,
            "accion": "Evaluación IF",
            "valor": condicion,
            "valido": True
        })

        if condicion:
            for ins in nodo.cuerpo:
                self.analizar(ins)
        else:
            for ins in nodo.sino:
                self.analizar(ins)

    # ----------------------
    # 🔥 WHILE

    def visitar_While(self, nodo):

        limite = 10000
        contador = 0

        while self.analizar(nodo.condicion):

            contador += 1

            if contador > limite:
                raise CompilerError(
                    "Bucle infinito detectado",
                    nodo.linea
                )

            self.traza.append({
                "linea": nodo.linea,
                "accion": "Iteración WHILE",
                "valido": True
            })

            for ins in nodo.cuerpo:
                self.analizar(ins)

    # ----------------------
    # 🔥 FOR

    def visitar_Para(self, nodo):

        inicio = self.analizar(nodo.inicio)
        fin = self.analizar(nodo.fin)

        for i in range(inicio, fin):

            self.tabla_simbolos[nodo.variable] = Simbolo(
                nodo.variable,
                "int",
                i,
                nodo.linea
            )

            self.traza.append({
                "linea": nodo.linea,
                "accion": f"For {nodo.variable} = {i}",
                "valido": True
            })

            for ins in nodo.cuerpo:
                self.analizar(ins)

    # ----------------------
    # 🔥 LISTAS

    def visitar_Lista(self, nodo):
        return [self.analizar(x) for x in nodo.elementos]

    def visitar_AccesoLista(self, nodo):

        if nodo.nombre not in self.tabla_simbolos:
            raise CompilerError(
                f"Variable no definida: {nodo.nombre}",
                nodo.linea
            )

        lista = self.tabla_simbolos[nodo.nombre].valor
        indice = self.analizar(nodo.indice)

        try:
            return lista[indice]
        except Exception:
            raise CompilerError(
                "Índice fuera de rango",
                nodo.linea
            )

    # ----------------------
    # 🔥 OPERACIONES

    def visitar_BinOp(self, nodo):
        izq = self.analizar(nodo.izquierda)
        der = self.analizar(nodo.derecha)

        if type(izq) != type(der):
            raise CompilerError(
                f"Tipos incompatibles: {type(izq).__name__} y {type(der).__name__}",
                nodo.linea
            )

        izq = self.analizar(nodo.izquierda)
        der = self.analizar(nodo.derecha)

        if nodo.op == "+":
            return izq + der
        if nodo.op == "-":
            return izq - der
        if nodo.op == "*":
            return izq * der
        if nodo.op == "/":
            if der == 0:
                raise CompilerError("División entre cero", nodo.linea)
            return izq / der

        if nodo.op == "==":
            return izq == der
        if nodo.op == "!=":
            return izq != der
        if nodo.op == "<":
            return izq < der
        if nodo.op == ">":
            return izq > der
        if nodo.op == "<=":
            return izq <= der
        if nodo.op == ">=":
            return izq >= der

        raise CompilerError(
            f"Operador no soportado: {nodo.op}",
            nodo.linea
        )