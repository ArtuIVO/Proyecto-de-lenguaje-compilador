from logica_del_lenguaje import Lexer, Parser

def main():

    print("=== Lenguaje de NPCs ===")
    print("Escribe tu script (línea vacía para terminar):\n")

    lineas = []

    while True:
        linea = input(">> ")
        if linea.strip() == "":
            break
        lineas.append(linea)

    codigo = " ".join(lineas)  

    print("\n--- ANALISIS LEXICO ---")

    lexer = Lexer(codigo)
    tokens = lexer.analizar()

    for t in tokens:
        print(f"{t.valor} -> {t.tipo}")

    print("\n--- ANALISIS SINTACTICO ---")

    try:
        parser = Parser(tokens)
        parser.parse()
        print("Programa válido")
    except SyntaxError as e:
        print("Error sintáctico:", e)


if __name__ == "__main__":
    main()