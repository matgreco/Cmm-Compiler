# Cmm-Compiler

## PARA INSTALAR 
export CLASSPATH=".:/home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar:$CLASSPATH"
alias antlr4='java -jar /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar'
alias grun='java org.antlr.v4.gui.TestRig'

## PARA GENERAR EL LEXER Y PARSER
antlr4 Cmm2.g4
javac Cmm2*.java -cp /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar


## CODIGOS PARA PROBAR Y GENERAR EL ARBOL

### prueba evaluando un if que asigna dos variables
echo "if(casa == 10){casaa = 20; casab =0; }" | grun Cmm2 expression -gui

### una funcion
echo "void main(){int unavariable; unavariable = funcion1(argumento1, argumento2, 3);}"
