// Nombre de la gramatica.
grammar Cmm2;


build:
    (
        declare_statement//usar solo declaraciones sin asignacion?
        | forward_function_definition
        | function_definition
        | struct_definition
        | ';'
    )*
;



//TODO? cambiar orden?

declare_statement:
    declare_expression ';'
;

declare_expression:
    type VAR ('=' expression (',' VAR ('=' expression)?)*)?
    | type VAR '[' comma_expression ']'
;

assign_expression:
    (VAR | member_var) assign_op expression
;

compare_expression:
    expression compare_op expression
;

compare_op:
    '=='
    | '<='
    | '>='
    | '<'
    | '>'
;

assign_op:
    '='
    | '+='
    | '-='
    | '*='
    | '/='
    | '%='
    | '<<='
    | '>>='
    | '&='
    | '^='
    | '|='
;

unary_left_op:
    '++'
    | '--'
    | '+'
    | '-'
    | '!'
    | '~'
;

statement:
    comma_expression?';'
    | declare_statement
    | 'break' ';'
    | 'continue' ';'
    | 'return' comma_expression? ';'
    | if_statement
    | while_statement
    | for_statement
    | '{' statement* '}'
;

if_statement:
    If '(' comma_expression ')' statement
    | If '(' comma_expression ')' statement Else statement
//    | If '(' expression ')' '{' statement* '}'
//    | If '(' expression ')' '{' statement* '}' Else '{' statement* '}'
//    | If '(' expression ')' statement Else '{' statement* '}'
//    | If '(' expression ')' '{' statement* '}' Else statement
;

while_statement:
    While'(' comma_expression ')' statement
//    | While '(' expression ')' '{' statement* '}'
;

for_statement:
    For '('(comma_expression | declare_expression) ';' comma_expression ';' comma_expression ')' statement
//    | For '('(expression | declare_expression) ';' expression ';' expression ')' '{' statement* '}'
;

function_call_expression : 
    VAR '(' (expression (',' expression)*)? ')'  
;

function_definition : 
    (type | 'void') VAR '(' ((type VAR (',' type VAR)*)? | 'void') ')' '{' statement* '}'  
;

forward_function_definition:
    (type | 'void') VAR '(' ((type VAR? (',' type VAR?)*)? | 'void') ')' ';'
;

struct_definition:
    'struct' VAR '{'
        declare_statement*
    '}' ';'
;

NUMBER:
    DEC_NUMBER
    | OCT_NUMBER
    | HEX_NUMBER
;

//TODO? poner escape characters?
STRING_CONSTANT :
    '"' ~('"')* '"'
;

CHAR_CONSTANT:
    '\'' ~('\'')* '\''
;


DEC_NUMBER:
    '0'
    | [1-9][0-9]*
;

OCT_NUMBER:
    '0'[0-7]+
;

HEX_NUMBER:
    ('0x' | '0X')[0-9a-fA-F]+
;

type:
    Int
    | Char
    | 'struct' VAR
//  | String //?
;

//KEYWORDS
Int:'int';
Char:'char';
If:'if';
Else:'else';
While:'while';
For:'for';
Break:'break';
Continue:'continue';
True:'true';
False:'false';
Struct:'struct';
Void:'void';
//String:'string'; //?


VAR:
    [a-zA-Z_][a-zA-Z0-9_]*
;


WS
    : [ \t\u000C\r\n]+ -> skip
;

//Comments
COMMENT:
    '//' ~[\n]* -> skip
;

MULTILINE_COMMENT:
    '/*' ~[*/]* '*/' -> skip
;

/*
    EXPRESSIONS:
    HIGHER PRECEDENCE
    1   right_unary
        ++/--
        ()
        []
        .
    2   left_unary_operator_expression
        ++/--
        left unary +/-
        !
        ~
    3   operator_expression
        *
        /
        %
    4
        +
        -
    5
        <<
        >>
    6
        <
        <=
        >
        >=
    7
        ==
        !=
    8
        &
    9
        ^
    10
        |
    11
        &&
    12
        ||
    13  expression
        =
        +=
        -=
        *=
        /=
        %=
        <<=
        >>=
        &=
        ^=
        |=
    14 comma_expression
        comma operator ,
 */

comma_expression:
    expression
    | comma_expression ',' expression
;

//tratar a.b.c.d (...) como variables
member_var:
    VAR
    | member_var '.' VAR
;

expression:
    '(' comma_expression ')'
    | NUMBER
    | STRING_CONSTANT
    | CHAR_CONSTANT
    | VAR
    | member_var
    | function_call_expression | ((VAR | member_var) '[' expression ']') // expression[expression] para permitir usar 0[var] == var[0]
    | expression ('++' | '--')
    | unary_left_op expression
    | expression ('*' | '/' | '%') expression
    | expression ('+' | '-') expression
    | expression ('<<' | '>>') expression
    | expression ('<' | '<=' | '>' | '>=') expression
    | expression ('==' | '!=') expression
    | expression '&' expression
    | expression '^' expression
    | expression '|' expression
    | expression '&&' expression
    | expression '||' expression
    | <assoc=right>assign_expression
;
