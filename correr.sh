declare ruta_absoluta="/home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar"
export CLASSPATH=".:/home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar:$CLASSPATH"
alias antlr4='java -jar /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar'
alias grun='java org.antlr.v4.gui.TestRig'
echo "Done $ruta_absoluta"



antlr4 Cmm.g4
javac Cmm*.java -cp /home/mat/Escritorio/antlr/antlr-4.7.1-complete.jar
