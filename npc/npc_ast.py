class NPC:
    def __init__(self, nombre, cuerpo):
        self.nombre = nombre
        self.cuerpo = cuerpo


class Hablar:
    def __init__(self, personaje, texto):
        self.personaje = personaje
        self.texto = texto
    
class Mover:
    def __init__(self, eje, cantidad):
        self.eje = eje
        self.cantidad = cantidad


class Patrullar:
    def __init__(self):
        pass


class Atacar:
    def __init__(self, objetivo):
        self.objetivo = objetivo

class Vida:
    def __init__(self, valor):
        self.valor = valor


class Animar:
    def __init__(self, nombre):
        self.nombre = nombre


class Esperar:
    def __init__(self, tiempo):
        self.tiempo = tiempo


class Ruta:
    def __init__(self, puntos):
        self.puntos = puntos