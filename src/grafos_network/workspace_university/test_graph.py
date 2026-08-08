import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


numberToLetter = {
    1: "C",
    2: "Q",
    3: "T",
    4: "E"
}


MATRIZ = np.array([
    [2, 3, 1, 3, 1, 2],
    [3, 3, 2, 1, 2, 3],
    [1, 2, 3, 2, 3, 1],
    [3, 1, 2, 4, 3, 3],
    [1, 2, 3, 2, 3, 1],
    [2, 3, 1, 1, 2, 3]
])


G = nx.Graph()

pos = {
    (linha, coluna): (coluna, -linha)
    for linha in range(MATRIZ.shape[0])
    for coluna in range(MATRIZ.shape[1])
}


for linha in range(MATRIZ.shape[0]):
    for coluna in range(MATRIZ.shape[1]):

        node = (linha, coluna)

        G.add_node(
            node,
            tipo=numberToLetter[MATRIZ[linha][coluna]]
        )


formatos = {
    "C": ("o", "blue"),
    "Q": ("s", "black"),
    "T": ("^", "green"),
    "E": ("*", "yellow")
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


plt.axis("off")
plt.axis("equal")
plt.show()