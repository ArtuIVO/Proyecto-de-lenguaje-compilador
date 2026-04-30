class Nodo:
    def __init__(self, linea=0):
        self.linea = linea


class Programa(Nodo):
    def __init__(self, sentencias):
        super().__init__()
        self.sentencias = sentencias


class Asignacion(Nodo):
    def __init__(self, nombre, valor, linea=0):
        super().__init__(linea)
        self.nombre = nombre
        self.valor = valor


class If(Nodo):
    def __init__(self, condicion, cuerpo, sino=None, linea=0):
        super().__init__(linea)
        self.condicion = condicion
        self.cuerpo = cuerpo
        self.sino = sino or []


class While(Nodo):
    def __init__(self, condicion, cuerpo, linea=0):
        super().__init__(linea)
        self.condicion = condicion
        self.cuerpo = cuerpo


class Para(Nodo):
    def __init__(self, variable, inicio, fin, cuerpo, linea=0):
        super().__init__(linea)
        self.variable = variable
        self.inicio = inicio
        self.fin = fin
        self.cuerpo = cuerpo


class BinOp(Nodo):
    def __init__(self, izquierda, op, derecha, linea=0):
        super().__init__(linea)
        self.izquierda = izquierda
        self.op = op
        self.derecha = derecha


class Numero(Nodo):
    def __init__(self, valor, linea=0):
        super().__init__(linea)
        self.valor = valor


class Cadena(Nodo):
    def __init__(self, valor, linea=0):
        super().__init__(linea)
        self.valor = valor


class Identificador(Nodo):
    def __init__(self, nombre, linea=0):
        super().__init__(linea)
        self.nombre = nombre


class Escribir(Nodo):
    def __init__(self, valor, linea=0):
        super().__init__(linea)
        self.valor = valor


class Funcion(Nodo):
    def __init__(self, nombre, parametros, cuerpo, linea=0):
        super().__init__(linea)
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo


class Retornar(Nodo):
    def __init__(self, valor, linea=0):
        super().__init__(linea)
        self.valor = valor


class Llamada(Nodo):
    def __init__(self, nombre, argumentos, linea=0):
        super().__init__(linea)
        self.nombre = nombre
        self.argumentos = argumentos


class Lista(Nodo):
    def __init__(self, elementos, linea=0):
        super().__init__(linea)
        self.elementos = elementos


class AccesoLista(Nodo):
    def __init__(self, nombre, indice, linea=0):
        super().__init__(linea)
        self.nombre = nombre
        self.indice = indice