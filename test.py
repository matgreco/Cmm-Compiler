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

print(''.join(llvm_output))


file_s = sys.argv[0].split(".")[0]+".ll"
file_o = sys.argv[0].split(".")[0]+".o"

f = open(file_s, "w+")
f.write(''.join(llvm_output))
#subprocess.call(["ls", "-l"])
subprocess.call(["llc", file_s, "-filetype=obj"] )
#subprocess.call(["gcc", file_o ,"-o out.out -no-pie"])
#subprocess.run(["./out.out"])