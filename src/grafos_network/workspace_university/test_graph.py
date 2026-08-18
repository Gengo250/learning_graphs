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


G = nx.DiGraph()

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


arestas = []

direcoes = [
    (-1,  0),
    (-1,  1),
    ( 0,  1),
    ( 1,  1),
    ( 1,  0),
    ( 1, -1),
    ( 0, -1),
    (-1, -1)
]


# CÍRCULO -> QUADRADO

quadrados_encontrados = set()

for linha in range(MATRIZ.shape[0]):
    for coluna in range(MATRIZ.shape[1]):

        if MATRIZ[linha][coluna] == 1:

            for dl, dc in direcoes:

                nova_linha = linha + dl
                nova_coluna = coluna + dc

                if (
                    0 <= nova_linha < MATRIZ.shape[0]
                    and
                    0 <= nova_coluna < MATRIZ.shape[1]
                ):

                    if MATRIZ[nova_linha][nova_coluna] == 2:

                        arestas.append(
                            (
                                (linha, coluna),
                                (nova_linha, nova_coluna)
                            )
                        )

                        quadrados_encontrados.add(
                            (nova_linha, nova_coluna)
                        )


# QUADRADO -> TRIÂNGULO

direcoes_quadrado = [
    (0, 1),  # direita
    (1, 0)   # baixo
]

triangulos_encontrados = set()

for linha, coluna in quadrados_encontrados:

    for dl, dc in direcoes_quadrado:

        nova_linha = linha + dl
        nova_coluna = coluna + dc

        if (
            0 <= nova_linha < MATRIZ.shape[0]
            and
            0 <= nova_coluna < MATRIZ.shape[1]
        ):

            if MATRIZ[nova_linha][nova_coluna] == 3:

                arestas.append(
                    (
                        (linha, coluna),
                        (nova_linha, nova_coluna)
                    )
                )

                triangulos_encontrados.add(
                    (nova_linha, nova_coluna)
                )


# ENCONTRAR A ESTRELA

estrela = None

for linha in range(MATRIZ.shape[0]):
    for coluna in range(MATRIZ.shape[1]):

        if MATRIZ[linha][coluna] == 4:
            estrela = (linha, coluna)


# TRIÂNGULOS -> ESTRELA

for triangulo in triangulos_encontrados:

    arestas.append(
        (
            triangulo,
            estrela
        )
    )


G.add_edges_from(arestas)


nx.draw_networkx_edges(
    G,
    pos
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