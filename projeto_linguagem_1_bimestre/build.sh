#!/bin/bash

# Script para compilar e executar o interpretador Python primitivo

echo "Compilando gramática ANTLR..."

# Gerar código Python a partir da gramática
antlr4 -Dlanguage=Python3 -visitor Python.g4

# Verificar se a compilação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "✅ Gramática compilada com sucesso!"
    echo "Arquivos gerados:"
    ls Python*.py
    
    echo ""
    echo "🧪 Executando testes automáticos..."
    echo "=========================================="
    
    # Verificar se existe arquivo de teste
    if [ -f "test_subject.py" ]; then
        echo "📄 Testando arquivo: test_subject.py"
        python3 tester.py test_subject.py
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "🚀 Executando interpretador com test_subject.py:"
            echo "=========================================="
            python3 homebrew_Interpreter.py test_subject.py
        else
            echo "❌ Teste de sintaxe falhou para test_subject.py"
        fi
    else
        echo "⚠️  Arquivo test_subject.py não encontrado."
        echo "Crie um arquivo test_subject.py para testar o interpretador."
    fi
    
    echo ""
    echo "=========================================="
    echo "✅ Build e testes concluídos!"
    echo ""
    echo "📋 Como usar:"
    echo "  • Testar sintaxe: python3 test_script.py <arquivo.py>"
    echo "  • Executar código: python3 homebrew_Interpreter.py <arquivo.py>"
    echo "  • Editar teste: vim test_subject.py"
    
else
    echo "❌ Erro na compilação da gramática!"
    exit 1
fi