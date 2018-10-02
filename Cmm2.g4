// Nombre de la gramatica.
grammar Cmm2;


build:
    (
        declare_statement //usar solo declaraciones sin asignacion?
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
    type VAR ('=' expression)? (',' VAR ('=' expression)?)*
    | type VAR '[' comma_expression ']'
;

assign_expression:
    (VAR | member_var) assign_op expression
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
    | Break ';'
    | Continue ';'
    | Return comma_expression? ';'
    | Case INT_NUMBER ':' //modificar para usar constant expression (?)
//    | VAR ':' //label
//    | Goto VAR ';'
    | if_statement
    | while_statement
    | for_statement
    | switch_statement
    | do_statement
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
switch_statement:
    Switch '(' expression ')' '{' statement* '}'
;

default_statement : 
    Default ':' statement*
;



while_statement:
    While'(' comma_expression ')' statement
//    | While '(' expression ')' '{' statement* '}'
;

for_statement:
    For '('(comma_expression | declare_expression)? ';' comma_expression? ';' comma_expression? ')' statement
//    | For '('(expression | declare_expression) ';' expression ';' expression ')' '{' statement* '}'
;

do_statement:
    Do statement While '(' comma_expression ')' ';'
;


function_call_expression : 
    VAR '(' (expression (',' expression)*)? ')'  
;

function_definition : 
    (type | 'void') VAR '(' ((type '&'? VAR (',' type '&'? VAR)*)? | 'void') ')' '{' statement* '}'  
;

forward_function_definition:
    (type | 'void') VAR '(' ((type '&'? VAR? (',' type '&'? VAR?)*)? | 'void') ')' ';'
;

struct_definition:
    'struct' VAR '{'
        declare_statement*
    '}' ';'
;

FLOAT_NUMBER :
    [0-9]* '.' [0-9]+
    | [0-9]+ '.' [0-9]*
;

INT_NUMBER:
    DEC_NUMBER ('u' | 'U')? ('ll' | 'LL')?
    | OCT_NUMBER ('u' | 'U')? ('ll' | 'LL')?
    | HEX_NUMBER ('u' | 'U')? ('ll' | 'LL')?
    | CHAR_CONSTANT
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
    Unsigned? Int
    | Unsigned? Char
    | Double
    | Unsigned? Long
    | Unsigned? Short
    | Float
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
Return:'return';

Switch:'switch';
Case:'case';
Default:'default';
Do:'do';

Double:'double';
Long:'long';
Short:'short';
Float:'float';
Unsigned:'unsigned';
Sizeof:'sizeof';


//unused
Const:'const';
Static:'static';
Auto:'auto';
Goto:'goto';



//Typedef:'typedef';

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
        sizeof()
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
    | INT_NUMBER
    | STRING_CONSTANT
    | CHAR_CONSTANT
    | VAR
    | expression '.' VAR
    | 'sizeof' '(' (expression | type) ')'
    | function_call_expression
    | expression '[' expression ']' // expression[expression] para permitir usar 0[var] == var[0]
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
    | <assoc=right> expression '?' comma_expression ':' expression
    | <assoc=right>assign_expression
;
