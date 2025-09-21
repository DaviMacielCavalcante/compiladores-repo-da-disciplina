#!/usr/bin/env python3

import sys
import os
from antlr4 import *
from PythonLexer import PythonLexer
from PythonParser import PythonParser

def test_script(filename):
    """Testa um script de arquivo"""
    
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
        
        return True
        
    except Exception as e:
        print(f"ERRO em '{filename}': {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python test_script.py <arquivo.py>")
        return
    
    filename = sys.argv[1]
    
    if test_script(filename):
        print(f"OK: '{filename}' aceito pela gramática")
    else:
        print(f"FALHOU: '{filename}' rejeitado pela gramática")

if __name__ == '__main__':
    main()