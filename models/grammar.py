GRAMMAR = """
<programa> ::= <sentencias>

<sentencias> ::= <sentencia> | <sentencia> <sentencias>

<sentencia> ::= <if> | <asignacion> | <expresion>

<if> ::= "si" <expresion> ":" <sentencias>

<asignacion> ::= IDENTIFICADOR "=" <expresion>

<expresion> ::= <termino> | <termino> <operador> <expresion>

<termino> ::= IDENTIFICADOR | NUMERO

<operador> ::= "==" | "!=" | "<" | ">" | "<=" | ">=" | "y" | "o"
"""