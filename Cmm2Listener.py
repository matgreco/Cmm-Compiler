# Generated from Cmm2.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Cmm2Parser import Cmm2Parser
else:
    from Cmm2Parser import Cmm2Parser

# This class defines a complete listener for a parse tree produced by Cmm2Parser.
class Cmm2Listener(ParseTreeListener):

    # Enter a parse tree produced by Cmm2Parser#build.
    def enterBuild(self, ctx:Cmm2Parser.BuildContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#build.
    def exitBuild(self, ctx:Cmm2Parser.BuildContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#declare_statement.
    def enterDeclare_statement(self, ctx:Cmm2Parser.Declare_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#declare_statement.
    def exitDeclare_statement(self, ctx:Cmm2Parser.Declare_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#declare_normal.
    def enterDeclare_normal(self, ctx:Cmm2Parser.Declare_normalContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#declare_normal.
    def exitDeclare_normal(self, ctx:Cmm2Parser.Declare_normalContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#declare_array.
    def enterDeclare_array(self, ctx:Cmm2Parser.Declare_arrayContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#declare_array.
    def exitDeclare_array(self, ctx:Cmm2Parser.Declare_arrayContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#declare_assign_expression.
    def enterDeclare_assign_expression(self, ctx:Cmm2Parser.Declare_assign_expressionContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#declare_assign_expression.
    def exitDeclare_assign_expression(self, ctx:Cmm2Parser.Declare_assign_expressionContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#case_statement.
    def enterCase_statement(self, ctx:Cmm2Parser.Case_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#case_statement.
    def exitCase_statement(self, ctx:Cmm2Parser.Case_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#normal_statement.
    def enterNormal_statement(self, ctx:Cmm2Parser.Normal_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#normal_statement.
    def exitNormal_statement(self, ctx:Cmm2Parser.Normal_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#break_statement.
    def enterBreak_statement(self, ctx:Cmm2Parser.Break_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#break_statement.
    def exitBreak_statement(self, ctx:Cmm2Parser.Break_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#continue_statement.
    def enterContinue_statement(self, ctx:Cmm2Parser.Continue_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#continue_statement.
    def exitContinue_statement(self, ctx:Cmm2Parser.Continue_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#block_statement.
    def enterBlock_statement(self, ctx:Cmm2Parser.Block_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#block_statement.
    def exitBlock_statement(self, ctx:Cmm2Parser.Block_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#if_statement.
    def enterIf_statement(self, ctx:Cmm2Parser.If_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#if_statement.
    def exitIf_statement(self, ctx:Cmm2Parser.If_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#switch_statement.
    def enterSwitch_statement(self, ctx:Cmm2Parser.Switch_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#switch_statement.
    def exitSwitch_statement(self, ctx:Cmm2Parser.Switch_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#while_statement.
    def enterWhile_statement(self, ctx:Cmm2Parser.While_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#while_statement.
    def exitWhile_statement(self, ctx:Cmm2Parser.While_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#for_1.
    def enterFor_1(self, ctx:Cmm2Parser.For_1Context):
        pass

    # Exit a parse tree produced by Cmm2Parser#for_1.
    def exitFor_1(self, ctx:Cmm2Parser.For_1Context):
        pass


    # Enter a parse tree produced by Cmm2Parser#for_2.
    def enterFor_2(self, ctx:Cmm2Parser.For_2Context):
        pass

    # Exit a parse tree produced by Cmm2Parser#for_2.
    def exitFor_2(self, ctx:Cmm2Parser.For_2Context):
        pass


    # Enter a parse tree produced by Cmm2Parser#for_3.
    def enterFor_3(self, ctx:Cmm2Parser.For_3Context):
        pass

    # Exit a parse tree produced by Cmm2Parser#for_3.
    def exitFor_3(self, ctx:Cmm2Parser.For_3Context):
        pass


    # Enter a parse tree produced by Cmm2Parser#for_statement.
    def enterFor_statement(self, ctx:Cmm2Parser.For_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#for_statement.
    def exitFor_statement(self, ctx:Cmm2Parser.For_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#do_statement.
    def enterDo_statement(self, ctx:Cmm2Parser.Do_statementContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#do_statement.
    def exitDo_statement(self, ctx:Cmm2Parser.Do_statementContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#function_call_expression.
    def enterFunction_call_expression(self, ctx:Cmm2Parser.Function_call_expressionContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#function_call_expression.
    def exitFunction_call_expression(self, ctx:Cmm2Parser.Function_call_expressionContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#function_argument.
    def enterFunction_argument(self, ctx:Cmm2Parser.Function_argumentContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#function_argument.
    def exitFunction_argument(self, ctx:Cmm2Parser.Function_argumentContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#forward_function_argument.
    def enterForward_function_argument(self, ctx:Cmm2Parser.Forward_function_argumentContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#forward_function_argument.
    def exitForward_function_argument(self, ctx:Cmm2Parser.Forward_function_argumentContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#function_definition.
    def enterFunction_definition(self, ctx:Cmm2Parser.Function_definitionContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#function_definition.
    def exitFunction_definition(self, ctx:Cmm2Parser.Function_definitionContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#forward_function_definition.
    def enterForward_function_definition(self, ctx:Cmm2Parser.Forward_function_definitionContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#forward_function_definition.
    def exitForward_function_definition(self, ctx:Cmm2Parser.Forward_function_definitionContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#struct_definition.
    def enterStruct_definition(self, ctx:Cmm2Parser.Struct_definitionContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#struct_definition.
    def exitStruct_definition(self, ctx:Cmm2Parser.Struct_definitionContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#type_cmm.
    def enterType_cmm(self, ctx:Cmm2Parser.Type_cmmContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#type_cmm.
    def exitType_cmm(self, ctx:Cmm2Parser.Type_cmmContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#comma_expression.
    def enterComma_expression(self, ctx:Cmm2Parser.Comma_expressionContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#comma_expression.
    def exitComma_expression(self, ctx:Cmm2Parser.Comma_expressionContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expAssign.
    def enterExpAssign(self, ctx:Cmm2Parser.ExpAssignContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expAssign.
    def exitExpAssign(self, ctx:Cmm2Parser.ExpAssignContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expRightUnary.
    def enterExpRightUnary(self, ctx:Cmm2Parser.ExpRightUnaryContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expRightUnary.
    def exitExpRightUnary(self, ctx:Cmm2Parser.ExpRightUnaryContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expFunctionCall.
    def enterExpFunctionCall(self, ctx:Cmm2Parser.ExpFunctionCallContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expFunctionCall.
    def exitExpFunctionCall(self, ctx:Cmm2Parser.ExpFunctionCallContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expDot.
    def enterExpDot(self, ctx:Cmm2Parser.ExpDotContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expDot.
    def exitExpDot(self, ctx:Cmm2Parser.ExpDotContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expTerOp.
    def enterExpTerOp(self, ctx:Cmm2Parser.ExpTerOpContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expTerOp.
    def exitExpTerOp(self, ctx:Cmm2Parser.ExpTerOpContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expArray.
    def enterExpArray(self, ctx:Cmm2Parser.ExpArrayContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expArray.
    def exitExpArray(self, ctx:Cmm2Parser.ExpArrayContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expLeftUnary.
    def enterExpLeftUnary(self, ctx:Cmm2Parser.ExpLeftUnaryContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expLeftUnary.
    def exitExpLeftUnary(self, ctx:Cmm2Parser.ExpLeftUnaryContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expOp.
    def enterExpOp(self, ctx:Cmm2Parser.ExpOpContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expOp.
    def exitExpOp(self, ctx:Cmm2Parser.ExpOpContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expAtom.
    def enterExpAtom(self, ctx:Cmm2Parser.ExpAtomContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expAtom.
    def exitExpAtom(self, ctx:Cmm2Parser.ExpAtomContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expPar.
    def enterExpPar(self, ctx:Cmm2Parser.ExpParContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expPar.
    def exitExpPar(self, ctx:Cmm2Parser.ExpParContext):
        pass


    # Enter a parse tree produced by Cmm2Parser#expSizeof.
    def enterExpSizeof(self, ctx:Cmm2Parser.ExpSizeofContext):
        pass

    # Exit a parse tree produced by Cmm2Parser#expSizeof.
    def exitExpSizeof(self, ctx:Cmm2Parser.ExpSizeofContext):
        pass


