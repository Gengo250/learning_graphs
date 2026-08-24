import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_weighted_edges_from([
    ("A", "B", 1),
    ("A", "C", 4),
    ("B", "C", 2),
    ("B", "D", 5),
    ("C", "D", 1),
    ("C", "E", 3),
    ("D", "E", 2)
])

arvore = nx.minimum_spanning_tree(G)

pos = nx.spring_layout(G, seed=42)

nx.draw(
    arvore,
    pos,
    with_labels=True,
    node_size=1000
)

pesos = nx.get_edge_attributes(arvore, "weight")

nx.draw_networkx_edge_labels(
    arvore,
    pos,
    edge_labels=pesos
)

plt.show()