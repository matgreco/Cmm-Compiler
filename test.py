import sys
import subprocess
from antlr4 import *
from Cmm2Lexer import Cmm2Lexer
from Cmm2Parser import Cmm2Parser
#from Cmm2Listener import Cmm2Listener
from Cmm2Visitor__ import *
 

input = FileStream(sys.argv[1])
lexer = Cmm2Lexer(input)
stream = CommonTokenStream(lexer)
parser = Cmm2Parser(stream)
tree = parser.build()

visitor = Cmm2Visitor()
result,llvm_output = visitor.visit(tree)
llvm_output.append("declare i32 @printf(i8*, ...) #1")

mostrarArbol(visitor.tree)

txt_code = ''.join(llvm_output)
print("------------  - - - - CODIGO GENERADO - - - - -----------------")
print(txt_code)
print("---------------------------------------------------------------")
file_s = sys.argv[1].split(".")[0]+".ll"
file_o = sys.argv[1].split(".")[0]+".o"
file_out = sys.argv[1].split(".")[0]+".out"

f = open(file_s, "w")
f.write( txt_code )
f.close()

#print(file_s + "  _____ " + file_o)
#print("1 *****************************************")
subprocess.call(["llc", file_s, "-filetype=obj"] )
#print("2 *****************************************")
subprocess.call(["gcc", file_o ,"-o"+ file_out , "-no-pie"])
#print("3 *****************************************")
#subprocess.call(["./out.out"])