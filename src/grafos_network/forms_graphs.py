import networkx as nx
import matplotlib.pyplot as plt

# "o"   círculo
# "s"   quadrado
# "^"   triângulo para cima
# "v"   triângulo para baixo
# ">"   triângulo direita
# "<"   triângulo esquerda
# "d"   losango fino
# "p"   pentágono
# "h"   hexágono
# "8"   octógono

G = nx.DiGraph()

G.add_edges_from([
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (2, 5)
])

pos = nx.spring_layout(G, seed=42)

circulos = [1, 4]
quadrados = [2, 5]
triangulos = [3]

nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowsize=20
)

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=circulos,
    node_shape="o",
    node_color="blue",
    node_size=700
)

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=quadrados,
    node_shape="s",
    node_color="black",
    node_size=700
)

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=triangulos,
    node_shape="^",
    node_color="green",
    node_size=700
)


plt.axis("off")
plt.show()

