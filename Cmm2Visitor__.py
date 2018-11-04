# Generated from Cmm2.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Cmm2Parser import Cmm2Parser
else:
    from Cmm2Parser import Cmm2Parser

# This class defines a complete generic visitor for a parse tree produced by Cmm2Parser.

def Error(msg, line):
    print("Error en linea: "+str(line)+": " + str(msg))


def stoi(s:str):
    if s[0] == '\'':
        if len(s) != 3:
            Error("Caracter invalido: "+s)
            return 0
        else:
            return [ord(s[1]),'char']
    if s[-1] in ["ll","LL"]:
        s = s[:-2]
        base = 10
        if s[0:2] in ["0x","0X"]:
            s = s[2:]
            base = 16
        else if s[0] == "0":
            base = 8
        return [(int(s) & (2<<64 - 1)), 'long']
    else:
        base = 10
        if s[0:2] in ["0x","0X"]:
            s = s[2:]
            base = 16
        else if s[0] == "0":
            base = 8
        return [(int(s) & (2<<32 - 1)), 'int']



class symbol:
    def __init__(self, stype, name, value):
        self.stype = stype #function, struct, variable, value
        self.name = name #name
        self.value = value #information about symbol:
        #function: [return type, [arg1, opts], [arg2, opts], ...]
        #struct: [[member1, type], [member2, type], ...]
        #variable: [type]
        #value: [type]

    
class Cmm2Visitor(ParseTreeVisitor):

    def __init__(self):
        self.structs = []
        self.tree = Node(dict{})
        self.where = 'global' #'global', 'function', 'struct'

    # Visit a parse tree produced by Cmm2Parser#build.
    def visitBuild(self, ctx:Cmm2Parser.BuildContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#declare_statement.
    def visitDeclare_statement(self, ctx:Cmm2Parser.Declare_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#declare_normal.
    def visitDeclare_normal(self, ctx:Cmm2Parser.Declare_normalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#declare_array.
    def visitDeclare_array(self, ctx:Cmm2Parser.Declare_arrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#compare_op.
    def visitCompare_op(self, ctx:Cmm2Parser.Compare_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#assign_op.
    def visitAssign_op(self, ctx:Cmm2Parser.Assign_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#unary_left_op.
    def visitUnary_left_op(self, ctx:Cmm2Parser.Unary_left_opContext):
        return self.visitChildren(ctx)


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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#if_statement.
    def visitIf_statement(self, ctx:Cmm2Parser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#switch_statement.
    def visitSwitch_statement(self, ctx:Cmm2Parser.Switch_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#while_statement.
    def visitWhile_statement(self, ctx:Cmm2Parser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#for_statement.
    def visitFor_statement(self, ctx:Cmm2Parser.For_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#do_statement.
    def visitDo_statement(self, ctx:Cmm2Parser.Do_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#function_call_expression.
    def visitFunction_call_expression(self, ctx:Cmm2Parser.Function_call_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#function_argument.
    def visitFunction_argument(self, ctx:Cmm2Parser.Function_argumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#forward_function_argument.
    def visitForward_function_argument(self, ctx:Cmm2Parser.Forward_function_argumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#function_definition.
    def visitFunction_definition(self, ctx:Cmm2Parser.Function_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#forward_function_definition.
    def visitForward_function_definition(self, ctx:Cmm2Parser.Forward_function_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#struct_definition.
    def visitStruct_definition(self, ctx:Cmm2Parser.Struct_definitionContext):
        name = ctx.VAR().getText()
        if Consultar(self.tree, name) != None:
            line = ctx.start.getLine()
            Error(name + " ya esta definido",line)
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
        if Consultar(self.tree, name) != None:
            self.tree.name[name] = symbol('struct', name, members)
        self.where = 'global'
        return


    # Visit a parse tree produced by Cmm2Parser#comma_expression.
    def visitComma_expression(self, ctx:Cmm2Parser.Comma_expressionContext):
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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expAtom.
    def visitExpAtom(self, ctx:Cmm2Parser.ExpAtomContext):
        if ctx.VAR() != None:
            if Consultar(self.tree, ctx.VAR().getText()) == None:
                line = ctx.start.getLine()
                Error(ctx.VAR().getText() + " no esta definido", line)
                return None
            else:
                return ctx.VAR().getText()
        if ctx.INT_NUMBER() != None:
            val = stoi(INT_NUMBER().getText())
            return symbol('value', "", [val[1]])


    # Visit a parse tree produced by Cmm2Parser#expPar.
    def visitExpPar(self, ctx:Cmm2Parser.ExpParContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Cmm2Parser#expSizeof.
    def visitExpSizeof(self, ctx:Cmm2Parser.ExpSizeofContext):
        return self.visitChildren(ctx)



del Cmm2Parser