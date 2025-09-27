# Generated from PythonParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PythonParser import PythonParser
else:
    from PythonParser import PythonParser

# This class defines a complete listener for a parse tree produced by PythonParser.
class PythonParserListener(ParseTreeListener):

    # Enter a parse tree produced by PythonParser#program.
    def enterProgram(self, ctx:PythonParser.ProgramContext):
        pass

    # Exit a parse tree produced by PythonParser#program.
    def exitProgram(self, ctx:PythonParser.ProgramContext):
        pass


    # Enter a parse tree produced by PythonParser#statement.
    def enterStatement(self, ctx:PythonParser.StatementContext):
        pass

    # Exit a parse tree produced by PythonParser#statement.
    def exitStatement(self, ctx:PythonParser.StatementContext):
        pass


    # Enter a parse tree produced by PythonParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:PythonParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:PythonParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#printStatement.
    def enterPrintStatement(self, ctx:PythonParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#printStatement.
    def exitPrintStatement(self, ctx:PythonParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#inputStatement.
    def enterInputStatement(self, ctx:PythonParser.InputStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#inputStatement.
    def exitInputStatement(self, ctx:PythonParser.InputStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#ifStatement.
    def enterIfStatement(self, ctx:PythonParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#ifStatement.
    def exitIfStatement(self, ctx:PythonParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#whileStatement.
    def enterWhileStatement(self, ctx:PythonParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#whileStatement.
    def exitWhileStatement(self, ctx:PythonParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#forStatement.
    def enterForStatement(self, ctx:PythonParser.ForStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#forStatement.
    def exitForStatement(self, ctx:PythonParser.ForStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#doWhileStatement.
    def enterDoWhileStatement(self, ctx:PythonParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#doWhileStatement.
    def exitDoWhileStatement(self, ctx:PythonParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#breakStatement.
    def enterBreakStatement(self, ctx:PythonParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#breakStatement.
    def exitBreakStatement(self, ctx:PythonParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#continueStatement.
    def enterContinueStatement(self, ctx:PythonParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#continueStatement.
    def exitContinueStatement(self, ctx:PythonParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#defStatement.
    def enterDefStatement(self, ctx:PythonParser.DefStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#defStatement.
    def exitDefStatement(self, ctx:PythonParser.DefStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#expressionStatement.
    def enterExpressionStatement(self, ctx:PythonParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by PythonParser#expressionStatement.
    def exitExpressionStatement(self, ctx:PythonParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by PythonParser#block.
    def enterBlock(self, ctx:PythonParser.BlockContext):
        pass

    # Exit a parse tree produced by PythonParser#block.
    def exitBlock(self, ctx:PythonParser.BlockContext):
        pass


    # Enter a parse tree produced by PythonParser#Parenteses.
    def enterParenteses(self, ctx:PythonParser.ParentesesContext):
        pass

    # Exit a parse tree produced by PythonParser#Parenteses.
    def exitParenteses(self, ctx:PythonParser.ParentesesContext):
        pass


    # Enter a parse tree produced by PythonParser#Variable.
    def enterVariable(self, ctx:PythonParser.VariableContext):
        pass

    # Exit a parse tree produced by PythonParser#Variable.
    def exitVariable(self, ctx:PythonParser.VariableContext):
        pass


    # Enter a parse tree produced by PythonParser#comparison.
    def enterComparison(self, ctx:PythonParser.ComparisonContext):
        pass

    # Exit a parse tree produced by PythonParser#comparison.
    def exitComparison(self, ctx:PythonParser.ComparisonContext):
        pass


    # Enter a parse tree produced by PythonParser#AddSub.
    def enterAddSub(self, ctx:PythonParser.AddSubContext):
        pass

    # Exit a parse tree produced by PythonParser#AddSub.
    def exitAddSub(self, ctx:PythonParser.AddSubContext):
        pass


    # Enter a parse tree produced by PythonParser#MulDiv.
    def enterMulDiv(self, ctx:PythonParser.MulDivContext):
        pass

    # Exit a parse tree produced by PythonParser#MulDiv.
    def exitMulDiv(self, ctx:PythonParser.MulDivContext):
        pass


    # Enter a parse tree produced by PythonParser#String.
    def enterString(self, ctx:PythonParser.StringContext):
        pass

    # Exit a parse tree produced by PythonParser#String.
    def exitString(self, ctx:PythonParser.StringContext):
        pass


    # Enter a parse tree produced by PythonParser#ArrayLiteral.
    def enterArrayLiteral(self, ctx:PythonParser.ArrayLiteralContext):
        pass

    # Exit a parse tree produced by PythonParser#ArrayLiteral.
    def exitArrayLiteral(self, ctx:PythonParser.ArrayLiteralContext):
        pass


    # Enter a parse tree produced by PythonParser#logical.
    def enterLogical(self, ctx:PythonParser.LogicalContext):
        pass

    # Exit a parse tree produced by PythonParser#logical.
    def exitLogical(self, ctx:PythonParser.LogicalContext):
        pass


    # Enter a parse tree produced by PythonParser#ArrayAccess.
    def enterArrayAccess(self, ctx:PythonParser.ArrayAccessContext):
        pass

    # Exit a parse tree produced by PythonParser#ArrayAccess.
    def exitArrayAccess(self, ctx:PythonParser.ArrayAccessContext):
        pass


    # Enter a parse tree produced by PythonParser#Number.
    def enterNumber(self, ctx:PythonParser.NumberContext):
        pass

    # Exit a parse tree produced by PythonParser#Number.
    def exitNumber(self, ctx:PythonParser.NumberContext):
        pass


    # Enter a parse tree produced by PythonParser#BoolFalse.
    def enterBoolFalse(self, ctx:PythonParser.BoolFalseContext):
        pass

    # Exit a parse tree produced by PythonParser#BoolFalse.
    def exitBoolFalse(self, ctx:PythonParser.BoolFalseContext):
        pass


    # Enter a parse tree produced by PythonParser#bitwise.
    def enterBitwise(self, ctx:PythonParser.BitwiseContext):
        pass

    # Exit a parse tree produced by PythonParser#bitwise.
    def exitBitwise(self, ctx:PythonParser.BitwiseContext):
        pass


    # Enter a parse tree produced by PythonParser#pow.
    def enterPow(self, ctx:PythonParser.PowContext):
        pass

    # Exit a parse tree produced by PythonParser#pow.
    def exitPow(self, ctx:PythonParser.PowContext):
        pass


    # Enter a parse tree produced by PythonParser#BoolTrue.
    def enterBoolTrue(self, ctx:PythonParser.BoolTrueContext):
        pass

    # Exit a parse tree produced by PythonParser#BoolTrue.
    def exitBoolTrue(self, ctx:PythonParser.BoolTrueContext):
        pass


    # Enter a parse tree produced by PythonParser#add_sub.
    def enterAdd_sub(self, ctx:PythonParser.Add_subContext):
        pass

    # Exit a parse tree produced by PythonParser#add_sub.
    def exitAdd_sub(self, ctx:PythonParser.Add_subContext):
        pass


    # Enter a parse tree produced by PythonParser#mul_div.
    def enterMul_div(self, ctx:PythonParser.Mul_divContext):
        pass

    # Exit a parse tree produced by PythonParser#mul_div.
    def exitMul_div(self, ctx:PythonParser.Mul_divContext):
        pass


    # Enter a parse tree produced by PythonParser#pow_op.
    def enterPow_op(self, ctx:PythonParser.Pow_opContext):
        pass

    # Exit a parse tree produced by PythonParser#pow_op.
    def exitPow_op(self, ctx:PythonParser.Pow_opContext):
        pass


    # Enter a parse tree produced by PythonParser#comparison_op.
    def enterComparison_op(self, ctx:PythonParser.Comparison_opContext):
        pass

    # Exit a parse tree produced by PythonParser#comparison_op.
    def exitComparison_op(self, ctx:PythonParser.Comparison_opContext):
        pass


    # Enter a parse tree produced by PythonParser#logical_op.
    def enterLogical_op(self, ctx:PythonParser.Logical_opContext):
        pass

    # Exit a parse tree produced by PythonParser#logical_op.
    def exitLogical_op(self, ctx:PythonParser.Logical_opContext):
        pass


    # Enter a parse tree produced by PythonParser#bitwise_and_or.
    def enterBitwise_and_or(self, ctx:PythonParser.Bitwise_and_orContext):
        pass

    # Exit a parse tree produced by PythonParser#bitwise_and_or.
    def exitBitwise_and_or(self, ctx:PythonParser.Bitwise_and_orContext):
        pass



del PythonParser