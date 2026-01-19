import numpy as np
from mesh import Mesh
from visualization import Visualizer
from metrics import get_mesh_metrics, print_stats_table

class LoopSubdivisionSphere:
    """
    Implementação do algoritmo de subdivisão de Loop para malhas triangulares.
    Transforma uma malha grossa em uma superfície suave através de refinamento iterativo.
    """
    def __init__(self, subdivision_levels=2, normalize_each_step=False):
        self.levels = subdivision_levels
        self.normalize_each_step = normalize_each_step
        self.meshes = [] # Armazena malhas de cada nível
        self.run()

    def run(self):
        """Executa a subdivisão até o nível desejado começando de um icosaedro."""
        mesh = Mesh.generate_icosahedron()
        if self.normalize_each_step:
            mesh = self.normalize_to_sphere(mesh)
        self.meshes.append(mesh)
        
        for k in range(self.levels):
            print(f"Subdividindo nível {k} -> {k+1}...")
            mesh = self.subdivide(mesh)
            if self.normalize_each_step:
                mesh = self.normalize_to_sphere(mesh)
            self.meshes.append(mesh)
        return self.meshes[-1]

    def subdivide(self, mesh):
        """
        Aplica uma iteração do algoritmo de Loop.
        1. Cria novos 'odd vertices' nas arestas.
        2. Atualiza 'even vertices' (originais).
        3. Reconecta para formar 4 novos triângulos por face original.
        """
        vertices = mesh.vertices
        faces = mesh.faces
        edges = mesh.get_edges()
        
        # 1. Calcular Novos Vértices nas Arestas (Odd Vertices)
        new_vertices = list(vertices)
        edge_to_new_vertex = {}
        
        for edge, adj_faces in edges.items():
            v1_idx, v2_idx = edge
            v1, v2 = vertices[v1_idx], vertices[v2_idx]
            
            # Se a aresta for compartilhada por duas faces (malha fechada)
            if len(adj_faces) == 2:
                # Encontrar os vértices opostos nas duas faces
                opposite_vertices = []
                for f_idx in adj_faces:
                    face = faces[f_idx]
                    for v_idx in face:
                        if v_idx not in edge:
                            opposite_vertices.append(vertices[v_idx])
                            break
                
                v3, v4 = opposite_vertices[0], opposite_vertices[1]
                # Regra do Loop para odd vertices: 3/8 * (v1 + v2) + 1/8 * (v3 + v4)
                new_v = (3/8) * (v1 + v2) + (1/8) * (v3 + v4)
            else:
                # Caso de borda (não esperado para uma esfera/icosaedro, mas bom para robustez)
                new_v = 0.5 * (v1 + v2)
            
            edge_to_new_vertex[edge] = len(new_vertices)
            new_vertices.append(new_v)
            
        # 2. Atualizar Vértices Originais (Even Vertices)
        updated_vertices = np.copy(np.array(new_vertices))
        
        # Mapear adjacência de vértices
        v_adj = {}
        for edge in edges.keys():
            v1, v2 = edge
            if v1 not in v_adj: v_adj[v1] = []
            if v2 not in v_adj: v_adj[v2] = []
            v_adj[v1].append(v2)
            v_adj[v2].append(v1)
            
        for v_idx in range(len(vertices)):
            neighbors = v_adj.get(v_idx, [])
            n = len(neighbors)
            
            if n > 0:
                # Cálculo do peso Beta
                if n == 3:
                    beta = 3/16
                else:
                    beta = (1/n) * (5/8 - (3/8 + 0.25 * np.cos(2 * np.pi / n))**2)
                
                sum_neighbors = np.sum(vertices[neighbors], axis=0)
                # Regra: (1 - n*beta) * v_original + beta * sum(v_neighbors)
                updated_vertices[v_idx] = (1 - n * beta) * vertices[v_idx] + beta * sum_neighbors

        # 3. Gerar Novas Faces
        new_faces = []
        for face in faces:
            v1, v2, v3 = face
            
            # Obter índices dos novos vértices nas arestas
            a = edge_to_new_vertex[tuple(sorted((v1, v2)))]
            b = edge_to_new_vertex[tuple(sorted((v2, v3)))]
            c = edge_to_new_vertex[tuple(sorted((v3, v1)))]
            
            # Cada triângulo original v1-v2-v3 vira 4 triângulos:
            # (v1, a, c), (v2, b, a), (v3, c, b), (a, b, c)
            new_faces.append([v1, a, c])
            new_faces.append([v2, b, a])
            new_faces.append([v3, c, b])
            new_faces.append([a, b, c])
            
        return Mesh(updated_vertices, np.array(new_faces))

    def normalize_to_sphere(self, mesh):
        """Normaliza todos os vértices para raio 1 (projeção na esfera)."""
        norms = np.linalg.norm(mesh.vertices, axis=1)[:, np.newaxis]
        mesh.vertices /= norms
        return mesh

    def visualize(self, level=-1, show_wireframe=True, show_surface=True):
        """Visualiza a malha do nível especificado (padrão: último nível)."""
        Visualizer.plot_mesh(self.meshes[level], title=f"Esfera Subdividida - Nível {len(self.meshes)-1 if level == -1 else level}", 
                           show_wireframe=show_wireframe, show_surface=show_surface)
        import matplotlib.pyplot as plt
        plt.show()

    def show_progression(self):
        """Mostra evolução da subdivisão lado a lado."""
        Visualizer.show_progression(self.meshes)

    def print_statistics(self):
        """Exibe métricas de todos os níveis processados."""
        all_metrics = [get_mesh_metrics(m) for m in self.meshes]
        print_stats_table(all_metrics)

    def interactive_demo(self):
        """Inicia a visualização interativa com slider."""
        Visualizer.interactive_plot(self.meshes)
