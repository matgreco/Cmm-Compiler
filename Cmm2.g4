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
    TYPE VAR
    | TYPE VAR '=' expression
    | TYPE VAR '[' NUMBER ']'
;

assign_expression:
    VAR assign_op expression
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
    expression?';'
    | declare_expression';'
    | 'break' ';'
    | 'continue' ';'
    | 'return' expression? ';'
    | if_statement
    | while_statement
    | for_statement
    | '{' statement* '}'
;

if_statement:
    If '(' expression ')' statement
    | If '(' expression ')' statement Else statement
//    | If '(' expression ')' '{' statement* '}'
//    | If '(' expression ')' '{' statement* '}' Else '{' statement* '}'
//    | If '(' expression ')' statement Else '{' statement* '}'
//    | If '(' expression ')' '{' statement* '}' Else statement
;

while_statement:
    While'(' expression ')' statement
//    | While '(' expression ')' '{' statement* '}'
;

for_statement:
    For '('(expression | declare_expression) ';' expression ';' expression ')' statement
//    | For '('(expression | declare_expression) ';' expression ';' expression ')' '{' statement* '}'
;

function_call_expression : 
    VAR '(' (expression (',' expression)*)? ')'  
;

function_definition : 
    TYPE VAR '(' (TYPE VAR (',' TYPE VAR)*)? ')' '{' statement* '}'  
;

forward_function_definition:
    TYPE VAR '(' (TYPE VAR? (',' TYPE VAR?)*)? ')' ';'
;

struct_definition:
    'struct' VAR '{'
        declare_statement*
    '}'';'
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


DEC_NUMBER:
    '0'
    | [1-9][0-9]*
;

OCT_NUMBER:
    '0'[0-7][0-7]*
;

HEX_NUMBER:
    ('0x' | '0X')[0-9a-fA-F][0-9a-fA-F]*
;

TYPE:
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
True:'true';
False:'false';
Struct:'struct';
//String:'string'; //?


VAR:
    [a-zA-Z_][a-zA-Z0-9_]*
;


WS
    : [ \t\u000C\r\n]+ -> skip
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

expression:
    '(' expression ')'
    | NUMBER
    | STRING_CONSTANT
    | VAR
    | expression '.' VAR 
    | function_call_expression | (VAR '[' expression ']') // expression[expression] para permitir usar 0[var] == var[0]
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
    | expression ',' expression
;