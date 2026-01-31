import os
import sys

# Adiciona o diretório src ao path para permitir imports do pacote esferaloop
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from esferaloop.nucleo.subdivisao_loop import SubdivisaoLoopEsfera # Importa a lógica principal do algoritmo

def main(): # Define a função de entrada principal do programa
    print("Iniciando demonstração do Algoritmo de Subdivisão de Loop...") # Exibe mensagem de início

    # Criar a esfera com 4 níveis de subdivisão
    esfera = SubdivisaoLoopEsfera(niveis_subdivisao=4)

    # Exibe estatísticas (Vértices, Faces, Erro de convergência)
    esfera.exibir_estatisticas()

    # Mostra a evolução visual lado a lado
    print("\nGerando visualização da progressão...")
    esfera.mostrar_progressao()

    # Visualização final detalhada do último nível
    print("\nExibindo resultado final (Nível 4)...")
    esfera.visualizar(mostrar_wireframe=True, mostrar_superficie=True)

if __name__ == "__main__":
    main()
