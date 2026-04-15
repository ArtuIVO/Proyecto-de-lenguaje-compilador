class AnalizadorSemantico:
    def __init__(self):
        self.variables = {}
        self.salida = []

    def analizar(self, nodo):
        metodo = f"visitar_{type(nodo).__name__}"
        return getattr(self, metodo)(nodo)
    
    def visitar_Escribir(self, nodo):
        valor = self.analizar(nodo.valor)
        self.salida.append(valor)

    def visitar_Programa(self, nodo):
        for s in nodo.sentencias:
            self.analizar(s)

    def visitar_Asignacion(self, nodo):
        valor = self.analizar(nodo.valor)
        self.variables[nodo.nombre] = valor

    def visitar_Numero(self, nodo):
        return int(nodo.valor)

    def visitar_Identificador(self, nodo):
        if nodo.nombre not in self.variables:
            raise Exception(f"Variable no definida: {nodo.nombre}")
        return self.variables[nodo.nombre]

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
            return izq / der

        if nodo.op == "==":
            return izq == der
        if nodo.op == "<":
            return izq < der
        if nodo.op == ">":
            return izq > der

        raise Exception(f"Operador no válido: {nodo.op}")