#!/bin/sh

export CLASSPATH=".:/home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar:$CLASSPATH"
alias antlr4='java -jar /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar'
alias grun='java org.antlr.v4.gui.TestRig'

antlr4 Cmm2.g4
javac Cmm2*.java -cp /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar

grun Cmm2 build -gui < $1