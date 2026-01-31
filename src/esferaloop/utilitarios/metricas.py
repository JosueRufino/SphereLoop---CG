import numpy as np # Importa NumPy para cálculos estatísticos e vetoriais
import time # Importa biblioteca para controle de tempo (se necessário)
# 
def obter_metricas_malha(malha, raio_alvo=1.0) -> dict: # Função para calcular a precisão geométrica da malha
    """ # Início da docstring
    Calcula métricas de qualidade da malha. # Objetivo principal
    - Contagem de elementos # Vértices e faces
    - Erro de raio (distância média ao centro) # Quão longe está de ser uma esfera
    - Desvio padrão do raio (suavidade da forma) # Consistência da esfericidade
    """ # Fim da docstring
    vertices = malha.vertices # Pega as coordenadas XYZ dos pontos da malha
    faces = malha.faces # Pega a lista de triângulos da malha

    # Radii de todos os vértices (distância da origem) # Título do bloco de cálculo
    raios = np.linalg.norm(vertices, axis=1) # Calcula o raio (norma) de cada vértice em relação à origem (0,0,0)

    # Erro médio em relação ao raio alvo # Título do bloco de estatísticas
    raio_medio = np.mean(raios) # Calcula o raio médio de todos os pontos
    raio_max = np.max(raios) # Identifica o ponto mais distante do centro
    raio_min = np.min(raios) # Identifica o ponto mais próximo do centro

    erro_medio = np.mean(np.abs(raios - raio_alvo)) # Erro médio absoluto: média da diferença para o raio ideal (1.0)
    desvio_padrao_raio = np.std(raios) # Desvio padrão: indica se os pontos estão todos à mesma distância ou oscilam

    # Cálculo de áreas das faces para avaliar a distribuição uniforme
    face_vertices = vertices[faces] # Pega os 3 vértices de cada face: shape (M, 3, 3)
    v0, v1, v2 = face_vertices[:, 0], face_vertices[:, 1], face_vertices[:, 2]
    # Área do triângulo via produto vetorial: 0.5 * |(v1-v0) x (v2-v0)|
    areas = 0.5 * np.linalg.norm(np.cross(v1 - v0, v2 - v0), axis=1)
    
    area_media = np.mean(areas)
    desvio_padrao_area = np.std(areas) # Medida de uniformidade da distribuição

    return { # Retorna um dicionário com todos os dados calculados
        "num_vertices": len(vertices), # Quantidade total de pontos
        "num_faces": len(faces), # Quantidade total de triângulos
        "erro_medio": erro_medio, # Média de erro em relação à esfera ideal
        "desvio_padrao_raio": desvio_padrao_raio, # Medida de rugosidade/irregularidade
        "area_media": area_media, # Área média das faces
        "desvio_padrao_area": desvio_padrao_area, # Uniformidade da malha (objetivo específico)
        "raio_min": raio_min, # Raio mínimo encontrado
        "raio_max": raio_max # Raio máximo encontrado
    } # Fim do dicionário

def exibir_tabela_estatisticas(todas_metricas: list): # Função para imprimir os resultados de forma organizada
    """Exibe uma tabela formatada com as estatísticas de cada nível.""" # Docstring
    print("\n" + "="*80) # Imprime uma linha decorativa superior (80 sinais de igual)
    print(f"{'Nível':<6} | {'Vértices':<8} | {'Faces':<8} | {'Erro Raio':<12} | {'Desvio Raio':<12} | {'Desvio Área':<12}") # Cabeçalho da tabela
    print("-" * 95) # Linha separadora do cabeçalho
    for i, meta in enumerate(todas_metricas): # Itera por cada nível de métrica fornecido
        # Imprime os valores com alinhamento e precisão decimal
        print(f"{i:<6} | {meta['num_vertices']:<8} | {meta['num_faces']:<8} | {meta['erro_medio']:<12.6f} | {meta['desvio_padrao_raio']:<12.6f} | {meta['desvio_padrao_area']:<12.6f}")
    print("="*95 + "\n") # Imprime uma linha decorativa inferior
