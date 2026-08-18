import networkx as nx
import matplotlib.pyplot as plt

MATRIZ = [
    [2, 3, 1, 3, 1, 2],
    [3, 3, 2, 1, 2, 3],
    [1, 2, 3, 2, 3, 1],
    [3, 1, 2, 2, 3, 3],
    [1, 2, 3, 2, 3, 1],
    [2, 3, 1, 1, 2, 3]
]

G = nx.Graph()

pos = {}

for linha, valores in enumerate(MATRIZ):
    for coluna, valor in enumerate(valores):
        node = (linha, coluna)
        G.add_node(node, tipo=valor)
        pos[node] = (coluna, -linha)

formatos = {
    1: ("o", "blue"),
    2: ("s", "black"),
    3: ("^", "green")
}

for tipo, (forma, cor) in formatos.items():
    nodes = [
        node
        for node in G.nodes
        if G.nodes[node]["tipo"] == tipo
    ]

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=nodes,
        node_shape=forma,
        node_color=cor,
        node_size=700
    )

x_nodes = {
    (0, 2),
    (2, 0),
    (4, 5)
}

labels_x = {
    node: "X"
    for node in x_nodes
}

nx.draw_networkx_labels(
    G,
    pos,
    labels=labels_x,
    font_color="black",
    font_size=12,
    font_weight="bold"
)

plt.axis("off")
plt.axis("equal")
plt.show()