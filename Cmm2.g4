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
    declare_assign_expression ';'
;

declare_expression:
    Type_cmm VAR #declare_normal
    | Type_cmm VAR '[' comma_expression ']' #declare_array
;


declare_assign_expression:
    Type_cmm VAR ('=' expression)?
;


case_statement:
    Case INT_NUMBER ':'
    | Default;

statement:
    comma_expression?';' #normal_statement
    | declare_expression ';' #normal_statement
    | Break ';' #break_statement
    | Continue ';' #continue_statement
    | Return comma_expression? ';' #normal_statement
    | case_statement #normal_statement
//    | VAR ':' //label
//    | Goto VAR ';'
    | if_statement #normal_statement
    | while_statement #normal_statement
    | for_statement #normal_statement
    | switch_statement #normal_statement
    | do_statement #normal_statement
    | '{' statement* '}' #block_statement
;

if_statement:
    If '(' comma_expression ')' statement (Else statement)?
//    | If '(' comma_expression ')' statement Else statement
//    | If '(' expression ')' '{' statement* '}'
//    | If '(' expression ')' '{' statement* '}' Else '{' statement* '}'
//    | If '(' expression ')' statement Else '{' statement* '}'
//    | If '(' expression ')' '{' statement* '}' Else statement
;
switch_statement:
    Switch '(' comma_expression ')' '{' statement* '}'
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

FUNCTION_ARGUMENT_OPTION:
    '&'
    | '[' ']'
;

function_argument:
    Type_cmm op=FUNCTION_ARGUMENT_OPTION? VAR
;

forward_function_argument:
    Type_cmm op=FUNCTION_ARGUMENT_OPTION? VAR?
;


function_definition : 
    T=(Type_cmm | 'void') VAR '(' (function_argument (',' function_argument)*) |('void'?) ')' '{' statement* '}'  
;

forward_function_definition:
    T = (Type_cmm | 'void') VAR '('(forward_function_argument (',' forward_function_argument)*) |('void'?) ')' ';'
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
    DEC_NUMBER ('ll' | 'LL')?
    | OCT_NUMBER ('ll' | 'LL')?
    | HEX_NUMBER ('ll' | 'LL')?
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

Type_cmm:
    Int
    | Char
    | Double
    | Long
    | Short
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
True_cmm:'true';
False_cmm:'false';
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
//Const:'const';
//Static:'static';
//Auto:'auto';
//Goto:'goto';



//type_cmmdef:'type_cmmdef';

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
    '/*' .*? '*/' -> skip
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


expression:
    '(' comma_expression ')' #expPar
    | INT_NUMBER #expAtom
    | STRING_CONSTANT #expAtom
    | FLOAT_NUMBER #expAtom
    | VAR #expAtom
    | expression '.' VAR #expDot
    | 'sizeof' '(' (expression | Type_cmm) ')' #expSizeof
    | function_call_expression #expFunctionCall
    | expression '[' expression ']' #expArray// expression[expression] para permitir usar 0[var] == var[0]
    | expression op=('++' | '--') #expRightUnary
    | op=('++'| '--'| '+'| '-'| '!'| '~') expression #expLeftUnary
    | expression op=('*' | '/' | '%') expression #expOp
    | expression op=('+' | '-') expression #expOp
    | expression op=('<<' | '>>') expression #expOp
    | expression op=('<' | '<=' | '>' | '>=') expression #expOp
    | expression op=('==' | '!=') expression #expOp
    | expression op='&' expression #expOp
    | expression op='^' expression #expOp
    | expression op='|' expression #expOp
    | expression op='&&' expression #expOp
    | expression op='||' expression #expOp
    | <assoc=right> expression '?' comma_expression ':' expression #expTerOp
    | <assoc=right> expression op=('='| '+='| '-='| '*='| '/='| '%='| '<<='| '>>='| '&='| '^='| '|=') expression #expAssign
;
