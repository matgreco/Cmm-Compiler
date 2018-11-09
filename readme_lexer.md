# Cmm-Compiler

## PARA INSTALAR 
- export CLASSPATH=".:/home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar:$CLASSPATH"
- alias antlr4='java -jar /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar'
- alias grun='java org.antlr.v4.gui.TestRig'

## PARA GENERAR EL LEXER Y PARSER
- antlr4 Cmm2.g4
- javac Cmm2*.java -cp /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar


## CODIGOS PARA PROBAR Y GENERAR EL ARBOL
Para ejecutar códigos de prueba bajo la gramática definida por C+- y ver el AST generado, debe ejecutar el script compile.sh junto con el archivo a ejecutar.
Recordar que es necesario tener java instalado

I.E.:

- ./compile.sh tests/error_do.cmm 
- ./compile.sh tests/error_if.cmm 
- ./compile.sh tests/test.cmm 
- ./compile.sh tests/test_comma_operation.cmm 
- ./compile.sh tests/test_function_struct.cmm
- ./compile.sh tests/test_struct.cmm
- ./compile.sh tests/test_switch.cmm

## Pruebas con código inline
- prueba evaluando un if que asigna dos variables
echo "if(casa == 10){casaa = 20; casab =0; }" | grun Cmm2 build -gui

- una funcion
echo "void main(){int unavariable; unavariable = funcion1(argumento1, argumento2, 3);}" | grun Cmm2 build -gui


