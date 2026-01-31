import numpy as np # Importa NumPy para cálculos matemáticos e manipulação de vetores
from esferaloop.nucleo.malha import Malha # Importa a classe Malha para gerenciar a geometria
from esferaloop.visualizacao.renderizador import Visualizador # Importa o Visualizador para exibir a malha
from esferaloop.utilitarios.metricas import obter_metricas_malha, exibir_tabela_estatisticas # Importa funções de análise

class SubdivisaoLoopEsfera: # Define a classe principal que coordena a subdivisão da esfera
    """ # Início da docstring da classe
    Implementação do algoritmo de subdivisão de Loop para malhas triangulares. # Explica o propósito do algoritmo
    Transforma uma malha grossa em uma superfície suave através de refinamento iterativo. # Detalha o processo de suavização
    """ # Fim da docstring
    def __init__(self, niveis_subdivisao=2, normalizar_cada_passo=False): # Inicializa o processo com níveis e opção de normalização
        self.niveis = niveis_subdivisao # Armazena a quantidade de vezes que a malha será subdividida
        self.normalizar_cada_passo = normalizar_cada_passo # Define se a malha deve ser projetada na esfera em cada passo
        self.malhas = [] # Cria uma lista vazia para armazenar as malhas de cada nível de detalhe
        self.executar() # Chama o método que inicia a execução do algoritmo

    def executar(self) -> list: # Método que coordena a execução sequencial das subdivisões
        """Executa a subdivisão até o nível desejado começando de um icosaedro.""" # Docstring do método
        malha = Malha.gerar_icosaedro() # Gera a malha inicial do icosaedro (Nível 0)
        if self.normalizar_cada_passo: # Verifica se a normalização inicial foi solicitada
            malha = self.normalizar_para_esfera(malha) # Ajusta os vértices iniciais para ficarem sobre a esfera
        self.malhas.append(malha) # Adiciona a malha inicial à lista de níveis

        for k in range(self.niveis): # Itera de acordo com o número de níveis solicitados
            print(f"Subdividindo nível {k} -> {k+1}...") # Exibe mensagem de progresso no console
            malha = self.subdividir(malha) # Aplica uma iteração do algoritmo de Loop na malha atual
            if self.normalizar_cada_passo: # Verifica se deve normalizar após esta subdivisão
                malha = self.normalizar_para_esfera(malha) # Reprojeta os novos pontos na superfície da esfera
            self.malhas.append(malha) # Salva a nova malha refinada na lista de níveis
        return self.malhas[-1] # Retorna a malha final (a mais refinada de todas)

    def subdividir(self, malha: Malha) -> Malha: # O "coração" do algoritmo: aplica as regras de Loop
        """ # Início da docstring
        Aplica uma iteração do algoritmo de Loop. # Objetivo principal
        1. Cria novos 'odd vertices' nas arestas. # Passo 1: novos pontos
        2. Atualiza 'even vertices' (originais). # Passo 2: suavizar pontos antigos
        3. Reconecta para formar 4 novos triângulos por face original. # Passo 3: nova topologia
        """ # Fim da docstring
        vertices = malha.vertices # Obtém os pontos (coordenadas) da malha atual
        faces = malha.faces # Obtém a conectividade (triângulos) da malha atual
        arestas_dict = malha.obter_arestas() # Obtém o mapa de arestas e suas faces vizinhas

        # 1. Calcular Novos Vértices nas Arestas (Odd Vertices) # Cabeçalho do primeiro passo
        novos_vertices = list(vertices) # Começa a nova lista de vértices copiando os originais
        aresta_para_novo_vertice = {} # Mapa para saber qual novo vértice pertence a qual aresta

        for aresta, faces_adjacentes in arestas_dict.items(): # Itera sobre cada aresta única da malha
            v1_idx, v2_idx = aresta # Identifica os dois vértices que formam a aresta
            v1, v2 = vertices[v1_idx], vertices[v2_idx] # Pega as coordenadas XYZ desses vértices

            # Se a aresta for compartilhada por duas faces (malha fechada) # Regra para arestas internas
            if len(faces_adjacentes) == 2: # Se houver dois triângulos vizinhos a esta aresta
                # Encontrar os vértices opostos nas duas faces # Precisamos deles para a fórmula de peso
                vertices_opostos = [] # Lista para guardar os dois vértices "da ponta" dos triângulos
                for idx_face in faces_adjacentes: # Itera pelas duas faces adjacentes
                    face = faces[idx_face] # Pega os 3 índices da face
                    for idx_v in face: # Itera pelos vértices da face
                        if idx_v not in aresta: # Se o vértice não fizer parte da aresta atual, ele é o oposto
                            vertices_opostos.append(vertices[idx_v]) # Guarda a coordenada do vértice oposto
                            break # Sai do loop interno pois já achou o oposto desta face

                v3, v4 = vertices_opostos[0], vertices_opostos[1] # Nomeia os vértices opostos como v3 e v4
                # Regra do Loop para odd vertices: 3/8 * (v1 + v2) + 1/8 * (v3 + v4) # Fórmula matemática
                novo_v = (3/8) * (v1 + v2) + (1/8) * (v3 + v4) # Calcula a posição do novo ponto na aresta
            else: # Caso a aresta tenha apenas 1 face (bordas da malha)
                # Caso de borda (não esperado para uma esfera/icosaedro, mas bom para robustez) # Tratamento de exceção
                novo_v = 0.5 * (v1 + v2) # Em bordas, o novo ponto é apenas a média simples (ponto médio)

            aresta_para_novo_vertice[aresta] = len(novos_vertices) # Registra o índice que este novo vértice terá
            novos_vertices.append(novo_v) # Adiciona o novo vértice à lista global

        # 2. Atualizar Vértices Originais (Even Vertices) # Passo de suavização dos pontos que já existiam
        vertices_atualizados = np.copy(np.array(novos_vertices))

        # Mapear adjacência de vértices # Precisamos saber quem é vizinho de quem
        v_adj = {} # Dicionário para guardar a lista de vizinhos de cada vértice
        for aresta in arestas_dict.keys(): # Itera por todas as arestas
            v1, v2 = aresta # Pega os dois vértices da aresta
            if v1 not in v_adj: v_adj[v1] = [] # Se for a primeira vez que vemos v1, inicializa lista
            if v2 not in v_adj: v_adj[v2] = [] # Se for a primeira vez que vemos v2, inicializa lista
            v_adj[v1].append(v2) # v2 é vizinho de v1
            v_adj[v2].append(v1) # v1 é vizinho de v2

        for idx_v in range(len(vertices)): # Agora itera apenas pelos vértices originais (índices antigos)
            vizinhos = v_adj.get(idx_v, []) # Busca a lista de vizinhos do vértice atual
            n = len(vizinhos) # n é o grau (valência) do vértice

            if n > 0: # Só processa se o vértice tiver vizinhos
                # Cálculo do peso Beta # Define o quanto os vizinhos influenciam na nova posição
                if n == 3: # Caso especial para vértices com 3 vizinhos
                    beta = 3/16 # Valor constante de beta para n=3
                else: # Caso geral para n > 3
                    beta = (1/n) * (5/8 - (3/8 + 0.25 * np.cos(2 * np.pi / n))**2) # Fórmula trigonométrica de Loop

                soma_vizinhos = np.sum(vertices[vizinhos], axis=0) # Soma as coordenadas XYZ de todos os vizinhos
                # Regra: (1 - n*beta) * v_original + beta * sum(v_neighbors) # Fórmula de atualização
                vertices_atualizados[idx_v] = (1 - n * beta) * vertices[idx_v] + beta * soma_vizinhos # Calcula nova posição

        # 3. Gerar Novas Faces # Último passo: reconstruir a topologia da malha
        novas_faces = [] # Lista para as novas faces triangulares (4x mais que antes)
        for face in faces: # Itera sobre cada triângulo original
            v1, v2, v3 = face # Identifica os 3 vértices do triângulo original

            # Obter índices dos novos vértices nas arestas # Busca no mapa que criamos no Passo 1
            a = aresta_para_novo_vertice[tuple(sorted((v1, v2)))] # Novo ponto entre v1 e v2
            b = aresta_para_novo_vertice[tuple(sorted((v2, v3)))] # Novo ponto entre v2 e v3
            c = aresta_para_novo_vertice[tuple(sorted((v3, v1)))] # Novo ponto entre v3 e v1

            # Cada triângulo original v1-v2-v3 vira 4 triângulos: # Divisão geométrica
            # (v1, a, c), (v2, b, a), (v3, c, b), (a, b, c) # Conectividade dos novos triângulos
            novas_faces.append([v1, a, c]) # Triângulo do "canto" v1
            novas_faces.append([v2, b, a]) # Triângulo do "canto" v2
            novas_faces.append([v3, c, b]) # Triângulo do "canto" v3
            novas_faces.append([a, b, c]) # Triângulo central (invertido)

        return Malha(vertices_atualizados, np.array(novas_faces)) # Retorna a nova malha completa

    def normalizar_para_esfera(self, malha: Malha) -> Malha: # Função utilitária para manter a forma circular
        """Normaliza todos os vértices para raio 1 (projeção na esfera).""" # Docstring
        normas = np.linalg.norm(malha.vertices, axis=1)[:, np.newaxis] # Calcula a distância de cada vértice até a origem
        malha.vertices /= normas # Divide a posição pela distância (fazendo o raio ser exatamente 1.0)
        return malha # Retorna a malha modificada

    def visualizar(self, nivel=-1, mostrar_wireframe=True, mostrar_superficie=True): # Exibe uma malha específica
        """Visualiza a malha do nível especificado (padrão: último nível).""" # Docstring
        Visualizador.plotar_malha(self.malhas[nivel], title=f"Esfera Subdividida - Nível {len(self.malhas)-1 if nivel == -1 else nivel}", 
                           mostrar_wireframe=mostrar_wireframe, mostrar_superficie=mostrar_superficie) # Chama o renderizador
        import matplotlib.pyplot as plt # Importa Matplotlib para exibir a janela
        plt.show() # Abre a janela gráfica

    def mostrar_progressao(self): # Exibe todos os níveis lado a lado
        """Mostra evolução da subdivisão lado a lado.""" # Docstring
        Visualizador.mostrar_progressao(self.malhas) # Chama o método de progressão do Visualizador

    def exibir_estatisticas(self): # Exibe os dados numéricos de crescimento da malha
        """Exibe métricas de todos os níveis processados.""" # Docstring
        todas_metricas = [obter_metricas_malha(m) for m in self.malhas] # Calcula métricas para cada nível salvo
        exibir_tabela_estatisticas(todas_metricas) # Exibe a tabela formatada no console

    def demo_interativa(self): # Inicia o modo interativo
        """Inicia a visualização interativa com slider.""" # Docstring
        Visualizador.plot_interativo(self.malhas) # Abre janela com controle deslizante de nível
