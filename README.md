# Loop Subdivision Sphere Rendering

Este projeto faz parte do trabalho sobre "Algoritmos de Subdivisão para Exibição de Superfícies Curvas em Computadores". Ele implementa o algoritmo de **Loop Subdivision** para transformar um icosaedro inicial em uma esfera suave.

## Funcionamento do Algoritmo

O algoritmo de Loop é um esquema de subdivisão aproximada que trabalha com malhas triangulares. Para cada iteração:
1. **Refinamento Topológico**: Cada triângulo é dividido em 4 novos triângulos menores.
2. **Cálculo de Novos Vértices (Odd Vertices)**: Posicionados nas arestas existentes usando uma média ponderada dos vértices adjacentes.
3. **Atualização de Vértices Existentes (Even Vertices)**: Reposicionados para suavizar a malha usando pesos $\beta$.

### Fórmulas Matemáticas
- **Peso Beta ($\beta$)**: Para um vértice de grau $n$, se $n > 3$:
  $$\beta = \frac{1}{n} \left( \frac{5}{8} - \left( \frac{3}{8} + \frac{1}{4} \cos \frac{2\pi}{n} \right)^2 \right)$$
  Se $n = 3$, $\beta = 3/16$.

## Estrutura do Projeto
- `main.py`: Ponto de entrada e exemplo de uso.
- `loop_subdivision.py`: Lógica central do algoritmo de Loop.
- `mesh.py`: Estrutura de dados da malha e gerador de icosaedro.
- `visualization.py`: Renderização 3D usando Matplotlib.
- `metrics.py`: Ferramentas para análise de convergência e estatísticas.

## Requisitos
- Python 3.x
- NumPy
- Matplotlib

## Como Rodar
```bash
python main.py
```
