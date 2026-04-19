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
    def __init__(self, condicion, cuerpo, sino=None):
        self.condicion = condicion
        self.cuerpo = cuerpo
        self.sino = sino or []


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

class While(Nodo):
    def __init__(self, condicion, cuerpo):
        self.condicion = condicion
        self.cuerpo = cuerpo

class Funcion(Nodo):
    def __init__(self, nombre, parametros, cuerpo):
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo


class Retornar(Nodo):
    def __init__(self, valor):
        self.valor = valor


class Llamada(Nodo):
    def __init__(self, nombre, argumentos):
        self.nombre = nombre
        self.argumentos = argumentos

class Para(Nodo):
    def __init__(self, variable, inicio, fin, cuerpo):
        self.variable = variable
        self.inicio = inicio
        self.fin = fin
        self.cuerpo = cuerpo

class Lista(Nodo):
    def __init__(self, elementos):
        self.elementos = elementos


class AccesoLista(Nodo):
    def __init__(self, nombre, indice):
        self.nombre = nombre
        self.indice = indice

class Cadena(Nodo):
    def __init__(self, valor):
        self.valor = valor