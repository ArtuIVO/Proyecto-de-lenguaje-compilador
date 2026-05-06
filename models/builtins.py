class Builtins:

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
    # REGISTRO OFICIAL
    # =====================================================

    FUNCTIONS = {
        "largo": largo.__func__,
        "mayus": mayus.__func__,
        "minus": minus.__func__,
        "tipo": tipo.__func__,
    }
