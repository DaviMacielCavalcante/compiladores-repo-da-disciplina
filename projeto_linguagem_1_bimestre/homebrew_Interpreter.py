#!/usr/bin/env python3

import sys
import os
from antlr4 import *
from PythonLexer import PythonLexer
from PythonParser import PythonParser
from PythonParserVisitor import PythonParserVisitor

class PythonInterpreter(PythonParserVisitor):
    def __init__(self):
        self.variables = {}
        self.break_flag = False
        self.continue_flag = False
    
    def visitProgram(self, ctx):
        for statement in ctx.statement():
            self.visit(statement)
    
    def visitAssignmentStatement(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.expression()[-1])  # Último expression é o valor
        
        # Verificar se é atribuição a array
        if ctx.LBRACKET():
            # Atribuição a elemento do array: arr[0] = 5 ou matriz[0][1] = 10
            indices = []
            for i in range(len(ctx.expression()) - 1):  # Todos exceto o último
                indices.append(self.visit(ctx.expression()[i]))
            
            # Pegar o array
            if var_name not in self.variables:
                raise Exception(f"Array '{var_name}' não definido")
            
            arr = self.variables[var_name]
            
            # Navegar pelos índices (suporta múltiplas dimensões)
            for idx in indices[:-1]:
                arr = arr[int(idx)]
            
            # Atribuir valor no último índice
            arr[int(indices[-1])] = value
        else:
            # Atribuição simples
            self.variables[var_name] = value
        
        return value
    
    def visitPrintStatement(self, ctx):
        expressions = ctx.expression()
        values = []
        
        for expr in expressions:
            value = self.visit(expr)
            values.append(str(value))
        
        print(' '.join(values))
        return values
    
    def visitInputStatement(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        
        # Pegar mensagem opcional
        message = ""
        if ctx.STRING():
            message = ctx.STRING().getText()[1:-1]
        
        # Ler entrada do usuário
        if message:
            user_input = input(message)
        else:
            user_input = input()
        
        # Tentar converter para número
        try:
            value = int(user_input)
        except ValueError:
            try:
                value = float(user_input)
            except ValueError:
                value = user_input
        
        self.variables[var_name] = value
        return value
    
    def visitIfStatement(self, ctx):
        condition = self.visit(ctx.expression())
        if condition:
            self.visit(ctx.block(0))
        elif ctx.block(1):
            self.visit(ctx.block(1))
    
    def visitWhileStatement(self, ctx):
        self.break_flag = False
        self.continue_flag = False
        
        while self.visit(ctx.expression()) and not self.break_flag:
            self.continue_flag = False
            self.visit(ctx.block())
            
        self.break_flag = False
        self.continue_flag = False
    
    def visitForStatement(self, ctx):
        self.break_flag = False
        self.continue_flag = False
        
        var_name = ctx.IDENTIFIER().getText()
        expressions = ctx.expression()
        
        if len(expressions) == 1:
            start = 0
            end = self.visit(expressions[0])
            step = 1
        elif len(expressions) == 2:
            start = self.visit(expressions[0])
            end = self.visit(expressions[1])
            step = 1
        elif len(expressions) == 3:
            start = self.visit(expressions[0])
            end = self.visit(expressions[1])
            step = self.visit(expressions[2])
        else:
            raise Exception("Range deve ter 1, 2 ou 3 parâmetros")
        
        current = start
        while (step > 0 and current < end) or (step < 0 and current > end):
            if self.break_flag:
                break
            
            self.variables[var_name] = current
            self.continue_flag = False
            self.visit(ctx.block())
            current += step
        
        self.break_flag = False
        self.continue_flag = False
    
    def visitDoWhileStatement(self, ctx):
        self.break_flag = False
        self.continue_flag = False
        
        self.continue_flag = False
        self.visit(ctx.block())
        
        while self.visit(ctx.expression()) and not self.break_flag:
            self.continue_flag = False
            self.visit(ctx.block())
            
        self.break_flag = False
        self.continue_flag = False
    
    def visitBreakStatement(self, ctx):
        self.break_flag = True
        return None
    
    def visitContinueStatement(self, ctx):
        self.continue_flag = True
        return None
    
    def visitExpressionStatement(self, ctx):
        return self.visit(ctx.expression())
    
    def visitBlock(self, ctx):
        if ctx.statement() and len(ctx.statement()) > 0:
            for statement in ctx.statement():
                self.visit(statement)
                if self.break_flag or self.continue_flag:
                    break
        elif ctx.statement() and len(ctx.statement()) == 0:
            pass
        else:
            self.visit(ctx.statement())
    
    def visitPow(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        return left ** right
    
    def visitMulDiv(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.mul_div().getText()
        
        if op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '%':
            return left % right
    
    def visitAddSub(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.add_sub().getText()
        
        if op == '+':
            return left + right
        else:
            return left - right
    
    def visitComparison(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.comparison_op().getText()
        
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
    
    def visitBitwise(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.bitwise_and_or().getText()
        
        if op == '&':
            return left & right
        elif op == '|':
            return left | right
    
    def visitLogical(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.logical_op().getText()
        
        if op == 'and':
            return left and right
        elif op == 'or':
            return left or right
        elif op == 'not':
            return not right
    
    def visitParentheses(self, ctx):
        return self.visit(ctx.expression())
    
    def visitArrayAccess(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        
        if var_name not in self.variables:
            raise Exception(f"Array '{var_name}' não definido")
        
        arr = self.variables[var_name]
        
        # Processar cada índice
        for expr in ctx.expression():
            idx = int(self.visit(expr))
            arr = arr[idx]
        
        return arr
    
    def visitArrayLiteral(self, ctx):
        elements = []
        if ctx.expression():
            for expr in ctx.expression():
                elements.append(self.visit(expr))
        return elements
    
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
        return ctx.getText()[1:-1]
    
    def visitBoolTrue(self, ctx):
        return True
    
    def visitBoolFalse(self, ctx):
        return False

def run_script(filename):
    if not os.path.exists(filename):
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return False
    
    try:
        lexer = PythonLexer(InputStream(code))
        stream = CommonTokenStream(lexer)
        parser = PythonParser(stream)
        tree = parser.program()
        
        if parser.getNumberOfSyntaxErrors() > 0:
            print(f"ERRO DE SINTAXE em '{filename}'")
            return False
        
        interpreter = PythonInterpreter()
        interpreter.visit(tree)
        return True
        
    except Exception as e:
        print(f"ERRO DE EXECUÇÃO em '{filename}': {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python homebrew_Interpreter.py <arquivo.py>")
        return
    
    filename = sys.argv[1]
    print(f"Executando '{filename}':")
    print("-" * 40)
    
    success = run_script(filename)
    
    print("-" * 40)
    if success:
        print("Execução concluída com sucesso.")
    else:
        print("Execução falhou.")

if __name__ == '__main__':
    main()