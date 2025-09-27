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
        self.break_flag = False     # Flag para controlar break
        self.continue_flag = False  # Flag para controlar continue
    
    def visitProgram(self, ctx):
        for statement in ctx.statement():
            self.visit(statement)
    
    def visitAssignmentStatement(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.expression())
        self.variables[var_name] = value
        return value
    
    def visitPrintStatement(self, ctx):
        # Pegar todas as expressões separadas por vírgula
        expressions = ctx.expression()
        values = []
        
        # Avaliar cada expressão
        for expr in expressions:
            value = self.visit(expr)
            values.append(str(value))
        
        # Imprimir valores separados por espaço (como Python real)
        print(' '.join(values))
        return values
    
    def visitIfStatement(self, ctx):
        condition = self.visit(ctx.expression())
        if condition:
            self.visit(ctx.block(0))
        elif ctx.block(1):
            self.visit(ctx.block(1))
    
    def visitWhileStatement(self, ctx):
        self.break_flag = False     # Reset flags
        self.continue_flag = False
        
        while self.visit(ctx.expression()) and not self.break_flag:
            self.continue_flag = False  # Reset continue flag a cada iteração
            self.visit(ctx.block())
            # Continue faz pular para próxima iteração, não sair do loop
            
        self.break_flag = False     # Reset após sair do loop
        self.continue_flag = False
    
    def visitForStatement(self, ctx):
        self.break_flag = False     # Reset flags
        self.continue_flag = False
        
        # Pegar nome da variável do loop
        var_name = ctx.IDENTIFIER().getText()
        
        # Pegar parâmetros do range
        expressions = ctx.expression()
        
        if len(expressions) == 1:
            # range(end)
            start = 0
            end = self.visit(expressions[0])
            step = 1
        elif len(expressions) == 2:
            # range(start, end)
            start = self.visit(expressions[0])
            end = self.visit(expressions[1])
            step = 1
        elif len(expressions) == 3:
            # range(start, end, step)
            start = self.visit(expressions[0])
            end = self.visit(expressions[1])
            step = self.visit(expressions[2])
        else:
            raise Exception("Range deve ter 1, 2 ou 3 parâmetros")
        
        # Executar o loop
        current = start
        while (step > 0 and current < end) or (step < 0 and current > end):
            if self.break_flag:
                break
            
            # Definir variável do loop
            self.variables[var_name] = current
            
            # Reset continue flag a cada iteração
            self.continue_flag = False
            
            # Executar bloco
            self.visit(ctx.block())
            
            # Se continue foi executado, pular para próxima iteração
            # (não precisa fazer nada especial, só incrementar)
            
            # Incrementar
            current += step
        
        self.break_flag = False     # Reset após sair do loop
        self.continue_flag = False
    
    def visitDoWhileStatement(self, ctx):
        self.break_flag = False     # Reset flags
        self.continue_flag = False
        
        # Do-while executa pelo menos uma vez
        self.continue_flag = False
        self.visit(ctx.block())
        
        while self.visit(ctx.expression()) and not self.break_flag:
            self.continue_flag = False  # Reset continue flag a cada iteração
            self.visit(ctx.block())
            
        self.break_flag = False     # Reset após sair do loop
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
        # Verificar se há statements no bloco
        if ctx.statement() and len(ctx.statement()) > 0:
            for statement in ctx.statement():
                self.visit(statement)
                # Se break ou continue foi executado, parar de executar statements
                if self.break_flag or self.continue_flag:
                    break
        elif ctx.statement() and len(ctx.statement()) == 0:
            # Bloco vazio entre chaves - não faz nada
            pass
        else:
            # Statement único (sem chaves)
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
        return ctx.getText()[1:-1]  # Remove aspas
    
    def visitBoolTrue(self, ctx):
        return True
    
    def visitBoolFalse(self, ctx):
        return False

def run_script(filename):
    """Executa um script do Python primitivo"""
    
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
        # Parse do código
        lexer = PythonLexer(InputStream(code))
        stream = CommonTokenStream(lexer)
        parser = PythonParser(stream)
        tree = parser.program()
        
        # Verificar erros de sintaxe
        if parser.getNumberOfSyntaxErrors() > 0:
            print(f"ERRO DE SINTAXE em '{filename}'")
            return False
        
        # Executar o código
        interpreter = PythonInterpreter()
        interpreter.visit(tree)
        return True
        
    except Exception as e:
        print(f"ERRO DE EXECUÇÃO em '{filename}': {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python run_script.py <arquivo.py>")
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