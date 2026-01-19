from loop_subdivision import LoopSubdivisionSphere
import matplotlib.pyplot as plt

def main():
    print("="*60)
    print("DEMONSTRAÇÃO INTERATIVA - ALGORITMO DE LOOP")
    print("="*60)
    print("\nNesta demonstração, você pode controlar o nível de subdivisão")
    print("usando o Slider na parte inferior da janela.")
    
    # Pergunta ao usuário sobre a normalização (opcional)
    print("\nOpções de Renderização:")
    print("1. Loop Padrão (Suavização com encolhimento)")
    print("2. Loop com Projeção Esférica (Ideal para Esferas)")
    
    choice = input("\nEscolha uma opção (1 ou 2) [Padrão 2]: ") or "2"
    normalize = True if choice == "2" else False
    
    levels = 5 # Nível maior para mostrar a potência do algoritmo
    print(f"\nProcessando {levels} níveis de subdivisão...")
    
    # Criar objeto com a opção escolhida
    sphere = LoopSubdivisionSphere(subdivision_levels=levels, normalize_each_step=normalize)
    
    print("\nEstatísticas da Malha:")
    sphere.print_statistics()
    
    print("\nAbrindo janela interativa...")
    print("DICA: Use o mouse para rotacionar a esfera e o slider para mudar o nível.")
    sphere.interactive_demo()

if __name__ == "__main__":
    main()
