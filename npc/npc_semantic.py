from models.semantico_model import AnalizadorSemantico


class NPCSemantic(AnalizadorSemantico):

    def __init__(self):
        super().__init__()
        self.npc_actual = None

    # --------------------------------

    def visitar_NPC(self, nodo):

        self.npc_actual = nodo.nombre
        self.salida.append(f"[NPC creado: {nodo.nombre}]")

        for ins in nodo.cuerpo:
            self.analizar(ins)

        self.npc_actual = None

    # --------------------------------

    def visitar_Hablar(self, nodo):

        personaje = self.analizar(nodo.personaje)
        texto = self.analizar(nodo.texto)

        self.salida.append(
            f"{personaje}: {texto}"
        )

    # --------------------------------

    def visitar_Mover(self, nodo):

        eje = self.analizar(nodo.eje)
        cantidad = self.analizar(nodo.cantidad)

        self.salida.append(
            f"{self.npc_actual} se mueve en {eje} {cantidad}"
        )

    # --------------------------------

    def visitar_Patrullar(self, nodo):

        self.salida.append(
            f"{self.npc_actual} inicia patrulla"
        )

    # --------------------------------

    def visitar_Atacar(self, nodo):

        objetivo = self.analizar(nodo.objetivo)

        self.salida.append(
            f"{self.npc_actual} ataca a {objetivo}"
        )
    def visitar_Vida(self, nodo):

        valor = self.analizar(nodo.valor)

        self.salida.append(
            f"{self.npc_actual} tiene vida {valor}"
        )


    def visitar_Animar(self, nodo):

        nombre = self.analizar(nodo.nombre)

        self.salida.append(
            f"{self.npc_actual} cambia animación a {nombre}"
        )


    def visitar_Esperar(self, nodo):

        tiempo = self.analizar(nodo.tiempo)

        self.salida.append(
            f"{self.npc_actual} espera {tiempo} segundos"
        )


    def visitar_Ruta(self, nodo):

        puntos = self.analizar(nodo.puntos)

        self.salida.append(
            f"{self.npc_actual} sigue ruta {puntos}"
        )