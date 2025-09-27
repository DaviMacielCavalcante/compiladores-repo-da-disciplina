# Generated from PythonParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PythonParser import PythonParser
else:
    from PythonParser import PythonParser

# This class defines a complete generic visitor for a parse tree produced by PythonParser.

class PythonParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PythonParser#program.
    def visitProgram(self, ctx:PythonParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#statement.
    def visitStatement(self, ctx:PythonParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:PythonParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#printStatement.
    def visitPrintStatement(self, ctx:PythonParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#inputStatement.
    def visitInputStatement(self, ctx:PythonParser.InputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#ifStatement.
    def visitIfStatement(self, ctx:PythonParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#whileStatement.
    def visitWhileStatement(self, ctx:PythonParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#forStatement.
    def visitForStatement(self, ctx:PythonParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:PythonParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#breakStatement.
    def visitBreakStatement(self, ctx:PythonParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#continueStatement.
    def visitContinueStatement(self, ctx:PythonParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#defStatement.
    def visitDefStatement(self, ctx:PythonParser.DefStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#expressionStatement.
    def visitExpressionStatement(self, ctx:PythonParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#block.
    def visitBlock(self, ctx:PythonParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#Parenteses.
    def visitParenteses(self, ctx:PythonParser.ParentesesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#Variable.
    def visitVariable(self, ctx:PythonParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#comparison.
    def visitComparison(self, ctx:PythonParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#AddSub.
    def visitAddSub(self, ctx:PythonParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#MulDiv.
    def visitMulDiv(self, ctx:PythonParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#String.
    def visitString(self, ctx:PythonParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#ArrayLiteral.
    def visitArrayLiteral(self, ctx:PythonParser.ArrayLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#logical.
    def visitLogical(self, ctx:PythonParser.LogicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#ArrayAccess.
    def visitArrayAccess(self, ctx:PythonParser.ArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#Number.
    def visitNumber(self, ctx:PythonParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#BoolFalse.
    def visitBoolFalse(self, ctx:PythonParser.BoolFalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#bitwise.
    def visitBitwise(self, ctx:PythonParser.BitwiseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#pow.
    def visitPow(self, ctx:PythonParser.PowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#BoolTrue.
    def visitBoolTrue(self, ctx:PythonParser.BoolTrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#add_sub.
    def visitAdd_sub(self, ctx:PythonParser.Add_subContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#mul_div.
    def visitMul_div(self, ctx:PythonParser.Mul_divContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#pow_op.
    def visitPow_op(self, ctx:PythonParser.Pow_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#comparison_op.
    def visitComparison_op(self, ctx:PythonParser.Comparison_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#logical_op.
    def visitLogical_op(self, ctx:PythonParser.Logical_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonParser#bitwise_and_or.
    def visitBitwise_and_or(self, ctx:PythonParser.Bitwise_and_orContext):
        return self.visitChildren(ctx)



del PythonParser