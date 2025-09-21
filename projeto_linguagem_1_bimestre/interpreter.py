from antlr4 import *
from PythonLexer import PythonLexer
from PythonParser import PythonParser
from PythonBaseVisitor import PythonBaseVisitor

class PythonInterpreter(PythonBaseVisitor):
    def __init__(self):
        self.variables = {}
    
    def visitProgram(self, ctx):
        for statement in ctx.statement():
            self.visit(statement)
    
    def visitAssignmentStatement(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.expression())
        self.variables[var_name] = value
        return value
    
    def visitPrintStatement(self, ctx):
        value = self.visit(ctx.expression())
        print(value)
        return value
    
    def visitIfStatement(self, ctx):
        condition = self.visit(ctx.expression())
        if condition:
            self.visit(ctx.block(0))  # Then block
        elif ctx.block(1):  # Else block exists
            self.visit(ctx.block(1))
    
    def visitWhileStatement(self, ctx):
        while self.visit(ctx.expression()):
            self.visit(ctx.block())
    
    def visitExpressionStatement(self, ctx):
        return self.visit(ctx.expression())
    
    def visitBlock(self, ctx):
        if ctx.statement():
            for statement in ctx.statement():
                self.visit(statement)
        else:
            self.visit(ctx.statement())
    
    def visitMulDiv(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        
        if op == '*':
            return left * right
        else:  # op == '/'
            return left / right
    
    def visitAddSub(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        
        if op == '+':
            return left + right
        else:  # op == '-'
            return left - right
    
    def visitComparison(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        
        if op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
    
    def visitParentheses(self, ctx):
        return self.visit(ctx.expression())
    
    def visitVariable(self, ctx):
        var_name = ctx.getText()
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise Exception(f"Variable '{var_name}' not defined")
    
    def visitNumber(self, ctx):
        value = ctx.getText()
        if '.' in value:
            return float(value)
        else:
            return int(value)
    
    def visitString(self, ctx):
        # Remove aspas
        return ctx.getText()[1:-1]
    
    def visitBoolTrue(self, ctx):
        return True
    
    def visitBoolFalse(self, ctx):
        return False

def main():
    # Exemplo de uso
    code = """
    x = 10
    y = 20
    z = x + y
    print(z)
    
    if (z > 25):
        print("z é maior que 25")
    else:
        print("z não é maior que 25")
    
    i = 0
    while (i < 3):
        print(i)
        i = i + 1
    """
    
    # Criar lexer e parser
    lexer = PythonLexer(InputStream(code))
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)
    
    # Gerar árvore sintática
    tree = parser.program()
    
    # Interpretar
    interpreter = PythonInterpreter()
    interpreter.visit(tree)

if __name__ == '__main__':
    main()