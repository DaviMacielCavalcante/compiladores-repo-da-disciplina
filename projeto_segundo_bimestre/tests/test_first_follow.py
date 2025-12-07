import sys
from pathlib import Path

# Adiciona src/ ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from grammar import Grammar
from first_follow import FirstFollow

def test_vython_grammar():
    """Testa FIRST e FOLLOW na gramática Vython BNF pura."""
    
    print("=" * 60)
    print("TESTE: Gramática Vython (BNF Pura) - LL(1)")
    print("=" * 60)
    
    # CORRIGIDO: Nome correto do arquivo ✅
    grammar_file = project_root / "gramatica_sem_ambiguidade.bnf"
    
    if not grammar_file.exists():
        print(f"❌ ERRO: Arquivo não encontrado: {grammar_file}")
        print("\nProcurando em outros locais...")
        
        # Tenta outros caminhos possíveis
        alternatives = [
            project_root / "docs" / "gramatica_bnf_pura.bnf",
            project_root / "grammar" / "gramatica_bnf_pura.bnf",
            project_root / "src" / "gramatica_bnf_pura.bnf",
            Path("gramatica_bnf_pura.bnf"),
            # Adiciona também a versão sem ambiguidade como fallback
            project_root / "gramatica_sem_ambiguidade.bnf",
            project_root / "docs" / "gramatica_sem_ambiguidade.bnf",
        ]
        
        for alt in alternatives:
            if alt.exists():
                grammar_file = alt
                print(f"✅ Encontrado em: {grammar_file}")
                break
        else:
            print("❌ Arquivo não encontrado em nenhum local.")
            print("\nLocais verificados:")
            print(f"  - {project_root / 'gramatica_bnf_pura.bnf'}")
            print(f"  - {project_root / 'docs' / 'gramatica_bnf_pura.bnf'}")
            print(f"  - {project_root / 'grammar' / 'gramatica_bnf_pura.bnf'}")
            print(f"  - {project_root / 'src' / 'gramatica_bnf_pura.bnf'}")
            
            # CORRIGIDO: Retorna None explicitamente ✅
            return None  
    
    print(f"\n📁 Carregando: {grammar_file.name}")
    print("-" * 60)
    
    # Carrega gramática
    g = Grammar()
    g.load_from_file(str(grammar_file))
    
    # Estatísticas
    print(f"\n📊 ESTATÍSTICAS DA GRAMÁTICA:")
    print(f"   Símbolo inicial: {g.start_symbol}")
    print(f"   Não-terminais: {len(g.nonterminals)}")
    print(f"   Terminais: {len(g.terminals)}")
    print(f"   Produções: {sum(len(prods) for prods in g.productions.values())}")
    print(f"   Epsilon (ε): {g.epsilon}")
    
    # Conta produções com epsilon
    epsilon_count = 0
    for prods in g.productions.values():
        for prod in prods:
            if prod and g.is_epsilon(prod[0]):
                epsilon_count += 1
    
    print(f"   Produções com ε: {epsilon_count}")
    
    # Calcula FIRST e FOLLOW
    print("\n⏳ Calculando conjuntos FIRST...")
    ff = FirstFollow(g)
    ff.compute_first()
    print("✅ FIRST calculado!")
    
    print("⏳ Calculando conjuntos FOLLOW...")
    ff.compute_follow()
    print("✅ FOLLOW calculado!")
    
    # Exibe resultados
    print("\n" + "=" * 60)
    ff.print_sets()
    print("=" * 60)
    
    # Análise LL(1)
    print("\n🔍 ANÁLISE LL(1):")
    analyze_ll1(g, ff)
    
    # CORRIGIDO: Sempre retorna tupla ✅
    return g, ff

def analyze_ll1(grammar, first_follow):
    """Verifica se a gramática é LL(1)."""
    
    conflicts = []
    
    print("-" * 60)
    
    for nt in grammar.nonterminals:
        productions = grammar.productions.get(nt, [])
        
        if len(productions) <= 1:
            continue  # Sem ambiguidade possível
        
        # Calcula FIRST de cada produção
        first_sets = []
        for prod in productions:
            if prod and grammar.is_epsilon(prod[0]):
                first_prod = {grammar.epsilon}
            else:
                first_prod = first_follow._first_of_sequence(prod)
            first_sets.append(first_prod)
        
        # Verifica conflitos entre produções
        for i in range(len(first_sets)):
            for j in range(i + 1, len(first_sets)):
                intersection = first_sets[i] & first_sets[j]
                
                # Remove epsilon da interseção para análise
                non_epsilon_intersection = intersection - {grammar.epsilon}
                
                if non_epsilon_intersection:
                    conflicts.append({
                        'nt': nt,
                        'prod1': productions[i],
                        'prod2': productions[j],
                        'conflict': non_epsilon_intersection
                    })
    
    if not conflicts:
        print("✅ GRAMÁTICA É LL(1)!")
        print("   Nenhum conflito FIRST-FIRST detectado.")
    else:
        print(f"❌ CONFLITOS DETECTADOS: {len(conflicts)}")
        print("\n   Detalhes dos conflitos:")
        for conf in conflicts[:5]:  # Mostra apenas os 5 primeiros
            print(f"\n   Não-terminal: {conf['nt']}")
            print(f"   Produção 1: {' '.join(conf['prod1'])}")
            print(f"   Produção 2: {' '.join(conf['prod2'])}")
            print(f"   Conflito em: {conf['conflict']}")
        
        if len(conflicts) > 5:
            print(f"\n   ... e mais {len(conflicts) - 5} conflitos.")
    
    print("-" * 60)

def save_results(grammar, first_follow, output_file="first_follow_results.txt"):
    """Salva resultados em arquivo."""
    
    output_path = project_root / output_file
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("CONJUNTOS FIRST E FOLLOW - GRAMÁTICA VYTHON\n")
        f.write("=" * 60 + "\n\n")
        
        # FIRST
        f.write("=== FIRST ===\n\n")
        for nt in sorted(grammar.nonterminals):
            first_list = sorted(
                first_follow.first[nt], 
                key=lambda x: (x != grammar.epsilon, x)
            )
            f.write(f"{nt}:\n")
            f.write(f"  {{{', '.join(first_list)}}}\n\n")
        
        # FOLLOW
        f.write("\n" + "=" * 60 + "\n")
        f.write("=== FOLLOW ===\n\n")
        for nt in sorted(grammar.nonterminals):
            follow_list = sorted(
                first_follow.follow[nt],
                key=lambda x: (x != '$', x)
            )
            f.write(f"{nt}:\n")
            f.write(f"  {{{', '.join(follow_list)}}}\n\n")
    
    print(f"\n💾 Resultados salvos em: {output_path}")

def main():
    """Executa todos os testes."""
    
    try:
        # CORRIGIDO: Trata quando retorna None ✅
        result = test_vython_grammar()
        
        if result is None:
            print("\n❌ Teste falhou: gramática não foi carregada.")
            print("\n💡 DICA: Verifique se o arquivo existe em:")
            print(f"   {project_root / 'gramatica_bnf_pura.bnf'}")
            return
        
        g, ff = result
        
        # Pergunta se quer salvar
        print("\n" + "=" * 60)
        save = input("💾 Salvar resultados em arquivo? (s/n): ").lower()
        
        if save == 's':
            save_results(g, ff)
            print("✅ Arquivo gerado com sucesso!")
        
        print("\n🎉 Teste concluído!")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERRO: {e}")
        print("\nVerifique se o arquivo 'gramatica_bnf_pura.bnf' existe.")
    
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()