import matplotlib.pyplot as plt # Importa Matplotlib para criação de gráficos 2D e 3D
from mpl_toolkits.mplot3d import Axes3D # Importa ferramentas para eixos tridimensionais
from mpl_toolkits.mplot3d.art3d import Poly3DCollection # Permite desenhar coleções de triângulos em 3D
from matplotlib.widgets import Slider # Importa o componente de controle deslizante (slider)
import numpy as np # Importa NumPy para manipulação de arrays e vetores
# 
class Visualizador: # Classe dedicada à renderização visual da malha
    """ # Início da docstring da classe
    Classe responsável pela renderização 3D da malha usando Matplotlib. # Explica a responsabilidade da classe
    """ # Fim da docstring
    @staticmethod # Define que o método é estático e não precisa de 'self'
    def plotar_malha(malha, title="Nível de Subdivisão", mostrar_wireframe=True, mostrar_superficie=True, ax=None, intensidade_luz=1.0): # Desenha a malha em um eixo 3D
        if ax is None: # Se nenhum eixo foi fornecido (ex: gráfico único)
            fig = plt.figure(figsize=(10, 8)) # Cria uma nova figura com tamanho 10x8 polegadas
            ax = fig.add_subplot(111, projection='3d') # Adiciona um subgráfico com projeção tridimensional

        vertices = malha.vertices # Pega as coordenadas XYZ dos pontos da malha
        faces = malha.faces # Pega a conectividade dos triângulos da malha

        if mostrar_superficie: # Se a visualização de superfície (preenchida) estiver ativada
            # Criar coleção de polígonos para a superfície
            poly3d = [[vertices[idx] for idx in face] for face in faces] 

            # --- CÁLCULO MANUAL DE ILUMINAÇÃO (Lambertian Shading) ---
            v0, v1, v2 = vertices[faces[:, 0]], vertices[faces[:, 1]], vertices[faces[:, 2]]
            normais = np.cross(v1 - v0, v2 - v0) # Vetor normal a cada face
            with np.errstate(invalid='ignore'): # Trata divisão por zero em malhas degeneradas se houver
                modulo = np.linalg.norm(normais, axis=1)[:, np.newaxis]
                normais = np.where(modulo > 0, normais / modulo, 0)

            direcao_luz = np.array([0.8, 0.4, 1.2]) # Luz inclinada para o lado para sombra lateral
            direcao_luz /= np.linalg.norm(direcao_luz)

            # --- CÁLCULO DE ILUMINAÇÃO (Lambert + Refletida) ---
            dot_product = np.dot(normais, direcao_luz)
            
            # Luz direta (lado iluminado)
            direta = np.clip(dot_product, 0.0, 1.0)
            
            # Luz Refletida (brilho sutil na base da sombra, conforme imagem de referência)
            refletida = np.clip(-dot_product, 0.0, 1.0) * 0.2 
            
            # Intensidade base (com luz ambiente mínima)
            intesidades_calculadas = np.clip(direta + refletida + 0.1, 0.0, 1.0)
            
            # Interpolação para controle do slider
            intensidades_finais = (1.0 * (1 - intensidade_luz)) + (intesidades_calculadas * intensidade_luz)

            # Converte intensidades em cores (tons de ciano/cinza azulado)
            cores_faces = []
            for i in intensidades_finais:
                # Cor base: azul petróleo/ciano suave
                cores_faces.append((0, i * 0.7 + 0.1, i * 0.7 + 0.2)) 

            colecao = Poly3DCollection(poly3d, facecolors=cores_faces, 
                                     edgecolors='black' if mostrar_wireframe else 'none',
                                     alpha=1.0)
            ax.add_collection3d(colecao)

        elif mostrar_wireframe: # Caso apenas o esqueleto (linhas) seja solicitado
            # Se apenas wireframe for solicitado # Título do bloco alternativo
            for face in faces: # Itera por cada triângulo
                v = vertices[face] # Pega os 3 pontos do triângulo
                v = np.vstack([v, v[0]]) # Adiciona o primeiro ponto novamente ao final para fechar o triângulo ao desenhar
                ax.plot(v[:,0], v[:,1], v[:,2], color='black', linewidth=0.5) # Plota as linhas pretas finas

        # --- ADICIONA PLANO DE FUNDO (PISO - REMOVIDO VISUALMENTE) ---
        piso_z = -1.1 # Mantemos o valor para o cálculo da sombra, mas não desenhamos o piso

        # --- CÁLCULO DE SOMBRA PROJETADA ---
        # Projeta cada vértice na direção da luz até atingir o plano do piso
        direcao_luz = np.array([0.8, 0.4, 1.2])
        direcao_luz /= np.linalg.norm(direcao_luz)
        
        t = (piso_z - vertices[:, 2]) / direcao_luz[2]
        vertices_sombra = vertices + t[:, np.newaxis] * direcao_luz
        
        poly_sombra = [[vertices_sombra[idx] for idx in face] for face in faces]
        # Sombra suave e sem bordas para silhueta limpa
        sombra_colecao = Poly3DCollection(poly_sombra, facecolors='#111111', alpha=0.4, edgecolors='none', zorder=1)
        ax.add_collection3d(sombra_colecao)

        # Ajustar limites e labels # Configurações de visualização da cena
        # Limites ajustados para a nova posição da sombra (mais para o lado)
        ax.set_xlim([-1.8, 1.2]) 
        ax.set_ylim([-1.5, 1.5]) 
        ax.set_zlim([piso_z, 1.5]) 
        ax.set_title(title) # Define o título do gráfico
        ax.axis('off') # Desativa a exibição dos eixos

    @staticmethod # Define método estático para progressão
    def mostrar_progressao(malhas): # Mostra a evolução da malha nível por nível
        """Mostra evolução da subdivisão lado a lado.""" # Docstring
        num_niveis = len(malhas) # Conta quantos níveis de subdivisão existem para exibir
        fig = plt.figure(figsize=(5 * num_niveis, 5)) # Cria figura larga proporcional ao número de níveis

        for i, malha in enumerate(malhas): # Itera por cada malha salva na lista
            ax = fig.add_subplot(1, num_niveis, i + 1, projection='3d') # Cria um subgráfico para cada nível em uma linha
            Visualizador.plotar_malha(malha, title=f"Nível {i}", ax=ax) # Desenha a malha específica naquele subgráfico

        plt.tight_layout() # Ajusta automaticamente o espaçamento entre os subgráficos
        plt.show() # Abre a janela com a progressão completa

    @staticmethod # Define método estático para gráfico interativo
    def plot_interativo(malhas, metricas_por_nivel=None): # Cria janela com slider para navegar pelos níveis
        """Cria um gráfico interativo com um slider e painel de estatísticas.""" # Docstring
        fig = plt.figure(figsize=(11, 9)) # Cria figura levemente maior para as estatísticas
        ax = fig.add_subplot(111, projection='3d') # Cria o eixo 3D principal
        plt.subplots_adjust(bottom=0.2, top=0.95) # Reserva espaço para o slider e margem superior

        # Função para plotar um nível específico # Função interna de atualização (callback)
        def atualizar_plot(val): # val recebe o valor do nível vindo do slider
            nv = int(slider_nivel.val) # Pega o nível atual do slider correspondente
            
            ax.clear() # Limpa o desenho anterior (malha e texto)
            malha = malhas[nv] # Pega a malha correspondente ao nível
            
            Visualizador.plotar_malha(malha, title=f"Subdivisão de Loop - Nível {nv}", 
                               mostrar_wireframe=True, mostrar_superficie=True, ax=ax,
                               intensidade_luz=1.0) # Redesenha com iluminação total fixa

            # --- ADICIONA ESTATÍSTICAS EM TEMPO REAL ---
            if metricas_por_nivel:
                m = metricas_por_nivel[nv]
                texto_estatisticas = (
                    f"Estatísticas Nível {nv}:\n"
                    f"Vértices: {m['num_vertices']}\n"
                    f"Faces: {m['num_faces']}\n"
                    f"Erro Médio Raio: {m['erro_medio']:.6f}\n"
                    f"Desvio Área: {m['desvio_padrao_area']:.6f}"
                )
                # Adiciona texto no canto superior esquerdo (coordenadas 2D da figura)
                ax.text2D(0.05, 0.95, texto_estatisticas, transform=ax.transAxes, 
                          fontsize=11, family='monospace', verticalalignment='top',
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

            fig.canvas.draw_idle() # Atualiza a tela de forma eficiente

        # Configurar Slider # Criação do componente visual
        ax_nivel = plt.axes([0.2, 0.05, 0.6, 0.03]) # Posição do slider de Nível
        
        slider_nivel = Slider(ax_nivel, 'Nível', 0, len(malhas)-1, valinit=0, valstep=1)

        # Conectar evento # Liga o movimento do slider à função de atualização
        slider_nivel.on_changed(atualizar_plot)

        # Plot inicial
        atualizar_plot(None) # Chama o plot inicial manualmente

        plt.show() # Inicia o loop de eventos da interface gráfica
