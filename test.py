import sys
from antlr4 import *
from Cmm2Lexer import Cmm2Lexer
from Cmm2Parser import Cmm2Parser
from Cmm2Listener import Cmm2Listener
from Cmm2Visitor__ import Cmm2Visitor
 

input = FileStream(sys.argv[1])
lexer = Cmm2Lexer(input)
stream = CommonTokenStream(lexer)
parser = Cmm2Parser(stream)
tree = parser.build()

visitor = Cmm2Visitor()
result = visitor.visit(tree)

