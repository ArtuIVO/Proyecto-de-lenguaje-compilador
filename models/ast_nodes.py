class Nodo:
    pass


class Programa(Nodo):
    def __init__(self, sentencias):
        self.sentencias = sentencias


class Asignacion(Nodo):
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor


class If(Nodo):
    def __init__(self, condicion, cuerpo):
        self.condicion = condicion
        self.cuerpo = cuerpo


class BinOp(Nodo):
    def __init__(self, izquierda, op, derecha):
        self.izquierda = izquierda
        self.op = op
        self.derecha = derecha
        
class Variable:
    def __init__(self, nombre):
        self.nombre = nombre

class Numero(Nodo):
    def __init__(self, valor):
        self.valor = valor


class Identificador(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre
    
class Escribir(Nodo):
    def __init__(self, valor):
        self.valor = valor