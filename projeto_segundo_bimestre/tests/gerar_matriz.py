import sys
import os
from pathlib import Path

# --- 1. Configuração de Caminhos ---
# Pega o diretório onde este script está (tests/)
current_dir = Path(__file__).parent
# Pega a raiz do projeto (um nível acima de tests/)
project_root = current_dir.parent
# Define onde está o código fonte (src/)
src_dir = project_root / "src"

# Adiciona src/ ao path do Python para conseguir importar os módulos
sys.path.insert(0, str(src_dir))

try:
    from grammar import Grammar
    from first_follow import FirstFollow
    from parsing_table import ParsingTable
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print(f"O script tentou buscar os módulos em: {src_dir}")
    sys.exit(1)

def main():
    print("=" * 60)
    print("GERADOR DE MATRIZ DE PARSING LL(1)")
    print("=" * 60)

    # --- 2. Localizar e Carregar Gramática ---
    # Tenta achar o arquivo .bnf na pasta src ou docs
    possible_paths = [
        src_dir / "gramatica_sem_ambiguidade.bnf",
        project_root / "docs" / "gramatica_sem_ambiguidade.bnf",
        src_dir / "gramatica.bnf"
    ]
    
    grammar_file = None
    for path in possible_paths:
        if path.exists():
            grammar_file = path
            break
            
    if not grammar_file:
        print("❌ Arquivo de gramática não encontrado!")
        return

    print(f"📂 Gramática: {grammar_file.name}")
    g = Grammar()
    g.load_from_file(str(grammar_file))

    # --- 3. Calcular First e Follow ---
    print("⚙️  Calculando First e Follow...")
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()

    # --- 4. Gerar Tabela ---
    print("🏗️  Construindo Tabela de Parsing...")
    pt = ParsingTable(g, ff)
    pt.build()

    # Verifica status da tabela
    if pt.is_ll1_pure():
        print("✅ Gramática é LL(1) Pura.")
    elif pt.is_ll1_practical():
        print("⚠️ Gramática é LL(1) Prática (conflitos resolvidos automaticamente).")
    else:
        print(f"❌ Gramática NÃO é LL(1). Existem {len(pt.conflicts)} conflitos irresolvíveis.")
        print("   (O arquivo será gerado mesmo assim para análise)")

    # --- 5. Salvar na Raiz ---
    output_filename = "parsing_table_matrix.txt"
    output_path = project_root / output_filename
    
    print(f"\n💾 Salvando arquivo em: {output_path}")
    
    # Usa o método que já existe na sua classe ParsingTable
    # Ajustei a largura das colunas para ficar mais legível no txt
    pt.save_matrix_to_file(
        str(output_path), 
        max_col_width=18, 
        max_cell_width=40
    )
    
    # Opcional: Gerar também o CSV que é melhor para visualizar
    csv_path = project_root / "parsing_table.csv"
    pt.save_matrix_to_csv(str(csv_path))
    print(f"💾 CSV salvo em: {csv_path} (Recomendado para abrir no Excel)")

    print("\n✨ Concluído!")

if __name__ == "__main__":
    main()