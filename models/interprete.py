class Interprete:

    def ejecutar(self, tokens):
        memoria = {}
        resultados = []

        i = 0
        while i < len(tokens) - 2:
            t1, op, t2 = tokens[i], tokens[i+1], tokens[i+2]

            if t1.tipo == "IDENTIFICADOR" and op.valor == "=" and t2.tipo == "NUMERO":
                memoria[t1.valor] = int(t2.valor)
                resultados.append(f"{t1.valor} = {t2.valor}")

            i += 1

        return resultados