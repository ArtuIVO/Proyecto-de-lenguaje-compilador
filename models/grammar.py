GRAMMAR = """
<programa> ::= <sentencias>

<sentencias> ::= <sentencia> | <sentencia> <sentencias>

<sentencia> ::= <asignacion>
              | <if>
              | <escribir>

<asignacion> ::= IDENTIFICADOR "=" <expresion>

<if> ::= "si" <expresion> ":" <sentencia>

<escribir> ::= "escribir" "(" <expresion> ")"

<expresion> ::= <comparacion>

<comparacion> ::= <aritmetica>
                | <aritmetica> "==" <aritmetica>
                | <aritmetica> "!=" <aritmetica>
                | <aritmetica> "<" <aritmetica>
                | <aritmetica> ">" <aritmetica>

<aritmetica> ::= <termino>
               | <aritmetica> "+" <termino>
               | <aritmetica> "-" <termino>

<termino> ::= <factor>
            | <termino> "*" <factor>
            | <termino> "/" <factor>

<factor> ::= NUMERO
           | IDENTIFICADOR
           | "(" <expresion> ")"
"""