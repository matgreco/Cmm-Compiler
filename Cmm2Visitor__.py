# Generated from Cmm2.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Cmm2Parser import Cmm2Parser
else:
    from Cmm2Parser import Cmm2Parser
from anytree import Node, RenderTree

# This class defines a complete generic visitor for a parse tree produced by Cmm2Parser.


def Initialize_scope(scope):
    #print("Nuevo scope")
    nuevo_scope = Node(dict({}),scope)
    return nuevo_scope

def Finalize_scope(scope):
    #print("Fin scope")
    nuevo_scope = scope.parent
    #mostrarArbol(scope)
    return nuevo_scope

def Consultar(scope, name):
    #print("Consultar")
    test_scope = scope
    while True :
        if name in test_scope.name:
            #print("OK, simbolo encontrado, valor: ", test_scope.name[name])
            return test_scope.name[name]
        else:
            if test_scope.is_root == True:
                break
            test_scope = test_scope.parent

    if test_scope.is_root == True :
        #print("Simbolo no existe")
        return None


def mostrarArbol(nodo):
    print("+++++++++++++++++++++++++ TABLA DE SIMBOLOS +++++++++++++++++++++++++++++++")
    for pre, fill, node in RenderTree(nodo):
        if node.name :
            print( pre, node.name)









def Error(msg, line):
    print("Error en linea: "+str(line)+": " + str(msg))


def stoi(s:str):
    if s[0] == '\'':
        if len(s) != 3:
            Error("Caracter invalido: "+s,0)
            return [0,'int']
        else:
            return [ord(s[1]),'char']
    if s[-1] in ["ll","LL"]:
        s = s[:-2]
        base = 10
        if s[0:2] in ["0x","0X"]:
            s = s[2:]
            base = 16
        elif s[0] == "0":
            base = 8
        return [(int(s,base) & (2<<64 - 1)), 'long']
    else:
        base = 10
        if s[0:2] in ["0x","0X"]:
            s = s[2:]
            base = 16
        elif s[0] == "0":
            base = 8
        return [(int(s,base) & (2<<32 - 1)), 'int']



class symbol:
    def __init__(self, stype, name, vtype, info, line = 0):
        self.stype = stype #function, struct, variable, value
        self.name = name #name. If stype = 'value': it's value if constant, None if dependant of runtime
        self.vtype = vtype
        self.info = info #information about symbol:
        #function: [[arg1, opts], [arg2, opts], ...]
        #struct: [[member1, type], [member2, type], ...]
        #variable: []
        #value: []
        self.line = line
    def __str__(self):
        return self.name + "("+ self.stype + " " + self.vtype[0] + ")"
    def __repr__(self):
        return "("+ str(self.vtype) + ")"

    
class Cmm2Visitor(ParseTreeVisitor):

    def __init__(self):
        self.structs = dict() #[[member1, type], [member1, type], ...]
        self.functions = dict() #[return_type, [arg_type, opt], [arg_type, opt], ...]
        self.tree = Node(dict({}))
        self.where = 'global' #'global', 'function', 'struct'
        self.last_loop = None


    # Visit a parse tree produced by Cmm2Parser#build.
    def visitBuild(self, ctx:Cmm2Parser.BuildContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#declare_statement.
    def visitDeclare_statement(self, ctx:Cmm2Parser.Declare_statementContext):
        #print(self.visit(ctx.type_cmm()))
        if ctx.declare_expression() != None:
            return self.visit(ctx.declare_expression())
        if ctx.declare_assign_expression() != None:
            return self.visit(ctx.declare_assign_expression())


    # Visit a parse tree produced by Cmm2Parser#declare_normal.
    def visitDeclare_normal(self, ctx:Cmm2Parser.Declare_normalContext):
        #print("PPPP_ ",ctx.VAR().getText())
        vtype = self.visit(ctx.type_cmm())
        name = ctx.VAR().getText()
        line = ctx.start.line
        if name in self.tree.name:
            Error(name + " ya est\'a definida en este scope en la linea " + str(self.tree.name[name].line), line)
        else:
            self.tree.name[name] = symbol("variable", name, vtype, [], line)
        return None


    # Visit a parse tree produced by Cmm2Parser#declare_array.
    def visitDeclare_array(self, ctx:Cmm2Parser.Declare_arrayContext):
        vtype = self.visit(ctx.type_cmm())
        name = ctx.VAR().getText()
        line = ctx.start.line
        val = self.visit(ctx.expression())
        if name in self.tree.name:
            Error(name + " ya est\'a definida en este scope en la linea " + str(self.tree.name[name].line), line)
        else:
            self.tree.name[name] = symbol("variable", name, vtype + "[]", [], line)
        return None
    
    # Visit a parse tree produced by Cmm2Parser#declare_assign_expression.
    def visitDeclare_assign_expression(self, ctx:Cmm2Parser.Declare_assign_expressionContext):
        vtype = self.visit(ctx.type_cmm())
        name = ctx.VAR().getText()
        line = ctx.start.line
        if name in self.tree.name:
            Error(name + " ya est\'a definida en este scope en la linea " + str(self.tree.name[name].line), line)
        else:
            self.tree.name[name] = symbol("variable", name, vtype, [], line)
        val = self.visit(ctx.expression())
        return None

    # Visit a parse tree produced by Cmm2Parser#case_statement.
    def visitCase_statement(self, ctx:Cmm2Parser.Case_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#normal_statement.
    def visitNormal_statement(self, ctx:Cmm2Parser.Normal_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#break_statement.
    def visitBreak_statement(self, ctx:Cmm2Parser.Break_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#continue_statement.
    def visitContinue_statement(self, ctx:Cmm2Parser.Continue_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#block_statement.
    def visitBlock_statement(self, ctx:Cmm2Parser.Block_statementContext):
        #print("SSSSSSSSSSSSSSSSSSS")
        self.tree = Initialize_scope(self.tree)
        self.visitChildren(ctx)
        self.tree = Finalize_scope(self.tree)


    # Visit a parse tree produced by Cmm2Parser#if_statement.
    def visitIf_statement(self, ctx:Cmm2Parser.If_statementContext):
        #self.tree = Initialize_scope(self.tree)
        expression = self.visit(ctx.comma_expression())
        if_true = self.visit(ctx.statement(0))
        if_false = None
        if ctx.statement(1) != None:
            if_false = self.visit(ctx.statement(1))
        #self.tree = Finalize_scope(self.tree)
        return None


    # Visit a parse tree produced by Cmm2Parser#switch_statement.
    def visitSwitch_statement(self, ctx:Cmm2Parser.Switch_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#while_statement.
    def visitWhile_statement(self, ctx:Cmm2Parser.While_statementContext):
        #self.tree = Initialize_scope(self.tree)
        expression = self.visit(ctx.comma_expression())
        block = self.visit(ctx.statement())
        #self.tree = Finalize_scope(self.tree)
        return None

    # Visit a parse tree produced by Cmm2Parser#for_1.
    def visitFor_1(self, ctx:Cmm2Parser.For_1Context):
        if ctx.comma_expression() != None:
            return self.visit(ctx.comma_expression())
        if ctx.declare_statement != None:
            return self.visit(ctx.declare_statement())
        return None


    # Visit a parse tree produced by Cmm2Parser#for_2.
    def visitFor_2(self, ctx:Cmm2Parser.For_2Context):
        if ctx.comma_expression() != None:
            return self.visit(ctx.comma_expression())
        return None


    # Visit a parse tree produced by Cmm2Parser#for_3.
    def visitFor_3(self, ctx:Cmm2Parser.For_3Context):
        if ctx.comma_expression() != None:
            return self.visit(ctx.comma_expression())
        return None


    # Visit a parse tree produced by Cmm2Parser#for_statement.
    def visitFor_statement(self, ctx:Cmm2Parser.For_statementContext):
        self.tree = Initialize_scope(self.tree)
        if_init = self.visit(ctx.for_1())
        if_cond = self.visit(ctx.for_2())
        if_loop = self.visit(ctx.for_3())
        self.visit(ctx.statement())
        self.tree = Finalize_scope(self.tree)

    # Visit a parse tree produced by Cmm2Parser#do_statement.
    def visitDo_statement(self, ctx:Cmm2Parser.Do_statementContext):
        #self.tree = Initialize_scope(self.tree)
        block = self.visit(ctx.statement(0))
        expression = self.visit(ctx.comma_expression())
        #self.tree = Finalize_scope(self.tree)
        return None


    # Visit a parse tree produced by Cmm2Parser#function_call_expression.
    def visitFunction_call_expression(self, ctx:Cmm2Parser.Function_call_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#function_argument.
    def visitFunction_argument(self, ctx:Cmm2Parser.Function_argumentContext):
        vtype = self.visit(ctx.type_cmm())
        name = ctx.VAR().getText()
        op = ctx.op.text
        if op[0] == '[': #array
            vtype+='[]'
        if op == '&':
            return [vtype, name, '&']
        return [vtype, name, '']


    # Visit a parse tree produced by Cmm2Parser#forward_function_argument.
    def visitForward_function_argument(self, ctx:Cmm2Parser.Forward_function_argumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#function_definition.
    def visitFunction_definition(self, ctx:Cmm2Parser.Function_definitionContext):
        #Agrega el nombre de la funcion y el tipo a la symtab
        if ctx.type_cmm() is None :
            vtype = "void"
        else:
            vtype = self.visit(ctx.type_cmm())
        line = ctx.start.line
        name = ctx.VAR().getText()
        if name in self.tree.name:
            Error(name + " Ya esta definido en linea "+str(self.tree.name[name].line), line)
        i = 0
        args = []
        while ctx.function_argument(i) != None:
            args.append(self.visit(ctx.function_argument(i)))
            i += 1
        
        if not name in self.tree.name:
            self.tree.name[name] = symbol('funcion', name, vtype, args, line)

        #inicializa el scope y agrega lo de adentro
        self.tree = Initialize_scope(self.tree)
        for arg in args:
            self.tree.name[arg.name] = symbol("variable", name, vtype, [], line)
        i = 0
        while ctx.statement(i) != None:
            self.visit(ctx.statement(i))
            i += 1
        self.tree = Finalize_scope(self.tree)
        self.functions[name]=[vtype]
        for arg in args:
            self.functions[name].append([arg[0], arg[2]])
        return None



    # Visit a parse tree produced by Cmm2Parser#forward_function_definition.
    def visitForward_function_definition(self, ctx:Cmm2Parser.Forward_function_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#struct_definition.
    def visitStruct_definition(self, ctx:Cmm2Parser.Struct_definitionContext):
        name = ctx.VAR().getText()
        #print(ctx.start.__dict__)
        line = ctx.start.line
        if Consultar(self.tree, name) != None:
            Error(name + " ya esta definido en linea" + str(Consultar(self.tree,name).line),line)
        self.where = 'struct'
        self.tree = Initialize_scope(self.tree)
        members = []
        i = 0
        member = self.visit(ctx.declare_statement(i))
        while member != None:
            members.append(member)
            i += 1
            member = self.visit(ctx.declare_statement(i))
        self.tree = Finalize_scope(self.tree)
        if Consultar(self.tree, name) == None:
            self.tree.name[name] = symbol('struct', name, "", members, line)
        self.where = 'global'
        self.structs[name] = []
        for member in members:
            self.structs[name].append([member.name, member.vtype])
        return None


    # Visit a parse tree produced by Cmm2Parser#type_cmm.
    def visitType_cmm(self, ctx:Cmm2Parser.Type_cmmContext):
        if ctx.Int() != None:
            return "int"
        if ctx.Char() != None:
            return "char"
        if ctx.Double() != None:
            return "double"
        if ctx.Long() != None:
            return "long"
        if ctx.Short() != None:
            return "short"
        if ctx.Float() != None:
            return "float"
        if ctx.VAR() != None:
            return ["struct", ctx.VAR().getText()]



    # Visit a parse tree produced by Cmm2Parser#comma_expression.
    def visitComma_expression(self, ctx:Cmm2Parser.Comma_expressionContext):
        if ctx.comma_expression() == None:
            return self.visit(ctx.expression()) 
        else:
            self.visit(ctx.comma_expression())
            return self.visit(ctx.expression())


    # Visit a parse tree produced by Cmm2Parser#expAssign.
    def visitExpAssign(self, ctx:Cmm2Parser.ExpAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expRightUnary.
    def visitExpRightUnary(self, ctx:Cmm2Parser.ExpRightUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expFunctionCall.
    def visitExpFunctionCall(self, ctx:Cmm2Parser.ExpFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expDot.
    def visitExpDot(self, ctx:Cmm2Parser.ExpDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expTerOp.
    def visitExpTerOp(self, ctx:Cmm2Parser.ExpTerOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expArray.
    def visitExpArray(self, ctx:Cmm2Parser.ExpArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expLeftUnary.
    def visitExpLeftUnary(self, ctx:Cmm2Parser.ExpLeftUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expOp.
    def visitExpOp(self, ctx:Cmm2Parser.ExpOpContext):
        
        #left = self.tree.name[ctx.expression(0).VAR().getText()]
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        #print("---------------------------- L y R ", left.vtype, right.vtype)
        #right = ctx.expression(1).VAR().getText()
        op = ctx.op.text
        """
        if Consultar(self.tree, left) != None:
            print("AAAAAAAA  ",self.tree.name[left].stype)
        else :
            print("Error en linea",ctx.op.line , ": variable ",left ,"no está declarada")

        """
        #print("los tipos son ", Consultar(self.tree, left).stype)

        if op == '+':
            #print("SUMAA entre ",left,right)
            pass
        elif op == '-':
            pass
        elif op == '*':
            pass
        elif op == '/':
            pass
        elif op == '%':
            pass
        elif op == '<<':
            pass
        elif op == '>>':
            pass
        elif op == '<':
            pass
        elif op == '<=':
            pass
        elif op == '>':
            pass
        elif op == '>=':
            pass
        elif op == '==':
            pass
        elif op == '!=':
            pass
        elif op == '&':
            pass
        elif op == '^':
            pass
        elif op == '|':
            pass
        elif op == '&&':
            pass
        elif op == '||':
            pass
        if left == None or right == None:
            return None

        type1 = left.stype
        type2 = right.stype
        return symbol(left.stype,"", left.vtype,list(left.stype))


    # Visit a parse tree produced by Cmm2Parser#expAtom.
    def visitExpAtom(self, ctx:Cmm2Parser.ExpAtomContext):
        if ctx.VAR() != None:
            if Consultar(self.tree, ctx.VAR().getText()) == None:
                line = ctx.start.line
                
                Error(ctx.VAR().getText() + " no esta definido", line)
                return None
            else:
                x = Consultar(self.tree, ctx.VAR().getText())
                if x.stype == "function" or x.stype == "struct":
                    line = ctx.start.line
                    Error(x.name+ " no es una variable", line)
                    return None
                return x
        if ctx.INT_NUMBER() != None:
            val = stoi(ctx.INT_NUMBER().getText())
            return symbol('value', val[0], val[1],[])
        if ctx.STRING_CONSTANT() != None:
            return symbol('value', ctx.STRING_CONSTANT().getText(),"char[]",[])
        if ctx.FLOAT_NUMBER() != None:
            return symbol('value', float(ctx.FLOAT_NUMBER().getText()), "double",[])


    # Visit a parse tree produced by Cmm2Parser#expPar.
    def visitExpPar(self, ctx:Cmm2Parser.ExpParContext):
        return self.visit(ctx.comma_expression())


    # Visit a parse tree produced by Cmm2Parser#expSizeof.
    def visitExpSizeof(self, ctx:Cmm2Parser.ExpSizeofContext):
        return symbol("value", "", "int", [])



del Cmm2Parser
