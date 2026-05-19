class Builtins:

    # =====================================================
    # BUILTINS BASE
    # =====================================================

    @staticmethod
    def largo(valor):

        return len(valor)

    @staticmethod
    def mayus(valor):

        return str(valor).upper()

    @staticmethod
    def minus(valor):

        return str(valor).lower()

    @staticmethod
    def tipo(valor):

        return type(valor).__name__

    # =====================================================
    # BUILTINS MODERNOS
    # =====================================================

    @staticmethod
    def agregar(lista, valor):
        
        lista.append(valor)

        return lista

    @staticmethod
    def ordenar(lista):

        lista.sort()

        return lista

    # =====================================================
    # BUILTINS CORE
    # =====================================================

    @staticmethod
    def eliminar(lista, valor):

        lista.remove(valor)

        return lista

    @staticmethod
    def insertar(lista, indice, valor):

        lista.insert(indice, valor)

        return lista

    @staticmethod
    def contiene(lista, valor):

        return valor in lista

    @staticmethod
    def vacio(valor):

        return len(valor) == 0

    @staticmethod
    def limpiar(lista):

        lista.clear()

        return lista

    @staticmethod
    def convertir_texto(valor):

        return str(valor)

    @staticmethod
    def convertir_entero(valor):

        return int(valor)

    @staticmethod
    def convertir_decimal(valor):

        return float(valor)

    @staticmethod
    def convertir_booleano(valor):

        return bool(valor)

    # =====================================================
    # REGISTRO OFICIAL
    # =====================================================

    FUNCTIONS = {

        # =================================================
        # BUILTINS BASE
        # =================================================

        "largo": largo.__func__,

        "mayus": mayus.__func__,

        "minus": minus.__func__,

        "tipo": tipo.__func__,

        # =================================================
        # BUILTINS MODERNOS
        # =================================================

        "agregar": agregar.__func__,

        "ordenar": ordenar.__func__,

        # =================================================
        # BUILTINS CORE
        # =================================================

        "eliminar": eliminar.__func__,

        "insertar": insertar.__func__,

        "contiene": contiene.__func__,

        "vacio": vacio.__func__,

        "limpiar": limpiar.__func__,

        "convertir_texto": convertir_texto.__func__,

        "convertir_entero": convertir_entero.__func__,

        "convertir_decimal": convertir_decimal.__func__,

        "convertir_booleano": convertir_booleano.__func__,
    }