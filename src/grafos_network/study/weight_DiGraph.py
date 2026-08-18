import networkx as nx
import matplotlib.pyplot as plt


DG = nx.DiGraph()

paths = [
    (1, 2, 0.8),
    (2, 3, 0.9),
    (3, 1, 0.6),
    (4, 2, 0.55)
]

DG.add_weighted_edges_from(paths)

pos = nx.spring_layout(DG, seed=42)

nx.draw(
    DG,
    pos=pos,
    with_labels=True
)

weights = nx.get_edge_attributes(DG, "weight")

nx.draw_networkx_edge_labels(
    DG,
    pos=pos,
    edge_labels=weights
)

plt.show()