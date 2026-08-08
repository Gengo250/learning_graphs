import networkx as nx 
import matplotlib.pyplot as plt

#Graph city
#adiconar cidade 
#adicionar estrada 
#mostrar vizinhos 
#remover estrada 
#remover cidade 

C = nx.Graph()

#adicionar cidade 
C.add_node("Sao Paulo")
C.add_node("Niteroi")
C.add_node("Rio de Janeiro")
C.add_node("Ubatuba")

#adicionar estrada 
C.add_edges_from([("Sao Paulo", "Rio de Janeiro"), ("Ubatuba", "Niteroi"), ("Ubatuba", "Sao Paulo")])


print(C.number_of_nodes())
print(C.number_of_edges())
print(C.nodes)

pos = nx.spring_layout(C)

nx.draw(
    C,
    with_labels=True,
    font_weight="bold"
)

plt.show()