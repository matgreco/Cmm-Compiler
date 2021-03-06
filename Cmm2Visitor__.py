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

def isGlobal(scope, name):
    #print("Consultar")
    test_scope = scope
    while True :
        if name in test_scope.name:
            #print("OK, simbolo encontrado, valor: ", test_scope.name[name])
            return test_scope.is_root
        else:
            if test_scope.is_root == True:
                break
            test_scope = test_scope.parent

    if test_scope.is_root == True :
        #print("Simbolo no existe")
        return False

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
    if type[-1] == ']' or type == 'long':
        return 'i64'
    if type == 'void':
        return 'void'
    if type == 'float':
        return 'float'
    if type == 'double':
        return 'double'
    if type =='char' :
        return 'i8'
    if type == 'short':
        return 'i16'


def Error(msg, line):
    print("Error en linea "+str(line)+": " + str(msg))
    global error
    error = True


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
        return [(int(s,base) & ( (2<<64) - 1)), 'long']
    else:
        base = 10
        if s[0:2] in ["0x","0X"]:
            s = s[2:]
            base = 16
        elif s[0] == "0":
            base = 8
        return [(int(s,base) & ( (2<<32) - 1)), 'int']



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

    





error = False

codigo = list(' @.str = private unnamed_addr constant [4 x i8] c"%d\\0a\\00", align 1 \n')

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

    #devuelve prioridad entre dos tipos
    def type_priority(self, type1, type2):
        d = {"double":0, "float":1, "double[]":2, "float[]":3, "long[]":4, "int[]":5, "short[]":6, "char[]":7, "struct[]":8, "long":9, "int":10, "short":11, "char":12}
        invd = ["double", "float", "double[]", "float[]", "long[]", "int[]", "short[]", "char[]", "struct[]", "long", "int", "short", "char"]
        if type1 in d and type2 in d:
            return invd[min(d[type1],d[type2])]
        else:
            print("Error de casteo")

    #genera el codigo de casteo de type1 a type2
    def cast(self, type1, varname, type2, line = 0):
        llc_t1 = llc_vtype(type1)
        llc_t2 = llc_vtype(type2)
        if llc_t1 == llc_t2:
            return varname
        if llc_t1[0] == 'i' and llc_t2[0] == 'i': #ambos son enteros
            if int(llc_t1[1:]) < int(llc_t2[1:]):
                self.n_registro += 1
                codigo.append("%.r"+str(self.n_registro) + " = sext " + llc_t1 + " " + varname + " to " + llc_t2 + " \n")
                return "%.r" + str(self.n_registro)
            else:
                self.n_registro += 1
                codigo.append("%.r" + str(self.n_registro) + " = trunc " + llc_t1 + " " + varname + " to " + llc_t2 + " \n")
                return "%.r" + str(self.n_registro)
        elif llc_t1[0] == "i" and llc_t2 in ["float", "double"]:
            self.n_registro += 1
            codigo.append("%.r" + str(self.n_registro) + " = sitofp " + llc_t1 + " " + varname + " to " + llc_t2 + " \n")
            return "%.r" + str(self.n_registro)
        elif llc_t1 in ["float", "double"] and llc_t2[0] == "i":
            self.n_registro += 1
            codigo.append("%.r" + str(self.n_registro) + " = fptosi " + llc_t1 + " " + varname + " to " + llc_t2 + " \n")
            return "%.r" + str(self.n_registro)
        elif llc_t1 == "float" and llc_t2 == "double":
            self.n_registro += 1
            codigo.append("%.r" + str(self.n_registro) + " = fpext float " + varname + " to double"  + " \n")
            return "%.r" + str(self.n_registro)
        elif llc_t1 == "double" and llc_t2 == "float":
            self.n_registro += 1
            codigo.append("%.r" + str(self.n_registro) + " = fptrunc double " + varname + " to float" + " \n")
            return "%.r" + str(self.n_registro)
        else:
            Error("Error de casteo", line)
        
        
    def binop(self, type, var1, var2, op, line):
        iop = {"+":"add", "-":"sub", "*":"mul", "/":"sdiv", "%":"srem", "<<":"shl", ">>": "ashr", "&": "and", "|": "or", "^": "xor"}
        fop = {"+":"fadd", "-":"fsub", "*":"fmul", "/":"fdiv", "%":"frem"}
        icmp = {"==":"icmp eq", "!=":"icmp ne", "<":"icmp slt", "<=":"icmp sle", ">": "icmp sgt", ">=": "icmp sge"}
        fcmp = {"==":"fcmp eq", "!=":"fcmp ne", "<":"fcmp slt", "<=":"fcmp sle", ">": "fcmp sgt", ">=": "fcmp sge"}
        lop = {"&&": "and", "||": "or"}
        if type in ["i8", "i16", "i32", "i64"]:
            if op in iop:
                self.n_registro += 1
                newvar = "%.r" + str(self.n_registro)
                codigo.append(newvar + " = " + iop[op] + " " + type + " " + var1 + " , " + var2 + " \n")
                return
            elif op in icmp:
                temp = "%.r" + str(self.n_registro + 1)
                newvar = "%.r" + str(self.n_registro + 2)
                self.n_registro += 2
                codigo.append(temp + " = " + icmp[op] + " " + type + " " + var1 + " , " + var2 + " \n")
                codigo.append(newvar + " = zext i1 " + temp + " to i32"  + " \n")
                return
            elif op in lop:
                s1 = "{0} = icmp eq {1} {2} , 0"
                s2 = "{0} = {1} i1 {2} , {3}"
                s3 = "{0} = zext i1 {1} to i32"
                temp1 = "%.r" + str(self.n_registro + 1)
                temp2 = "%.r" + str(self.n_registro + 2)
                temp3 = "%.r" + str(self.n_registro + 3)
                newvar = "%.r" + str(self.n_registro + 4)
                self.n_registro += 4
                codigo.append(s1.format(temp1,type,var1))
                codigo.append(s1.format(temp2,type,var2))
                codigo.append(s2.format(temp3,lop[op],temp1,temp2))
                codigo.append(s3.format(newvar,temp3))
                return
            else:
                Error("Error de operacion",line)
        elif type in ["float", "double"]:
            if op in fop:
                self.n_registro += 1
                newvar = "%.r" + str(self.n_registro)
                codigo.append(newvar + " = " + fop[op] + " " + type + " " + var1 + " , " + var2  + " \n")
                return
            elif op in fcmp:
                temp = "%.r" + str(self.n_registro + 1)
                newvar = "%.r" + str(self.n_registro + 2)
                self.n_registro += 2
                codigo.append(temp + " = " + fcmp[op] + " " + type + " " + var1 + " , " + var2  + " \n")
                codigo.append(newvar + " = zext i1 " + temp + " to i32")
                return
            else:
                Error("No se puede realizar la operacion "+ op + " con numeros no enteros", line)
        else:
            Error("No se puede realizar la operacion " + op +" con valores no enteros",line)




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
            if self.tree.is_root:
                codigo.append("@" + name + " = global " + llc_vtype(vtype) + " \n")
            else:
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
        temp = "%.r" + str(self.n_registro)

        #valor_asignacion = 2222 #ESTO DEBE SER EL VALOR ASIGNADO - CAMBIAR
        codigo.append("%" + name + " = alloca " + llc_vtype(vtype) + " \n")
        temp = self.cast(val.vtype, temp, vtype, ctx.start.line)
        codigo.append("store " + llc_vtype(vtype) + " " + temp + " , " + llc_vtype(vtype) + "* %" + name)
        #codigo.append("%r" + str(self.n_registro) + " = add " + llc_vtype(vtype) + " " + str(valor_asignacion) + ", 0" + " \n")
        #codigo.append("store "+ llc_vtype(vtype) + " " + "%r" + str(self.n_registro) + ", " + llc_vtype(vtype) + "* %" + name + " \n")
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
        
        codigo.append("ret i32 %.r"+ str(self.n_registro) +" \n")
        self.n_registro+=1
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


        if(name == 'print'):
            codigo.append("%.r" + str(self.n_registro+1) + " = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i32 0, i32 0), i32 %.r" + str(self.n_registro) + ") \n"  )
            self.n_registro += 1


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

        codigo.append("} \n")
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
        var2 = "%.r" + str(self.n_registro)
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
        if isGlobal(self.tree, left.name):
            avar = "@" + left.name
        else:
            avar = "%" + left.name

        if op != "=":
            preop = op[:-1]
            newtype = self.type_priority(left.vtype, right.vtype)
            if newtype == left.vtype:
                var2 = self.cast(right.vtype,var2, newtype, ctx.start.line)
            else:
                avar = self.cast(left.vtype,avar, newtype, ctx.start.line)

            llc_type = llc_vtype(newtype)
            tempavar = "%.r" + str(self.n_registro +1)
            self.n_registro += 1
            codigo.append(tempavar + " = load " + llc_type + " , " + llc_type + "* " + avar + "\n")
            self.binop(llc_type, tempavar, var2, preop, ctx.start.line)
            temp = "%.r" + str(self.n_registro)
            temp = self.cast(newtype, temp, left.vtype, ctx.start.line)
            codigo.append("store " + llc_type + " " + temp + " , " + llc_type + "* " + avar + "\n")
        else:
            llc_type = llc_vtype(left.vtype)
            #print(llc_vtype(left.vtype), llc_vtype(right.vtype))
            var2 = self.cast(right.vtype, var2, left.vtype, ctx.start.line)
            #print("?????????????????????????",llc_type, var2, avar)
            codigo.append("store "+ llc_type + " " + var2 + " , " + llc_type + "* " + avar + "\n")


        #print("ASIGNANDO ", left.name, right.vtype)
        #%r2 = add i32 2, 0
        #store i32 %r2, i32* %x
        #print(vars(right))
        #codigo.append("%.r"+str(self.n_registro) + " = add " + llc_vtype(left.vtype) + " 99999, 0 \n" )
        #codigo.append("store " + llc_vtype(left.vtype) + " %.r" + str(self.n_registro) + ", " + llc_vtype(left.vtype) + "*" + "%" + left.name +" \n" )
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
        var1 = "%.r" + str(self.n_registro)
        right = self.visit(ctx.expression(1))
        var2 = "%.r" + str(self.n_registro)

        if left == None or right == None:
            return None

        op = ctx.op.text
        
        if str(left.vtype[0]) == "struct" or str(right.vtype[0]) == "struct":
            Error("No se pueden realizar operaciones con un struct", ctx.start.line)
            return None
        elif left.vtype == "void" or right.vtype == "void":
            Error("No se puede realizar la operacion, dado que la expresion no retorna ningun valor", ctx.start.line)
            return None
        
        newtype = self.type_priority(left.vtype, right.vtype)
        if newtype == left.vtype:
            var2 = self.cast(right.vtype,var2, newtype, ctx.start.line)
        else:
            var1 = self.cast(left.vtype,var1, newtype, ctx.start.line)

        llc_type = llc_vtype(newtype)

        self.binop(llc_type, var1, var2, op, ctx.start.line)
        if op in ["==", "!=", "<", "<=", ">", ">=", "||", "&&"]:
            return symbol("value","", "int", [])
        else:
            return symbol("value","", newtype, [])

        #type1 = left.stype
        #type2 = right.stype
        #return symbol(left.stype,"", left.vtype,list(left.stype))


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
                self.n_registro += 1
                newvar = "%.r" + str(self.n_registro)
                if isGlobal(self.tree, x.name):
                    vname = "@" + x.name
                else:
                    vname = "%" + x.name
                codigo.append(newvar + " = load " + llc_vtype(x.vtype) + " , " + llc_vtype(x.vtype) + "* " + vname + "\n")
                return x
        if ctx.INT_NUMBER() != None:
            val = stoi(ctx.INT_NUMBER().getText())
            newvar = "%.r" + str(self.n_registro + 1)
            self.n_registro += 1
            codigo.append(newvar + " = add " + llc_vtype(val[1]) + " " + str(val[0]) + " , 0\n")
            #codigo.append("store " + llc_vtype(val[1]) + " " + str(val[0]) + " , " + llc_vtype(val[1]) + "* " + newvar + "\n")
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
