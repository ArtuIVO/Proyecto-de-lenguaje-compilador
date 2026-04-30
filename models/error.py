class CompilerError(Exception):
    def __init__(self, mensaje, linea):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.linea = linea