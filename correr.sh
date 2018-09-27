#!/bin/sh
export CLASSPATH=".:/home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar:$CLASSPATH"
alias antlr4='java -jar /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar'
alias grun='java org.antlr.v4.gui.TestRig'
echo "Done $ruta_absoluta"



antlr4 Cmm2.g4
javac Cmm2*.java -cp /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar
