class RetornoFuncion(Exception):
    def __init__(self, valor):
        self.valor = valor


class AnalizadorSemantico:

    def __init__(self):
        self.variables = {}
        self.funciones = {}
        self.salida = []

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

    def visitar_Identificador(self, nodo):

        if nodo.nombre in self.variables:
            return self.variables[nodo.nombre]

        raise Exception(
            f"Variable no definida: {nodo.nombre}"
        )

    # ----------------------

    def visitar_Asignacion(self, nodo):

        valor = self.analizar(nodo.valor)
        self.variables[nodo.nombre] = valor

    # ----------------------

    def visitar_Escribir(self, nodo):

        valor = self.analizar(nodo.valor)
        self.salida.append(valor)

    # ----------------------

    def visitar_Funcion(self, nodo):

        self.funciones[nodo.nombre] = nodo

    # ----------------------

    def visitar_Llamada(self, nodo):
        # funciones nativas
        if nodo.nombre == "largo":
            if len(nodo.argumentos) != 1:
                raise Exception("largo() recibe 1 argumento")
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

        if nodo.nombre not in self.funciones:
            raise Exception(
                f"Función no definida: {nodo.nombre}"
            )

        funcion = self.funciones[nodo.nombre]

        if len(nodo.argumentos) != len(funcion.parametros):
            raise Exception(
                f"Cantidad incorrecta de parámetros en {nodo.nombre}"
            )

        respaldo = self.variables.copy()

        # scope local
        for i in range(len(funcion.parametros)):
            nombre = funcion.parametros[i]
            valor = self.analizar(nodo.argumentos[i])
            self.variables[nombre] = valor

        try:
            for ins in funcion.cuerpo:
                self.analizar(ins)

        except RetornoFuncion as r:
            self.variables = respaldo
            return r.valor

        self.variables = respaldo
        return None

    # ----------------------

    def visitar_Retornar(self, nodo):

        valor = self.analizar(nodo.valor)
        raise RetornoFuncion(valor)

    # ----------------------

    def visitar_If(self, nodo):

        if self.analizar(nodo.condicion):

            for ins in nodo.cuerpo:
                self.analizar(ins)

        else:

            for ins in nodo.sino:
                self.analizar(ins)

    # ----------------------

    def visitar_While(self, nodo):

        limite = 10000
        contador = 0

        while self.analizar(nodo.condicion):

            contador += 1

            if contador > limite:
                raise Exception(
                    "Bucle infinito detectado"
                )

            for ins in nodo.cuerpo:
                self.analizar(ins)

    # ----------------------

    def visitar_BinOp(self, nodo):

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
                raise Exception("División entre cero")

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

        raise Exception(
            f"Operador no soportado: {nodo.op}"
        )
    
    def visitar_Para(self, nodo):

        inicio = self.analizar(nodo.inicio)
        fin = self.analizar(nodo.fin)

        respaldo = self.variables.get(nodo.variable, None)
        existia = nodo.variable in self.variables

        for i in range(inicio, fin):
            self.variables[nodo.variable] = i

            for ins in nodo.cuerpo:
                self.analizar(ins)

        if existia:
            self.variables[nodo.variable] = respaldo
        else:
            del self.variables[nodo.variable]

    def visitar_Lista(self, nodo):
        return [self.analizar(x) for x in nodo.elementos]


    def visitar_AccesoLista(self, nodo):

        if nodo.nombre not in self.variables:
            raise Exception(f"Lista no definida: {nodo.nombre}")

        lista = self.variables[nodo.nombre]
        indice = self.analizar(nodo.indice)

        return lista[indice]
    
    def visitar_Cadena(self, nodo):
        return nodo.valor