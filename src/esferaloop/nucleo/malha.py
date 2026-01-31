import numpy as np # Importa a biblioteca NumPy para processamento numérico de arrays e matrizes
# 
class Malha: # Define a classe principal para representar uma malha triangular em 3D
    """ # Início da docstring da classe
    Classe para representar uma malha triangular 3D. # Descrição: representa a estrutura de dados da malha
    Armazena vértices e faces, e fornece métodos para manipulação da topologia. # Descrição complementar sobre armazenamento e métodos
    """ # Fim da docstring
    def __init__(self, vertices=None, faces=None): # Método construtor que inicializa a malha com vértices e faces
        # Vertices: array numpy de formato (N, 3) # Comentário interno sobre o formato esperado dos vértices
        self.vertices = np.array(vertices, dtype=float) if vertices is not None else np.empty((0, 3)) # Se houver vértices, converte para array float; se não, cria array vazio
        # Faces: array numpy de formato (M, 3) contendo índices de vértices # Comentário interno sobre o formato esperado das faces
        self.faces = np.array(faces, dtype=int) if faces is not None else np.empty((0, 3), dtype=int) # Se houver faces, converte para array int; se não, cria array vazio

    def obter_arestas(self) -> dict: # Método para extrair e mapear todas as arestas únicas da malha
        """ # Início da docstring do método
        Extrai todas as arestas únicas da malha. # Objetivo: identificar as conexões entre vértices
        Retorna um dicionário mapeando arestas (tupla ordenada) para faces adjacentes. # Explica o formato de retorno do mapeamento
        """ # Fim da docstring
        arestas = {} # Inicializa um dicionário vazio para armazenar as arestas
        for idx_face, face in enumerate(self.faces): # Itera sobre cada face da malha, mantendo o índice (idx_face)
            for i in range(3): # Cada face triangular possui 3 arestas, itera por elas
                v1, v2 = face[i], face[(i + 1) % 3] # Pega dois vértices consecutivos para formar uma aresta (cicla 0-1, 1-2, 2-0)
                aresta = tuple(sorted((v1, v2))) # Ordena os índices e cria uma tupla para que a aresta (1,2) seja igual a (2,1)
                if aresta not in arestas: # Verifica se esta aresta já foi registrada no dicionário
                    arestas[aresta] = [] # Se for nova, cria uma lista vazia para armazenar as faces que a compartilham
                arestas[aresta].append(idx_face) # Adiciona o índice da face atual à lista de faces adjacentes a esta aresta
        return arestas # Retorna o dicionário completo com todas as arestas e suas faces vizinhas

    @staticmethod # Decorador que define o método seguinte como estático (não depende de uma instância)
    def gerar_icosaedro(): # Método que gera a geometria inicial de um icosaedro regular
        """ # Início da docstring
        Gera um icosaedro regular centrado na origem como malha inicial (Nível 0). # Explica que é o ponto de partida do algoritmo
        Um icosaedro possui 12 vértices e 20 faces triangulares. # Detalhes geométricos do sólido platônico
        """ # Fim da docstring
        phi = (1 + np.sqrt(5)) / 2  # Calcula a constante da proporção áurea (número de ouro)

        # Vértices de um icosaedro regular # Comentário sobre a definição das coordenadas XYZ
        vertices = [ # Lista contendo os 12 pontos fundamentais do icosaedro
            [-1,  phi,  0], [ 1,  phi,  0], [-1, -phi,  0], [ 1, -phi,  0], # Coordenadas baseadas em planos ortogonais
            [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi], # Coordenadas baseadas em planos ortogonais
            [ phi,  0, -1], [ phi,  0,  1], [-phi,  0, -1], [-phi,  0,  1]  # Coordenadas baseadas em planos ortogonais
        ] # Fim da lista de vértices

        # Normalizar para que fiquem na esfera unitária (raio = 1) # Comentário sobre o ajuste de escala
        vertices = np.array(vertices) # Converte a lista de listas em um array NumPy para operações vetorizadas
        vertices /= np.linalg.norm(vertices, axis=1)[:, np.newaxis] # Divide cada vetor (XYZ) pelo seu comprimento para que o raio seja 1.0

        # 20 faces triangulares # Comentário sobre a conectividade (quais vértices formam cada triângulo)
        faces = [ # Lista contendo os conjuntos de 3 índices de vértices que compõem cada face
            [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11], # Primeiras 5 faces ao redor de um vértice
            [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8], # Faces intermediárias
            [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9], # Faces ao redor do vértice oposto
            [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]  # Faces de fechamento
        ] # Fim da lista de faces

        return Malha(vertices, faces) # Cria e retorna um novo objeto Malha com a geometria do icosaedro

    def estatisticas(self) -> tuple: # Método simples para obter informações básicas da malha
        """Retorna contagem de vértices e faces.""" # Docstring de linha única
        return len(self.vertices), len(self.faces) # Retorna uma tupla com a quantidade total de pontos e triângulos
