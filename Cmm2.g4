// Nombre de la gramatica.
grammar Cmm2;


//TODO? cambiar orden?


declare_expression:
    TYPE VAR
    | TYPE VAR '=' expression
;

assign_expression:
    VAR assign_op expression
;

compare_expression:
    VAR compare_op VAR  
    | VAR compare_op expression
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
;

statement:
    expression';'
    | declare_expression';'
    | if_statement
    | while_statement
    | for_statement
//  | '{' statement* '}' //?
;

if_statement:
    If '(' expression ')' statement
    | If '(' expression ')' statement Else statement
    | If '(' expression ')' '{' statement* '}'
    | If '(' expression ')' '{' statement* '}' Else '{' statement* '}'
    | If '(' expression ')' statement Else '{' statement* '}'
    | If '(' expression ')' '{' statement* '}' Else statement
;

while_statement:
    While'(' expression ')' statement
    | While '(' expression ')' '{' statement* '}'
;

for_statement:
    For '('(expression | declare_expression) ';' expression ';' expression ')' statement
    | For '('(expression | declare_expression) ';' expression ';' expression ')' '{' statement* '}'
;

function_call_statement : 
    VAR '(' expression (',' expression)? ')'  
;

function_definition_statement : 
    TYPE VAR '(' TYPE VAR (',' TYPE VAR)? ')' '{' statement '}'  
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
//String:'string'; //?


VAR:
    [a-zA-Z_][a-zA-Z0-9_]*
;


WS
    : [ \t\u000C\r\n]+ -> skip
;




expression:
    '(' expression ')'
    | NUMBER
    | STRING_CONSTANT
    | VAR
    | assign_expression
    | compare_expression
;