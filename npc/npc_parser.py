from models.sintactico_model import Parser
from npc.npc_ast import (
    NPC,
    Hablar,
    Mover,
    Patrullar,
    Atacar,
    Vida,
    Animar,
    Esperar,
    Ruta
        
)


class NPCParser(Parser):

    def sentencia(self):

        tok = self.actual()

        if tok and tok.valor == "npc":
            return self.npc_stmt()

        if tok and tok.valor == "hablar":
            return self.hablar_stmt()

        if tok and tok.valor == "mover":
            return self.mover_stmt()

        if tok and tok.valor == "patrullar":
            return self.patrullar_stmt()

        if tok and tok.valor == "atacar":
            return self.atacar_stmt()
        
        if tok and tok.valor == "vida":
            return self.vida_stmt()

        if tok and tok.valor == "animar":
            return self.animar_stmt()

        if tok and tok.valor == "esperar":
            return self.esperar_stmt()

        if tok and tok.valor == "ruta":
            return self.ruta_stmt()

        return super().sentencia()

    # ---------------------------------

    def npc_stmt(self):

        self.match("PALABRA_RESERVADA", "npc")

        nombre = self.match("IDENTIFICADOR").valor

        self.match("SIMBOLO", ":")

        self.match("NEWLINE")

        cuerpo = self.bloque()

        return NPC(nombre, cuerpo)

    # ---------------------------------

    def hablar_stmt(self):

        self.match("PALABRA_RESERVADA", "hablar")

        self.match("SIMBOLO", "(")

        personaje = self.expresion()

        self.match("SIMBOLO", ",")

        texto = self.expresion()

        self.match("SIMBOLO", ")")

        return Hablar(personaje, texto)

    # ---------------------------------

    def mover_stmt(self):

        self.match("PALABRA_RESERVADA", "mover")

        self.match("SIMBOLO", "(")

        eje = self.expresion()

        self.match("SIMBOLO", ",")

        cantidad = self.expresion()

        self.match("SIMBOLO", ")")

        return Mover(eje, cantidad)

    # ---------------------------------

    def patrullar_stmt(self):

        self.match("PALABRA_RESERVADA", "patrullar")

        self.match("SIMBOLO", "(")
        self.match("SIMBOLO", ")")

        return Patrullar()

    # ---------------------------------

    def atacar_stmt(self):

        self.match("PALABRA_RESERVADA", "atacar")

        self.match("SIMBOLO", "(")

        objetivo = self.expresion()

        self.match("SIMBOLO", ")")

        return Atacar(objetivo)
    
    def vida_stmt(self):

        self.match("PALABRA_RESERVADA", "vida")
        self.match("SIMBOLO", "(")

        valor = self.expresion()

        self.match("SIMBOLO", ")")

        return Vida(valor)


    def animar_stmt(self):

        self.match("PALABRA_RESERVADA", "animar")
        self.match("SIMBOLO", "(")

        nombre = self.expresion()

        self.match("SIMBOLO", ")")

        return Animar(nombre)


    def esperar_stmt(self):

        self.match("PALABRA_RESERVADA", "esperar")
        self.match("SIMBOLO", "(")

        tiempo = self.expresion()

        self.match("SIMBOLO", ")")

        return Esperar(tiempo)


    def ruta_stmt(self):

        self.match("PALABRA_RESERVADA", "ruta")
        self.match("SIMBOLO", "(")

        puntos = self.expresion()

        self.match("SIMBOLO", ")")

        return Ruta(puntos)