# Generated from Cmm2.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Cmm2Parser import Cmm2Parser
else:
    from Cmm2Parser import Cmm2Parser
from anytree import Node, RenderTree
from pprint import pprint
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
    print()
    print("+++++++++++++++++++++++++ TABLA DE SIMBOLOS +++++++++++++++++++++++++++++++")
    for pre, fill, node in RenderTree(nodo):
        if node.name :
            print( pre, node.name)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


def llc_vtype(type):
    if type == 'int':
        return 'i32'
    if type == 'void' :
        return 'void'
    if type == 'float' :
        return 'float'
    if type =='char' :
        return 'i8'


def Error(msg, line):
    print("Error en linea "+str(line)+": " + str(msg))


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
        self.value = ""
        self.line = line
    def __str__(self):
        return str(self.name) + "("+ str(self.stype) + " " + str(self.vtype[0]) + ")"
    def __repr__(self):
        return "("+ str(self.vtype) + ")"

    







codigo = list()

class Cmm2Visitor(ParseTreeVisitor):

    def __init__(self):
        self.structs = dict() #{"member":"type"}
        self.functions = dict() #[return_type, [arg_type, opt], [arg_type, opt], ...]
        self.tree = Node(dict({}))
        self.where = 'global' #'global', 'function', 'struct'

        #Agrega print
        self.functions['print']=['int']
        self.functions['print'].append(['int', 'int'])
        self.tree.name['print'] = symbol('function', 'print', 'void', list('int'), '0')

        self.n_registro = 0




    # Visit a parse tree produced by Cmm2Parser#build.
    def visitBuild(self, ctx:Cmm2Parser.BuildContext):
        return self.visitChildren(ctx),codigo


    # Visit a parse tree produced by Cmm2Parser#declare_statement.
    def visitDeclare_statement(self, ctx:Cmm2Parser.Declare_statementContext):
        #print(self.visit(ctx.type_cmm()))
        if ctx.declare_expression() != None:
            return self.visit(ctx.declare_expression())
        if ctx.declare_assign_expression() != None:
            return self.visit(ctx.declare_assign_expression())


    # Visit a parse tree produced by Cmm2Parser#declare_normal.
    def visitDeclare_normal(self, ctx:Cmm2Parser.Declare_normalContext):
        vtype = self.visit(ctx.type_cmm())
        name = ctx.VAR().getText()
        line = ctx.start.line
        if vtype[0] == "struct":
            if not vtype[1] in self.structs:
                Error("La estructura " + vtype[1] + " no esta definida", line)
        if name in self.tree.name:
            Error(name + " ya est\'a definida en este scope en la linea " + str(self.tree.name[name].line), line)
        else:
            self.tree.name[name] = symbol("variable", name, vtype, [], line)
            codigo.append("%" + name + " = alloca " + llc_vtype(vtype) + " \n")  
            return self.tree.name[name]
        
         
        return None


    # Visit a parse tree produced by Cmm2Parser#declare_array.
    def visitDeclare_array(self, ctx:Cmm2Parser.Declare_arrayContext):
        vtype = self.visit(ctx.type_cmm())
        name = ctx.VAR().getText()
        line = ctx.start.line
        val = self.visit(ctx.expression())
        if vtype[0] == "struct":
            if not vtype[1] in self.structs:
                Error("La estructura " + vtype[1] + " no esta definida", line)
        if name in self.tree.name:
            Error(name + " ya est\'a definida en este scope en la linea " + str(self.tree.name[name].line), line)
        else:
            if vtype[0] == "struct":
                vtype[0] = "struct[]"
                self.tree.name[name] = symbol("variable", name, vtype, [], line)
            else:
                self.tree.name[name] = symbol("variable", name, vtype + "[]", [], line)
            return self.tree.name[name]
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

        valor_asignacion = 2222 #ESTO DEBE SER EL VALOR ASIGNADO - CAMBIAR
        codigo.append("%" + name + " = " + " alloca " + llc_vtype(vtype) + " \n")
        codigo.append("%r" + str(self.n_registro) + " = add " + llc_vtype(vtype) + " " + str(valor_asignacion) + ", 0" + " \n")
        codigo.append("store "+ llc_vtype(vtype) + " " + "%r" + str(self.n_registro) + ", " + llc_vtype(vtype) + "* %" + name + " \n")
        return None


    # Visit a parse tree produced by Cmm2Parser#normal_statement.
    def visitNormal_statement(self, ctx:Cmm2Parser.Normal_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#break_statement.
    def visitBreak_statement(self, ctx:Cmm2Parser.Break_statementContext):
        if Consultar(self.tree, "%loop") == None:
            Error("Break statement fuera de un loop", ctx.start.line)
            return None
        return None


    # Visit a parse tree produced by Cmm2Parser#continue_statement.
    def visitContinue_statement(self, ctx:Cmm2Parser.Continue_statementContext):
        if Consultar(self.tree, "%loop") == None:
            Error("Continue statement fuera de un loop", ctx.start.line)
            return None
        return None


    # Visit a parse tree produced by Cmm2Parser#return_statement.
    def visitReturn_statement(self, ctx:Cmm2Parser.Return_statementContext):
        '''
        if ctx.comma_expression() == None:
            return symbol("value", "", "void", [], ctx.start.line)
        else:
            x = self.visit(ctx.comma_expression())
            x.line = ctx.start.line
            return x
        '''
        #siempre deberia estar definida en una funcion:
        vtype = Consultar(self.tree,"%return")
        if ctx.comma_expression() == None:
            if vtype != "void":
                Error("La funcion debe retornar un valor", ctx.start.line)
                return None
            return None
        
        exp = self.visit(ctx.comma_expression())
        if exp == None:
            return
        # si hay return, verifica que no sea void
        if vtype == "void" and exp.vtype != "void":
            Error("Una declaracion de funcion VOID no puede retornar valor",ctx.start.line)
            return None
        elif vtype[0] == "struct" and exp.vtype[0] == "struct":
            if vtype[1] != exp.vtype[1]:
                Error("La funcion  deberia retornar objetos de tipo struct " + vtype[1], ctx.start.line)
                return None
        elif vtype[0] == "struct":
            Error("La funcion deberia retornar objetos de tipo struct " + vtype[1], exp.line)
            return None
        elif exp.vtype[0] == "struct":
            Error("La funcion deberia retornar valores de tipo" + vtype, exp.line)
            return None
        return None

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


    # Visit a parse tree produced by Cmm2Parser#while_statement.
    def visitWhile_statement(self, ctx:Cmm2Parser.While_statementContext):
        self.tree = Initialize_scope(self.tree)
        self.tree.name["%loop"] = "while"
        expression = self.visit(ctx.comma_expression())
        block = self.visit(ctx.statement())
        self.tree = Finalize_scope(self.tree)
        return None

    # Visit a parse tree produced by Cmm2Parser#for_1.
    def visitFor_1(self, ctx:Cmm2Parser.For_1Context):
        if ctx.comma_expression() != None:
            return self.visit(ctx.comma_expression())
        if ctx.declare_statement() != None:
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
        self.tree.name["%loop"] = "for"
        if_init = self.visit(ctx.for_1())
        if_cond = self.visit(ctx.for_2())
        if_loop = self.visit(ctx.for_3())
        block = self.visit(ctx.statement())
        self.tree = Finalize_scope(self.tree)

    # Visit a parse tree produced by Cmm2Parser#do_statement.
    def visitDo_statement(self, ctx:Cmm2Parser.Do_statementContext):
        self.tree = Initialize_scope(self.tree)
        self.tree.name["%loop"] = "do"
        block = self.visit(ctx.statement(0))
        expression = self.visit(ctx.comma_expression())
        self.tree = Finalize_scope(self.tree)
        return None


    # Visit a parse tree produced by Cmm2Parser#function_call_expression.
    def visitFunction_call_expression(self, ctx:Cmm2Parser.Function_call_expressionContext):

        name = ctx.VAR().getText()
        args = []
        i = 0
        while ctx.expression(i) != None:
            args.append(self.visit(ctx.expression(i)))
            i += 1
        if not name in self.functions:
            Error("La funcion " + name +" no esta definida.", ctx.start.line)
            return None
        if len(args) != len(self.functions[name]) - 1:
            Error("La funcion requiere " + str(len(self.functions[name]) - 1) + " argumentos, y se otorgan " + str(len(args)), ctx.start.line)
            return None
        for i in range(len(args)):
            if args[i].vtype[0][0] == "struct" and self.functions[name][i][0][0] == "struct":
                if args[i].vtype[0][1] != self.functions[name][i][0][1]:
                    Error(name + " requiere un struct de tipo " + self.functions[name][i][0][1] + " y se otorga uno de tipo " + args[i].vtype[0][1], ctx.start.line)
                    return None
            elif args[i].vtype[0][0] == "struct" or self.functions[name][i][0][0] == "struct":
                Error(name + " requiere un argumento de tipo " + self.functions[name][i][0] + " y se otorga un struct " + args[i].vtype[0][1], ctx.start.line)
                return None




        return symbol("value", "", self.functions[name][0], [])


    # Visit a parse tree produced by Cmm2Parser#function_argument.
    def visitFunction_argument(self, ctx:Cmm2Parser.Function_argumentContext):
        vtype = self.visit(ctx.type_cmm())
        name = ctx.VAR().getText()
        if ctx.op != None:
            op = ctx.op.text
            if op[0] == '[': #array
                if vtype[0] == "struct":
                    vtype[0] = "struct[]"
                else:
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
        self.functions[name]=[vtype]
        for arg in args:
            self.functions[name].append([arg[0], arg[2]])
        
        if not name in self.tree.name:
            self.tree.name[name] = symbol('function', name, vtype, args, line)

        #inicializa el scope y agrega lo de adentro
        self.tree = Initialize_scope(self.tree)
        self.tree.name["%return"] = vtype

        #LLC
        codigo.append("define " + llc_vtype(vtype) + " @" + name + "(")
        count_args = 0
        for arg in args:
            self.tree.name[arg[1]] = symbol("variable", arg[1], arg[0], [], line)
            codigo.append(llc_vtype(arg[0]) + " %" + arg[1]  )
            count_args+=1
            if count_args < len(args):
                codigo.append(" ,")

        codigo.append(") #0 { \n")

        i = 0
        while ctx.statement(i) != None:
            statement = self.visit(ctx.statement(i))
            i += 1
        self.tree = Finalize_scope(self.tree)

        codigo.append("}")
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
        while ctx.declare_statement(i) != None:
            members.append(self.visit(ctx.declare_statement(i)))
            i += 1
        self.tree = Finalize_scope(self.tree)
        if Consultar(self.tree, name) == None:
            self.tree.name[name] = symbol('struct', name, "", members, line)
        self.where = 'global'
        self.structs[name] = dict()
        for mem in members:
            self.structs[name][mem.name] = mem.vtype
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
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.op.text
        if left is None or right is None :
            return None
       
        if left.stype != "variable":
            Error("Solo se puede asignar a variables", ctx.start.line)
            return None
        if right.vtype == "void" :
            Error("No se puede asignar a la variable, dado que la expresion no retorna ningun valor", ctx.start.line)
            return None
        if left.vtype[0] == "struct" and right.vtype[0] == "struct":
            if left.vtype[1] != right.vtype[1]:
                Error("Se intenta asignar a un objeto de tipo struct "+ left.vtype[1] + " un objeto de tipo struct " + right.vtype[1], ctx.start.line)
                return None
            else:
                if op != "=":
                    Error("La asignacion tinene una operacion no definida para structs", ctx.start.line)
                    return None
                else:
                    #asignar struct a struct
                    return symbol("variable", right.name, right.vtype, [])
        if op == "=":
            pass
        if op == "+=":
            pass
        if op == "-=":
            pass
        if op == "*=":
            pass
        if op == "/=":
            pass
        if op == "%=":
            pass
        if op == "<<=":
            pass
        if op == ">>=":
            pass
        if op == "&=":
            pass
        if op == "^=":
            pass
        if op == "|=":
            pass

        print("ASIGNANDO ", left.name, right.vtype)
        #%r2 = add i32 2, 0
        #store i32 %r2, i32* %x
        codigo.append("%r"+str(self.n_registro) + " = add " + llc_vtype(left.vtype) + " 99999, 0 \n" )
        codigo.append("store " + llc_vtype(left.vtype) + " %r" + str(self.n_registro) + ", " + llc_vtype(left.vtype) + "*" + "%" + left.name +" \n" )
        #n_registro+=1
        return symbol("variable", right.name, right.vtype, [])



    # Visit a parse tree produced by Cmm2Parser#expFunctionCall.
    def visitExpFunctionCall(self, ctx:Cmm2Parser.ExpFunctionCallContext):
        #print("FUNCION CALL", ctx.function_call_expression().VAR().getText() )
        #print("DATO: ", ctx.function_call_expression().expression(1))
        #return self.visitChildren(ctx)
        #return symbol("funcion_call", ctx.function_call_expression().VAR().getText() , self.structs[left.vtype[1]][name], [], 0)
        #def __init__(self, stype, name, vtype, info, line = 0):


        return self.visit(ctx.function_call_expression())

        #return symbol("funcion_call", ctx.function_call_expression().VAR().getText() , [] , [], 0)
        #return ctx.function_call_expression().VAR().getText()

    # Visit a parse tree produced by Cmm2Parser#expDot.
    def visitExpDot(self, ctx:Cmm2Parser.ExpDotContext):
        left = self.visit(ctx.expression())
        name = ctx.VAR().getText()
        line = ctx.start.line
        if left == None:
            return None
        if left.vtype[0] != "struct":
            Error(left.name + " no es una estructura.", line)
            return None
        if not name in self.structs[left.vtype[1]]:
            Error(name + " no es miembro de "+ left.vtype[1], line)
            return None
        
        return symbol("variable", left.name + "." + name, self.structs[left.vtype[1]][name], [], 0)


    # Visit a parse tree produced by Cmm2Parser#expTerOp.
    def visitExpTerOp(self, ctx:Cmm2Parser.ExpTerOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expArray.
    def visitExpArray(self, ctx:Cmm2Parser.ExpArrayContext):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left == None or right == None:
            return None
        if left.vtype[0] != "struct[]" or left.vtype[-1] != "]":
            Error("La expresion no corresponde a un array", ctx.start.line)
            return None
        if right.vtype[0] == "struct":
            Error("No se puede indexar con un struct", ctx.start.line)
            return None
        if left.vtype[0] == "struct[]":
            return symbol("variable", "", ["struct", left.vtype[1]], [])
        else:
            return symbol("variable", "", left.vtype[:-2], [])

    # Visit a parse tree produced by Cmm2Parser#expLeftUnary.
    def visitExpLeftUnary(self, ctx:Cmm2Parser.ExpLeftUnaryContext):
        exp = self.visit(ctx.expression())
        if exp == None:
            return None
        if exp.vtype[0] == "struct":
            Error("No se pueden realizar operaciones con un struct", ctx.start.line)
        if exp.vtype == "void":
            Error("No se puede operar ya que la expresion no retorna un valor", ctx.start.line)
        return symbol("value", "", exp.vtype, [])
        


    # Visit a parse tree produced by Cmm2Parser#expOp.
    def visitExpOp(self, ctx:Cmm2Parser.ExpOpContext):
        
        #left = self.tree.name[ctx.expression(0).VAR().getText()]
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        if left == None or right == None:
            return None

        op = ctx.op.text
        
        if str(left.vtype[0]) == "struct" or str(right.vtype[0]) == "struct":
            Error("No se pueden realizar operaciones con un struct", ctx.start.line)
            return None
        elif left.vtype == "void" or right.vtype == "void":
            Error("No se puede realizar la operacion, dado que la expresion no retorna ningun valor", ctx.start.line)
            return None
        

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
