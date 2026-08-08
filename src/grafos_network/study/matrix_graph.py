import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

matriz = np.array([
    [0, 1, 1, 0],
    [1, 0, 1, 0],
    [1, 1, 0, 1],
    [0, 0, 1, 0]
])

G = nx.from_numpy_array(matriz)

nx.draw(
    G,
    with_labels=False
)

plt.show()