from models.error import CompilerError
from models.builtins import Builtins

TIPOS_EDULANG = {

    "entero": int,

    "decimal": float,

    "texto": str,

    "booleano": bool,

    "lista": list,
}



class Simbolo:
    def __init__(self, nombre, tipo, valor, linea, scope="global"):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.scope = scope


class RetornoFuncion(Exception):
    def __init__(self, valor):
        self.valor = valor

class RomperLoop(Exception):
    pass


class ContinuarLoop(Exception):
    pass


class AnalizadorSemantico:

    def __init__(self):
        self.scopes = [{}]
        self.funciones = {}
        self.salida = []
        self.traza = []

    # ----------------------

    def analizar(self, nodo):
        metodo = f"visitar_{type(nodo).__name__}"
        return getattr(self, metodo)(nodo)

    # ----------------------

    def visitar_Programa(self, nodo):
        for sentencia in nodo.sentencias:
            self.analizar(sentencia)

    # ----------------------

    def visitar_Numero(self, nodo):
        return int(nodo.valor)
    
    def visitar_Booleano(self, nodo):
        return nodo.valor
    
    def visitar_Cadena(self, nodo):
        return nodo.valor

    # ----------------------

    def visitar_Identificador(self, nodo):

        for scope in reversed(self.scopes):
            if nodo.nombre in scope:
                valor = scope[nodo.nombre].valor

                self.traza.append({
                    "linea": nodo.linea,
                    "accion": f"Uso variable '{nodo.nombre}'",
                    "valor": valor,
                    "valido": True
                })

                return valor

        raise CompilerError(
            f"Variable no definida: {nodo.nombre}",
            nodo.linea
        )
    # ----------------------

    def visitar_Asignacion(self, nodo):

        valor = self.analizar(nodo.valor)
        tipo = type(valor).__name__

        self.scopes[-1][nodo.nombre] = Simbolo(
            nodo.nombre,
            tipo,
            valor,
            nodo.linea
        )

        self.traza.append({
            "linea": nodo.linea,
            "accion": f"Asignación '{nodo.nombre}'",
            "valor": valor,
            "valido": True
        })
    # ----------------------

    def visitar_DeclaracionTipada(self, nodo):

        valor = self.analizar(nodo.valor)

        tipo_python = TIPOS_EDULANG.get(
            nodo.tipo
        )

        if tipo_python is None:

            raise CompilerError(
                f"Tipo desconocido: {nodo.tipo}",
                nodo.linea
            )

        # ============================================
        # VALIDACIÓN DE TIPO
        # ============================================

        if not isinstance(valor, tipo_python):

            raise CompilerError(
                (
                    f"Se esperaba tipo "
                    f"'{nodo.tipo}' "
                    f"pero se recibió "
                    f"'{type(valor).__name__}'"
                ),
                nodo.linea
            )

        # ============================================
        # GUARDAR VARIABLE
        # ============================================

        self.scopes[-1][nodo.nombre] = Simbolo(
            nodo.nombre,
            nodo.tipo,
            valor,
            nodo.linea
        )

        self.traza.append({

            "linea": nodo.linea,

            "accion": (
                f"Declaración tipada "
                f"'{nodo.nombre}'"
            ),

            "valor": valor,

            "valido": True
        })



    def visitar_Escribir(self, nodo):
        valor = self.analizar(nodo.valor)

        self.traza.append({
            "linea": nodo.linea,
            "accion": "Salida",
            "valor": valor,
            "valido": True
        })

        self.salida.append(valor)

    # ----------------------

    def visitar_Funcion(self, nodo):
        self.funciones[nodo.nombre] = nodo

    # ----------------------

    
    def visitar_Llamada(self, nodo):

        # =====================================================
        # BUILTINS OFICIALES
        # =====================================================

        if nodo.nombre in Builtins.FUNCTIONS:

            argumentos = [
                self.analizar(arg)
                for arg in nodo.argumentos
            ]

            try:

                resultado = Builtins.FUNCTIONS[
                    nodo.nombre
                ](*argumentos)

                self.traza.append({
                    "linea": nodo.linea,
                    "accion": f"Builtin '{nodo.nombre}'",
                    "valor": resultado,
                    "valido": True
                })

                return resultado

            except Exception as e:

                raise CompilerError(
                    f"Error en builtin '{nodo.nombre}': {str(e)}",
                    nodo.linea
                )

        # =====================================================
        # FUNCIONES DEL USUARIO
        # =====================================================

        if nodo.nombre not in self.funciones:

            raise CompilerError(
                f"Función no definida: {nodo.nombre}",
                nodo.linea
            )

        funcion = self.funciones[nodo.nombre]

        # nuevo scope
        self.scopes.append({})

        # parámetros
        for i in range(len(funcion.parametros)):

            nombre = funcion.parametros[i]

            valor = self.analizar(
                nodo.argumentos[i]
            )

            self.scopes[-1][nombre] = Simbolo(
                nombre,
                type(valor).__name__,
                valor,
                nodo.linea,
                "local"
            )

        try:

            for ins in funcion.cuerpo:
                self.analizar(ins)

        except RetornoFuncion as r:

            self.scopes.pop()

            return r.valor

        self.scopes.pop()

        return None



    def visitar_Retornar(self, nodo):
        valor = self.analizar(nodo.valor)
        raise RetornoFuncion(valor)
    

    def visitar_Romper(self, nodo):

        raise RomperLoop()


    def visitar_Continuar(self, nodo):

        raise ContinuarLoop()


    def visitar_Nulo(self, nodo):

        return None



    # ----------------------
    # 🔥 IF

    def visitar_If(self, nodo):

        condicion = self.analizar(nodo.condicion)

        self.traza.append({
            "linea": nodo.linea,
            "accion": "Evaluación IF",
            "valor": condicion,
            "valido": True
        })

        if condicion:
            for ins in nodo.cuerpo:
                self.analizar(ins)
        else:
            for ins in nodo.sino:
                self.analizar(ins)

    # ----------------------
    # 🔥 WHILE

    def visitar_While(self, nodo):

        limite = 100000
        contador = 0

   
        while self.analizar(nodo.condicion):

            contador += 1

            if contador > limite:

                raise CompilerError(
                    "Bucle infinito detectado",
                    nodo.linea
                )

            try:

                for ins in nodo.cuerpo:

                    self.analizar(ins)

            except ContinuarLoop:

                continue

            except RomperLoop:

                break


    # ----------------------
    # 🔥 FOR

    def visitar_Para(self, nodo):

        inicio = self.analizar(nodo.inicio)
        fin = self.analizar(nodo.fin)

        for i in range(inicio, fin):

            self.scopes[-1][
                nodo.variable
            ] = Simbolo(
                nodo.variable,
                "entero",
                i,
                nodo.linea
            )

            try:

                for ins in nodo.cuerpo:

                    self.analizar(ins)

            except ContinuarLoop:

                continue

            except RomperLoop:

                break
   

    # ----------------------
    # 🔥 LISTAS

    def visitar_Lista(self, nodo):
        return [self.analizar(x) for x in nodo.elementos]

    def visitar_AccesoLista(self, nodo):

        for scope in reversed(self.scopes):
            if nodo.nombre in scope:
                lista = scope[nodo.nombre].valor
                indice = self.analizar(nodo.indice)

                try:
                    return lista[indice]
                except Exception:
                    raise CompilerError(
                        "Índice fuera de rango",
                        nodo.linea
                    )

        raise CompilerError(
            f"Variable no definida: {nodo.nombre}",
            nodo.linea
        )
    # ----------------------
    # 🔥 OPERACIONES

    def visitar_BinOp(self, nodo):
        izq = self.analizar(nodo.izquierda)
        der = self.analizar(nodo.derecha)

        if type(izq) != type(der):
            raise CompilerError(
                f"Tipos incompatibles: {type(izq).__name__} y {type(der).__name__}",
                nodo.linea
            )

        izq = self.analizar(nodo.izquierda)
        der = self.analizar(nodo.derecha)

        if nodo.op == "+":
            return izq + der
        if nodo.op == "-":
            return izq - der
        if nodo.op == "*":
            return izq * der
        if nodo.op == "/":
            if der == 0:
                raise CompilerError("División entre cero", nodo.linea)
            return izq / der

        if nodo.op == "==":
            return izq == der
        if nodo.op == "!=":
            return izq != der
        if nodo.op == "<":
            return izq < der
        if nodo.op == ">":
            return izq > der
        if nodo.op == "<=":
            return izq <= der
        if nodo.op == ">=":
            return izq >= der

        raise CompilerError(
            f"Operador no soportado: {nodo.op}",
            nodo.linea
        )
    
    def visitar_UnaryOp(self, nodo):
        valor = self.analizar(nodo.valor)

        if nodo.op == "+":
            return +valor
        if nodo.op == "-":
            return -valor
        if nodo.op == "no":
            return not valor

        raise CompilerError(
            f"Operador unario no soportado: {nodo.op}",
            nodo.linea
        )
    
    def visitar_LogicalOp(self, nodo):
        izq = self.analizar(nodo.izquierda)
        der = self.analizar(nodo.derecha)

        if nodo.op == "y":
            return izq and der
        if nodo.op == "o":
            return izq or der

        raise CompilerError(
            f"Operador lógico no soportado: {nodo.op}",
            nodo.linea
        )