import networkx as nx 
import matplotlib.pyplot as plt


#Graph friends 
#Seu programa deve:

#adicionar 6 pessoas;
#adicionar amizades;
#imprimir todos os nós;
#imprimir todas as arestas;
#mostrar os amigos de uma pessoa;
#mostrar o grau de cada pessoa;

G = nx.Graph()

G.add_nodes_from(["Miguel", "Joao", "Guilherme", "Rodrigo", "Gabrieal"])
G.add_edges_from([("Miguel", "Arthur"), ("Guilherme", "Rodrigo"), ("Gabriel", "Joao"), ("Miguel", "Rodrigo")])

print(G.number_of_nodes())
print(G.number_of_edges())
print(G.nodes)

print(G.adj["Miguel"])

for pessoa, grau in G.degree:
    print(f"{pessoa}: {grau} amigos")

pos = nx.spring_layout(G)

nx.draw(
    G,
    with_labels=True,
    font_weight="bold"
)

plt.show()