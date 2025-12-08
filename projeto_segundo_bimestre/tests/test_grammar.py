import os
from grammar import Grammar

# Obtém o diretório onde este script está
script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho completo para a gramática
grammar_path = os.path.join(script_dir, "gramatica_sem_ambiguidade.bnf")

g = Grammar()
g.load_from_file(grammar_path)
