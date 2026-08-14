# Requisitos:

#     Não adicionar arestas manualmente, as arestas devem ser adicionadas automaticamente, dependendo da matriz (para um exemplo de matriz, vejam o código de referênciaDownload código de referência)
#     Os nós devem ser coloridos
#     Os nós devem estar posicionados em uma grade conforme a referência
#     Os nós devem ter seus formatos respeitados
#     Não podem haver arestas sobrepostas (cruzar pode)
#     Marcar todos os nós finais passo 4 com estrela
#     Marcar todos os nos finais interrompidos (sem possibilidade de passo seguinte) com X
#     As distâncias são contadas em passos apenas nas 8 direções principais (norte, nordeste, leste, sudeste, sul, sudoeste, oeste, noroeste); meias diagonais não são alcançãveis (distância infinita).)
#     Deve ser submetido o código-fonte em python notebook e utilizar a biblioteca networkX

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

# Sigam os seguintes passosa:
# 1 - Escolher um círculo qualquer
# 2 - Ir para o quadrado mais próximo 
# 3 - Ir para o triângulo mais próximo, apenas à direita ou abaixo do quadrado
# 4 - Ir para o quadrado mais próximo apenas diagonais

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

MATRIZ = np.array ([  
    [2,3,1,3,1,2],
    [3,3,2,1,2,3],
    [1,2,3,2,3,1],
    [3,1,2,2,3,3],
    [1,2,3,2,3,1],
    [2,3,1,1,2,3]
])


numberToLetter = {
    1: "C",
    2: "Q",
    3: "T",
    4: "E"
}


G = nx.from_numpy_array(MATRIZ)

nx.draw(
    G,
    with_labels=False
)

plt.show()