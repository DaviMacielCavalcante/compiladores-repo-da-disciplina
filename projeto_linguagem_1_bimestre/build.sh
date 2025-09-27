#!/bin/bash

echo "Compilando gramática ANTLR..."
antlr4 -Dlanguage=Python3 -visitor PythonLexer.g4 PythonParser.g4

if [ $? -ne 0 ]; then
    echo "Erro na compilação!"
    exit 1
fi

echo "Compilação concluída."

# Opção: mostrar tokens
if [ "$1" == "--tokens" ] || [ "$1" == "-t" ]; then
    [ -f "test_subject.py" ] || { echo "test_subject.py não encontrado."; exit 1; }
    python3 -c "
from antlr4 import *
from PythonLexer import PythonLexer

with open('test_subject.py', 'r') as f:
    code = f.read()

lexer = PythonLexer(InputStream(code))
tokens = CommonTokenStream(lexer)
tokens.fill()

print('TOKENS:')
for i, token in enumerate(tokens.tokens):
    if token.type != Token.EOF:
        # Tentar pegar nome simbólico primeiro, depois literal
        if token.type < len(lexer.symbolicNames) and lexer.symbolicNames[token.type]:
            name = lexer.symbolicNames[token.type]
        elif token.type < len(lexer.literalNames) and lexer.literalNames[token.type]:
            name = lexer.literalNames[token.type]
        else:
            name = f'TOKEN_{token.type}'
        print(f'{i:3d} | {name:20s} | {repr(token.text)}')
    else:
        print(f'{i:3d} | EOF')
"
    exit 0
fi

# Opção: compilar GUI
if [ "$1" == "--gui" ] || [ "$1" == "-g" ]; then
    ANTLR_JAR="/usr/local/lib/antlr-4.13.1-complete.jar"
    
    [ -f "$ANTLR_JAR" ] || {
        echo "Baixando ANTLR JAR..."
        sudo wget -O "$ANTLR_JAR" https://www.antlr.org/download/antlr-4.13.1-complete.jar
    }
    
    java -cp "$ANTLR_JAR:$CLASSPATH" org.antlr.v4.Tool PythonLexer.g4 PythonParser.g4
    javac -cp "$ANTLR_JAR:$CLASSPATH" Python*.java
    
    if [ $? -eq 0 ]; then
        echo "Compilação Java concluída."
        echo "Uso: java -cp \".:$ANTLR_JAR\" org.antlr.v4.gui.TestRig Python program -gui < test_subject.py"
    fi
    exit 0
fi

# Executar testes
if [ -f "test_subject.py" ]; then
    python3 tester.py test_subject.py && python3 homebrew_Interpreter.py test_subject.py
else
    echo "test_subject.py não encontrado."
fi

echo ""
echo "Uso:"
echo "  ./build.sh           - build e teste"
echo "  ./build.sh --tokens  - mostrar tokens"
echo "  ./build.sh --gui     - compilar GUI"