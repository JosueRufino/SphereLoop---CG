import numpy as np
import time

def get_mesh_metrics(mesh, target_radius=1.0):
    """
    Calcula métricas de qualidade da malha.
    - Contagem de elementos
    - Erro de raio (distância média ao centro)
    - Desvio padrão do raio (suavidade da forma)
    """
    vertices = mesh.vertices
    faces = mesh.faces
    
    # Radii de todos os vértices (distância da origem)
    radii = np.linalg.norm(vertices, axis=1)
    
    # Erro médio em relação ao raio alvo
    mean_radius = np.mean(radii)
    max_radius = np.max(radii)
    min_radius = np.min(radii)
    
    error_avg = np.mean(np.abs(radii - target_radius))
    std_radius = np.std(radii)
    
    return {
        "num_vertices": len(vertices),
        "num_faces": len(faces),
        "error_avg": error_avg,
        "std_radius": std_radius,
        "min_radius": min_radius,
        "max_radius": max_radius
    }

def print_stats_table(all_metrics):
    """Exibe uma tabela formatada com as estatísticas de cada nível."""
    print("\n" + "="*80)
    print(f"{'Nível':<6} | {'Vértices':<8} | {'Faces':<8} | {'Erro Médio':<12} | {'Desvio Padrão':<12}")
    print("-" * 80)
    for i, meta in enumerate(all_metrics):
        print(f"{i:<6} | {meta['num_vertices']:<8} | {meta['num_faces']:<8} | {meta['error_avg']:<12.6f} | {meta['std_radius']:<12.6f}")
    print("="*80 + "\n")
