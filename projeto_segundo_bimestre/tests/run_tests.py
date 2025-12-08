import sys
import os
import glob
import time

# --- Configuração de Path para encontrar o 'src' ---
# Pega o diretório atual (tests/) e sobe um nível para achar src/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, "src")

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# --- Importações do seu compilador ---
try:
    from grammar import Grammar
    from first_follow import FirstFollow
    from parsing_table import ParsingTable
    from ll1_parser import LL1Parser
    from lexer import Lexer
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print(f"Verifique se os arquivos estão em: {src_dir}")
    sys.exit(1)


def setup_compiler():
    """Inicializa a Gramática e a Tabela (pesado, faz só uma vez)"""
    print("⏳ Inicializando compilador (Grammar + Table)...")

    # Tenta achar a gramática em locais comuns
    grammar_names = ["gramatica_sem_ambiguidade.bnf", "gramatica.bnf"]
    grammar_path = None

    # Procura em src/ e docs/
    search_paths = [src_dir, os.path.join(project_root, "docs"), project_root]

    for path in search_paths:
        for name in grammar_names:
            full_path = os.path.join(path, name)
            if os.path.exists(full_path):
                grammar_path = full_path
                break
        if grammar_path:
            break

    if not grammar_path:
        raise FileNotFoundError("Arquivo de gramática não encontrado!")

    g = Grammar()
    g.load_from_file(grammar_path)

    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()

    pt = ParsingTable(g, ff)
    pt.build()

    return g, pt


def run_file_test(filepath, grammar, table):
    """Roda o teste para um único arquivo (Corrigido para Windows)"""
    filename = os.path.basename(filepath)
    print(f"\n📄 Testando: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    # 1. Lexer
    try:
        lexer = Lexer(source_code)
        tokens = lexer.get_token_tuples()
    except Exception as e:
        print(f"   ❌ ERRO LÉXICO: {e}")
        return False

    # 2. Parser
    parser = LL1Parser(grammar, table)
    
    # CORREÇÃO AQUI: Forçar encoding utf-8 no devnull para suportar a seta '→'
    try:
        # Tenta usar devnull com encoding (Python 3)
        devnull = open(os.devnull, 'w', encoding='utf-8')
    except:
        # Fallback para sistemas muito antigos
        devnull = open(os.devnull, 'w')

    old_stdout = sys.stdout
    sys.stdout = devnull
    
    try:
        success = parser.parse(tokens)
    except Exception as e:
        # Se der erro durante o parse, restaura stdout para mostrar o erro
        sys.stdout = old_stdout
        print(f"   ❌ ERRO DE EXECUÇÃO: {e}")
        return False
    finally:
        sys.stdout = old_stdout # Restaura o print normal
        devnull.close()

    if success:
        print(f"   ✅ PASSOU (Sintaxe Aceita)")
    else:
        # Se o nome do arquivo contém 'erro' ou 'fail', falhar é o esperado!
        if 'erro' in filename or 'fail' in filename:
            print(f"   ✅ PASSOU (Rejeitado corretamente como esperado)")
        else:
            print(f"   ❌ FALHOU (Deveria aceitar, mas rejeitou)")
    
    return success


def main():
    try:
        # 1. Setup
        g, pt = setup_compiler()
        print("✅ Compilador pronto.\n")

        # 2. Encontrar arquivos de teste (.vy ou .txt na pasta tests)
        test_files = glob.glob(os.path.join(current_dir, "*.vy"))
        test_files += glob.glob(os.path.join(current_dir, "*.txt"))
        test_files.sort()

        if not test_files:
            print(
                "⚠️ Nenhum arquivo de teste encontrado em 'tests/'. Crie arquivos .vy!"
            )
            return

        # 3. Executar
        print("=" * 40)
        for file in test_files:
            # Pula o próprio script se ele for pego pelo glob (improvável mas seguro)
            if file.endswith(".py"):
                continue

            run_file_test(file, g, pt)
        print("=" * 40)

    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")


if __name__ == "__main__":
    main()
