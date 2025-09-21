# Generated from Python.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PythonParser import PythonParser
else:
    from PythonParser import PythonParser

# This class defines a complete listener for a parse tree produced by PythonParser.
class PythonListener(ParseTreeListener):

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


    # Enter a parse tree produced by PythonParser#Variable.
    def enterVariable(self, ctx:PythonParser.VariableContext):
        pass

    # Exit a parse tree produced by PythonParser#Variable.
    def exitVariable(self, ctx:PythonParser.VariableContext):
        pass


    # Enter a parse tree produced by PythonParser#Number.
    def enterNumber(self, ctx:PythonParser.NumberContext):
        pass

    # Exit a parse tree produced by PythonParser#Number.
    def exitNumber(self, ctx:PythonParser.NumberContext):
        pass


    # Enter a parse tree produced by PythonParser#MulDiv.
    def enterMulDiv(self, ctx:PythonParser.MulDivContext):
        pass

    # Exit a parse tree produced by PythonParser#MulDiv.
    def exitMulDiv(self, ctx:PythonParser.MulDivContext):
        pass


    # Enter a parse tree produced by PythonParser#AddSub.
    def enterAddSub(self, ctx:PythonParser.AddSubContext):
        pass

    # Exit a parse tree produced by PythonParser#AddSub.
    def exitAddSub(self, ctx:PythonParser.AddSubContext):
        pass


    # Enter a parse tree produced by PythonParser#Comparison.
    def enterComparison(self, ctx:PythonParser.ComparisonContext):
        pass

    # Exit a parse tree produced by PythonParser#Comparison.
    def exitComparison(self, ctx:PythonParser.ComparisonContext):
        pass


    # Enter a parse tree produced by PythonParser#BoolFalse.
    def enterBoolFalse(self, ctx:PythonParser.BoolFalseContext):
        pass

    # Exit a parse tree produced by PythonParser#BoolFalse.
    def exitBoolFalse(self, ctx:PythonParser.BoolFalseContext):
        pass


    # Enter a parse tree produced by PythonParser#String.
    def enterString(self, ctx:PythonParser.StringContext):
        pass

    # Exit a parse tree produced by PythonParser#String.
    def exitString(self, ctx:PythonParser.StringContext):
        pass


    # Enter a parse tree produced by PythonParser#BoolTrue.
    def enterBoolTrue(self, ctx:PythonParser.BoolTrueContext):
        pass

    # Exit a parse tree produced by PythonParser#BoolTrue.
    def exitBoolTrue(self, ctx:PythonParser.BoolTrueContext):
        pass


    # Enter a parse tree produced by PythonParser#Parentheses.
    def enterParentheses(self, ctx:PythonParser.ParenthesesContext):
        pass

    # Exit a parse tree produced by PythonParser#Parentheses.
    def exitParentheses(self, ctx:PythonParser.ParenthesesContext):
        pass



del PythonParser