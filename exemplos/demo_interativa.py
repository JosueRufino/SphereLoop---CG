import sys
import os
# Adiciona o diretório src ao path para permitir imports do pacote esferaloop
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from esferaloop.nucleo.subdivisao_loop import SubdivisaoLoopEsfera # Importa a classe do algoritmo para gerar a esfera

def run_interactive(): # Define a função para lançar a demonstração interativa
    """ # Início da docstring
    Inicia uma demonstração da esfera com um slider interativo. # Objetivo: permitir controle manual do nível
    """ # Fim da docstring
    print("Iniciando demonstração interativa...") # Log de mensagem no terminal
    print("Use o slider na janela gráfica para trocar o nível de subdivisão.") # Instrução para o usuário

    # Níveis altos (ex: 6) podem ser lentos para processar e renderizar em tempo real # Aviso de performance
    niveis = 5 # Define a quantidade total de níveis disponíveis para o slider (0 a 5)

    # Criar a esfera com a opção de normalizar a cada passo para maior precisão esférica # Detalhe técnico
    esfera = SubdivisaoLoopEsfera(niveis_subdivisao=niveis, normalizar_cada_passo=True)

    # Estatísticas no console para referência # Exibe dados numéricos prévios
    esfera.exibir_estatisticas()

    # Lançar interface interativa # Ponto de entrada da UI
    esfera.demo_interativa() # Abre a janela com o controle deslizante (slider)
# 
if __name__ == "__main__": # Padrão Python para execução de script principal
    run_interactive() # Dispara a execução da demo interativa
