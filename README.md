# Renderização de Esfera com Subdivisão de Loop

Este projeto faz parte do trabalho sobre **"Algoritmos de Subdivisão para Exibição de Superfícies Curvas em Computadores"**. Ele implementa o algoritmo de **Loop Subdivision** para transformar um icosaedro inicial em uma esfera suave.

## 📋 Funcionamento do Algoritmo

O algoritmo de Loop é um esquema de subdivisão aproximada que trabalha com malhas triangulares. Para cada iteração:

1. **Refinamento Topológico**: Cada triângulo é dividido em 4 novos triângulos menores.
2. **Cálculo de Novos Vértices (Odd Vertices)**: Posicionados nas arestas existentes usando uma média ponderada dos vértices adjacentes.
3. **Atualização de Vértices Existentes (Even Vertices)**: Reposicionados para suavizar a malha usando pesos β.

### Fórmulas Matemáticas

- **Peso Beta (β)**: Para um vértice de grau $n$, se $n > 3$:
  $$\beta = \frac{1}{n} \left( \frac{5}{8} - \left( \frac{3}{8} + \frac{1}{4} \cos \frac{2\pi}{n} \right)^2 \right)$$
  Se $n = 3$, $\beta = 3/16$.

## 📁 Estrutura do Projeto (Refatorado para Português)

```
EsferaLoop - CG/
├── src/
│   └── esferaloop/           # Pacote principal
│       ├── nucleo/           # Algoritmos e estruturas de dados (Malha e Subdivisão)
│       │   ├── malha.py      # Estrutura de dados da malha e gerador de icosaedro
│       │   └── subdivisao_loop.py  # Lógica central do algoritmo de Loop
│       ├── visualizacao/     # Renderização 3D e interface
│       │   └── renderizador.py # Renderização usando Matplotlib
│       └── utilitarios/      # Utilitários e métricas
│           └── metricas.py    # Ferramentas para análise de convergência e áreas
├── exemplos/                 # Scripts de demonstração
│   ├── demo_basica.py         # Exemplo básico de uso
│   └── demo_interativa.py     # Demo interativa com sliders de nível e luz
├── documentacao/             # Documentação detalhada
└── testes/                   # Testes (estrutura preparada)
```

## 🔧 Requisitos

- Python 3.x
- NumPy
- Matplotlib

### Instalação de Dependências

```bash
pip install numpy matplotlib
```

## 🚀 Como Rodar

### Demonstração Básica

Executa o algoritmo com 4 níveis de subdivisão e mostra a progressão:

```bash
python exemplos/demo_basica.py
```

### Demonstração Interativa

Abre uma interface com sliders para navegar entre os níveis e ajustar a iluminação em tempo real:

```bash
python exemplos/demo_interativa.py
```

## 📊 Resultados e Métricas de Qualidade

O algoritmo gera estatísticas detalhadas para cada nível:
- **Número de Vértices e Faces**: Acompanhamento do crescimento da malha.
- **Erro Médio de Raio**: Validação da esfericidade.
- **Desvio Padrão da Área**: Avaliação da distribuição uniforme dos polígonos.

## 🎓 Contexto Acadêmico

Este projeto demonstra como algoritmos de subdivisão podem transformar malhas poligonais grossas em superfícies suaves, sendo vital para o estudo de Computação Gráfica e modelagem geométrica.
