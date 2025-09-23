#!/bin/bash

# Script para compilar e executar o interpretador Python primitivo

echo "Compilando gramática ANTLR..."

# Gerar código Python a partir da gramática
antlr4 -Dlanguage=Python3 -visitor Python.g4

# Verificar se a compilação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "Gramática compilada com sucesso!"
    echo "Arquivos gerados:"
    ls Python*.py
    
    echo ""
    echo "Para executar o interpretador:"
    echo "python3 interpreter.py"
    
    echo ""
    echo "Ou crie um arquivo de teste (test.py) com código Python primitivo:"
    echo "x = 5"
    echo "print(x)"
    echo "if (x > 3):"
    echo "    print(\"x é maior que 3\")"
else
    echo "Erro na compilação da gramática!"
    exit 1
fi