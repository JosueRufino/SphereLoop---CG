from loop_subdivision import LoopSubdivisionSphere

def main():
    print("Iniciando demonstração do Algoritmo de Subdivisão de Loop...")
    
    # Criar a esfera com 4 níveis de subdivisão
    # Nível 0: 12 vértices
    # Nível 1: 42 vértices
    # Nível 2: 162 vértices
    # Nível 3: 642 vértices
    # Nível 4: 2562 vértices
    sphere = LoopSubdivisionSphere(subdivision_levels=4)
    
    # Exibe estatísticas (Vértices, Faces, Erro de convergência)
    sphere.print_statistics()
    
    # Mostra a evolução visual lado a lado
    print("\nGerando visualização da progressão...")
    sphere.show_progression()
    
    # Visualização final detalhada do último nível
    print("\nExibindo resultado final (Nível 4)...")
    sphere.visualize(show_wireframe=True, show_surface=True)

if __name__ == "__main__":
    main()
