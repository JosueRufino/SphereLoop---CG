import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Slider
import numpy as np

class Visualizer:
    """
    Classe responsável pela renderização 3D da malha usando Matplotlib.
    """
    @staticmethod
    def plot_mesh(mesh, title="Subdivision level", show_wireframe=True, show_surface=True, ax=None):
        if ax is None:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
        
        vertices = mesh.vertices
        faces = mesh.faces
        
        if show_surface:
            # Criar coleção de polígonos para a superfície
            poly3d = [[vertices[idx] for idx in face] for face in faces]
            
            # Cálculo simples de sombreamento baseado na normal (opcional para estética)
            collection = Poly3DCollection(poly3d, alpha=0.8, facecolors='cyan', edgecolors='black' if show_wireframe else 'none')
            ax.add_collection3d(collection)
        
        elif show_wireframe:
            # Se apenas wireframe for solicitado
            for face in faces:
                v = vertices[face]
                v = np.vstack([v, v[0]]) # Fechar o triângulo
                ax.plot(v[:,0], v[:,1], v[:,2], color='black', linewidth=0.5)

        # Ajustar limites e labels
        limit = 1.1
        ax.set_xlim([-limit, limit])
        ax.set_ylim([-limit, limit])
        ax.set_zlim([-limit, limit])
        ax.set_title(title)
        ax.axis('off') # Remove eixos para foco na esfera

    @staticmethod
    def show_progression(meshes):
        """Mostra a evolução da subdivisão lado a lado."""
        num_levels = len(meshes)
        fig = plt.figure(figsize=(5 * num_levels, 5))
        
        for i, mesh in enumerate(meshes):
            ax = fig.add_subplot(1, num_levels, i + 1, projection='3d')
            Visualizer.plot_mesh(mesh, title=f"Nível {i}", ax=ax)
            
        plt.tight_layout()
        plt.show()

    @staticmethod
    def interactive_plot(meshes):
        """Cria um gráfico interativo com um slider para escolher o nível de subdivisão."""
        fig = plt.figure(figsize=(10, 9))
        ax = fig.add_subplot(111, projection='3d')
        plt.subplots_adjust(bottom=0.2) # Espaço para o slider

        # Função para plotar um nível específico
        def update_plot(level):
            ax.clear()
            mesh = meshes[int(level)]
            Visualizer.plot_mesh(mesh, title=f"Loop Subdivision - Nível {int(level)}", 
                               show_wireframe=True, show_surface=True, ax=ax)
            fig.canvas.draw_idle()

        # Configurar o Slider
        ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
        slider = Slider(ax_slider, 'Nível', 0, len(meshes)-1, valinit=len(meshes)-1, valstep=1)
        
        # Conectar evento do slider
        slider.on_changed(update_plot)
        
        # Plot inicial
        update_plot(len(meshes)-1)
        
        plt.show()
