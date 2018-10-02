#!/bin/sh

export CLASSPATH=".:antlr-4.7.1-complete.jar:$CLASSPATH"
alias antlr4='java -jar antlr-4.7.1-complete.jar'
alias grun='java org.antlr.v4.gui.TestRig'

antlr4 Cmm2.g4
javac Cmm2*.java -cp antlr-4.7.1-complete.jar

grun Cmm2 build -gui < $1