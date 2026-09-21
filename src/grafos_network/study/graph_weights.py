import networkx as nx 
import matplotlib.pyplot as plt


G = nx.Graph()



G.add_edge("a", "b", weight=0.6)
G.add_edge("a", "c", weight=0.2)
G.add_edge("c", "d", weight=0.1)
G.add_edge("c", "e", weight=0.7)
G.add_edge("c", "f", weight=0.9)
G.add_edge("a", "d", weight=0.3)

pos = nx.spring_layout(G, seed=42)
weights = nx.get_edge_attributes(G, "weight")

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=1800,
    font_size=14,
    width=[peso * 5 for peso in weights.values()]
)

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=weights,
    font_size=12
)

plt.show()