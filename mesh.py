import numpy as np

class Mesh:
    """
    Classe para representar uma malha triangular 3D.
    Armazena vértices e faces, e fornece métodos para manipulação da topologia.
    """
    def __init__(self, vertices=None, faces=None):
        # Vertices: array numpy de formato (N, 3)
        self.vertices = np.array(vertices, dtype=float) if vertices is not None else np.empty((0, 3))
        # Faces: array numpy de formato (M, 3) contendo índices de vértices
        self.faces = np.array(faces, dtype=int) if faces is not None else np.empty((0, 3), dtype=int)

    def get_edges(self):
        """
        Extrai todas as arestas únicas da malha.
        Retorna um dicionário mapeando arestas (tupla ordenada) para faces adjacentes.
        """
        edges = {}
        for f_idx, face in enumerate(self.faces):
            for i in range(3):
                v1, v2 = face[i], face[(i + 1) % 3]
                edge = tuple(sorted((v1, v2)))
                if edge not in edges:
                    edges[edge] = []
                edges[edge].append(f_idx)
        return edges

    @staticmethod
    def generate_icosahedron():
        """
        Gera um icosaedro regular centrado na origem como malha inicial (Nível 0).
        Um icosaedro possui 12 vértices e 20 faces triangulares.
        """
        phi = (1 + np.sqrt(5)) / 2  # Proporção áurea
        
        # Vértices de um icosaedro regular
        vertices = [
            [-1,  phi,  0], [ 1,  phi,  0], [-1, -phi,  0], [ 1, -phi,  0],
            [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi],
            [ phi,  0, -1], [ phi,  0,  1], [-phi,  0, -1], [-phi,  0,  1]
        ]
        
        # Normalizar para que fiquem na esfera unitária (raio = 1)
        vertices = np.array(vertices)
        vertices /= np.linalg.norm(vertices, axis=1)[:, np.newaxis]

        # 20 faces triangulares
        faces = [
            [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
            [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
            [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
            [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
        ]
        
        return Mesh(vertices, faces)

    def stats(self):
        """Retorna contagem de vértices e faces."""
        return len(self.vertices), len(self.faces)
