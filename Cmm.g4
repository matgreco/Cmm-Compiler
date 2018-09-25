// Nombre de la gramatica.
grammar Cmm;

expesionCondicional :
    If '(' condicion ')' instruccion
    | If '(' condicion ')' instruccion Else instruccion
    | If '(' condicion ')' '{' instruccion* '}'
    | If '(' condicion ')' '{' instruccion* '}' Else '{' instruccion* '}'
    | If '(' condicion ')' instruccion Else '{' instruccion* '}'
    | If '(' condicion ')' '{' instruccion* '}' Else instruccion
;

condicion :
    //definir condicion
    var comparador var
    | var comparador NUMBER
    | var comparador BOOLEAN
;

comparador :
    '==' 
    | '<='
    | '>='
    | '<'
    | '>'
;

instruccion : 
    // definir instruccion
;



// PALABRAS RESERVADAS. KEYWORDS

If :
    'if'
;
Else :
    'else'
;


NUMBER :
    DIGIT*
;

DIGIT :
    [0-9]
;














/*
// ESTO VENIAEN EL EJEMPLO
// We define expression to be either a method call or a string.
expression
    : methodCall
    | STRING
    ;

// We define methodCall to be a method name followed by an opening
// paren, an optional list of arguments, and a closing paren.
methodCall
    : methodName '(' methodCallArguments ')'
    ;

// We define methodName to be a name.
methodName
    : NAME
    ;

// We define methodCallArguments to be a list of expressions
// separated by commas.
methodCallArguments
    : // No arguments
    | expression (',' expression)*  // Some arguments
    ;

// NAME represents any variable or method name.
// The regular expression we use basically means "starts with a letter
// and may follow with any number of alphanumerical characters"
NAME
    : [a-zA-Z][a-zA-Z0-9]*
    ;

// STRING represents a string value, for example "abc".
// Note that for simplicity, we don't allow escaping double quotes.
STRING
    : '"' ~('"')* '"'
    ;

// WS represents a whitespace, which is ignored entirely by skip.
WS
    : [ \t\u000C\r\n]+ -> skip
;

*/