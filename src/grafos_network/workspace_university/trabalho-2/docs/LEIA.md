# Trabalho 2 - Problema do Caminhão

Explicação teórica e de código do notebook `caminhao_networkx.ipynb`.

> - Fundamentação matemática completa (definições formais, teoremas com demonstração,
>   análise do algoritmo de Kruskal, complexidade, casos limites e roteiro de arguição):
>   [`TEORIA.md`](TEORIA.md).
> - Referência técnica de API (cada função, cada parâmetro, defaults, tipos e erros):
>   [`CODIGO.md`](CODIGO.md).

---

## 1. O problema

Um arquipélago tem `I` ilhas ligadas por `P` pontes. Cada ponte liga duas ilhas e tem um
**peso suportado**: o caminhão só atravessa aquela ponte se pesar no máximo esse valor.

Para cada uma das `S` consultas `X Y`, a pergunta é: **qual o caminhão mais pesado que
consegue sair da ilha `X` e chegar na ilha `Y`?**

### Formato de entrada

```
I P S
A1 B1 P1
A2 B2 P2
...
Ap Bp Pp
X1 Y1
X2 Y2
...
Xs Ys
```

As ilhas são numeradas a partir de 1. O arquivo pode conter vários casos de teste
seguidos: acabando as `S` consultas de um caso, a próxima linha já é o cabeçalho
`I P S` do caso seguinte.

Exemplo do enunciado:

```
4 5 4
1 2 9
1 3 0
2 3 8
2 4 7
3 4 4
1 4
2 1
3 1
4 3
```

Saída esperada:

```
7
9
8
7
```

---

## 2. Modelagem

O arquipélago é um **grafo não direcionado ponderado** `G = (V, E, w)`:

- vértices `V` = ilhas (`1..I`);
- arestas `E` = pontes;
- peso `w(e)` = carga máxima suportada pela ponte `e`.

Um caminhão que percorre um caminho `P = (e1, e2, ..., ek)` precisa passar por **todas**
as pontes do caminho. Logo o caminho inteiro só suporta o peso da sua ponte mais fraca:

```
capacidade(P) = min w(e)
                e ∈ P
```

Esse mínimo é o **gargalo** (bottleneck) do caminho. O caminhoneiro escolhe o caminho que
lhe for mais conveniente, então a resposta da consulta é o melhor gargalo possível:

```
resposta(X, Y) =  max        (  min   w(e) )
                caminhos P     e ∈ P
```

Isso é o **caminho de gargalo máximo** (*maximum bottleneck path*, também chamado de
*widest path*). É um problema **maximin**, e não de caminho mínimo: somar pesos não faz
sentido aqui, porque atravessar mais pontes não "gasta" capacidade — o que importa é
apenas a pior ponte da rota.

### Por que o caminho mais curto não serve

No exemplo do enunciado, a consulta `4 3` tem a ponte direta `4-3` de peso 4. Mas o desvio
`4 → 2 → 3` passa por pontes de peso 7 e 8, e seu gargalo é `min(7, 8) = 7`. Como 7 > 4, a
resposta é 7. O caminho ótimo é o mais longo em número de pontes.

Do mesmo modo, a ponte `1-3` tem peso 0: ela existe no grafo, mas nenhum caminhão com peso
positivo passa por ela, então ela nunca aparece em uma rota ótima quando há alternativa.

---

## 3. Fundamento teórico: árvore geradora máxima

A ideia central do notebook é:

> O caminho de gargalo máximo entre quaisquer dois vértices pode ser encontrado dentro de
> uma **árvore geradora máxima** (*maximum spanning tree*) do grafo.

Como a árvore é acíclica e conexa, existe **um único** caminho entre dois vértices dela.
Então basta pegar esse caminho único e calcular o mínimo dos seus pesos.

### Justificativa

Seja `T` uma árvore geradora máxima de `G`, e sejam `X` e `Y` dois vértices. Seja `PT` o
caminho único de `X` a `Y` dentro de `T`, com gargalo `b = min w(e)` para `e ∈ PT`.

Suponha, por absurdo, que exista em `G` um caminho `PG` de `X` a `Y` com gargalo
`b' > b`, ou seja, todas as arestas de `PG` têm peso maior que `b`.

Seja `f` a aresta de `PT` com peso `b` (a aresta mais fraca do caminho na árvore).
Removendo `f` de `T`, a árvore se parte em duas componentes: uma contendo `X` e outra
contendo `Y`. Como `PG` vai de `X` até `Y`, ele necessariamente tem alguma aresta `g` que
cruza essa mesma partição. Por hipótese, `w(g) > b = w(f)`.

Então `T - f + g` continua sendo uma árvore geradora (a troca reconecta as duas
componentes) e tem peso total **estritamente maior** que `T`. Isso contradiz `T` ser
máxima. Logo `b' > b` é impossível, e o caminho na árvore já é ótimo.

Esse é o mesmo argumento da **propriedade do corte** (*cut property*) usada para provar a
corretude de Kruskal e Prim, aplicado ao caso de maximização.

### Consequência prática

- A árvore é construída **uma vez por caso de teste**, com custo `O(P log P)`.
- Cada consulta vira uma busca de caminho em árvore, com custo `O(I)`.
- Com `S` consultas: `O(P log P + S · I)`, em vez de rodar um algoritmo de gargalo do zero
  para cada par.

### As "pontes de interesse"

As arestas que sobrevivem na árvore geradora máxima são exatamente as pontes que **podem
ser usadas** por algum caminhoneiro em alguma rota ótima. As pontes fora da árvore são
descartadas: para cada uma delas existe sempre uma rota alternativa dentro da árvore com
gargalo igual ou melhor. É isso que o notebook destaca em vermelho no segundo gráfico.

---

## 4. O código, célula a célula

### Célula 0 — imports e arquivo de entrada

```python
import networkx as nx
import matplotlib.pyplot as plt

arquivo = "testes/entrada.txt"
```

`networkx` fornece a estrutura de grafo e os algoritmos; `matplotlib` faz o desenho.
A variável `arquivo` aponta para o caso de teste que será processado — trocar esse caminho
é a única alteração necessária para rodar outro teste da pasta `testes/`.

### Célula 1 — `ler_casos(arquivo)`

```python
def ler_casos(arquivo):
    with open(arquivo, encoding="utf-8") as arquivo_entrada:
        linhas = [linha.split() for linha in arquivo_entrada if linha.strip()]
    ...
```

Lê o arquivo inteiro e quebra cada linha em tokens, ignorando linhas em branco
(`if linha.strip()`). Isso deixa a leitura imune a linhas vazias no meio ou no fim do
arquivo.

Depois, um laço `while` consome a lista com um cursor `indice`:

1. lê o cabeçalho `numero_ilhas, numero_pontes, numero_sedes`;
2. lê exatamente `numero_pontes` linhas como triplas `(origem, destino, peso)`;
3. lê exatamente `numero_sedes` linhas como pares `(sede, deposito)`;
4. empacota tudo num dicionário e repete enquanto sobrar linha.

É esse `while` que dá suporte a **múltiplos casos no mesmo arquivo**: como as quantidades
vêm no cabeçalho, o cursor sabe exatamente onde um caso termina e o próximo começa.

Retorno: lista de dicionários com as chaves `numero_ilhas`, `pontes` e `sedes`.

### Célula 2 — `criar_grafo(caso)`

```python
def criar_grafo(caso):
    grafo = nx.Graph()
    grafo.add_nodes_from(range(1, caso["numero_ilhas"] + 1))
    grafo.add_weighted_edges_from(caso["pontes"], weight="weight")
    return grafo
```

- `nx.Graph()` — grafo **não direcionado e simples**, que é a modelagem correta: uma ponte
  é atravessável nos dois sentidos.
- `add_nodes_from(range(1, I + 1))` — insere todas as ilhas explicitamente. Sem isso, uma
  ilha isolada (que não aparece em nenhuma ponte) simplesmente não existiria no grafo,
  porque `add_weighted_edges_from` só cria os vértices que aparecem em alguma aresta.
- `add_weighted_edges_from(pontes, weight="weight")` — insere as arestas a partir das
  triplas `(origem, destino, peso)`, guardando o peso no atributo `weight`, que é o nome
  padrão usado pelos algoritmos do NetworkX.

### Célula 3 — `resolver_caso(caso)`

```python
def resolver_caso(caso):
    grafo = criar_grafo(caso)

    arvore_maxima = nx.maximum_spanning_tree(
        grafo,
        weight="weight",
        algorithm="kruskal",
    )

    return grafo, arvore_maxima
```

`nx.maximum_spanning_tree` é a tradução direta da teoria da seção 3. Os parâmetros:

- `weight="weight"` — informa qual atributo da aresta é o peso a ser maximizado (o mesmo
  nome gravado em `criar_grafo`).
- `algorithm="kruskal"` — escolhe o algoritmo de Kruskal. Na versão de maximização, ele
  ordena as arestas por peso **decrescente** e adiciona cada uma se ela não fechar ciclo
  (controle feito por union-find). Complexidade `O(P log P)`.

A função retorna o grafo original e a árvore: o grafo é necessário para o desenho (para
mostrar também as pontes descartadas), a árvore é o que responde as consultas.

### Célula 4 — `responder_consulta` e `imprimir_consultas`

```python
def responder_consulta(arvore_maxima, inicio, fim):
    caminho = nx.shortest_path(arvore_maxima, inicio, fim)

    pesos_do_caminho = [
        arvore_maxima[origem][destino]["weight"]
        for origem, destino in zip(caminho, caminho[1:])
    ]

    peso_maximo = min(pesos_do_caminho)

    return caminho, peso_maximo
```

`nx.shortest_path` é chamado **sem o parâmetro `weight`**, e isso é intencional: sem peso,
ele roda uma BFS e devolve o caminho com menos arestas. Como a busca é feita **dentro da
árvore**, existe um único caminho entre `inicio` e `fim` — o caminho mais curto é o único
caminho. O papel da função aqui não é minimizar nada, é apenas recuperar esse caminho
único.

O `zip(caminho, caminho[1:])` transforma a lista de vértices `[a, b, c, d]` nos pares de
arestas consecutivas `(a,b), (b,c), (c,d)`. Para cada par, busca-se o peso em
`arvore_maxima[origem][destino]["weight"]`.

O `min(...)` desses pesos é o gargalo do caminho — e, pela demonstração da seção 3, é a
resposta da consulta.

```python
def imprimir_consultas(arvore_maxima, sedes):
    for inicio, fim in sedes:
        caminho, peso_maximo = responder_consulta(arvore_maxima, inicio, fim)
        print(f"{inicio} → {fim}")
        print(f"Caminho: {caminho}")
        print(f"Peso máximo: {peso_maximo}\n")
```

Percorre as consultas na ordem em que aparecem no arquivo e imprime, para cada uma, o
caminho encontrado e o peso máximo. O valor da linha `Peso máximo` é a resposta oficial do
problema; o caminho é impresso como evidência da rota escolhida.

### Célula 5 — `plotar_grafo_inicial`

```python
def plotar_grafo_inicial(grafo, posicoes, titulo):
    plt.figure(figsize=(8, 6))
    nx.draw_networkx(grafo, posicoes, with_labels=True, ...)

    pesos = nx.get_edge_attributes(grafo, "weight")
    nx.draw_networkx_edge_labels(grafo, posicoes, edge_labels=pesos)
    ...
```

Desenha o grafo de entrada completo. `nx.draw_networkx` faz nós, arestas e rótulos dos
nós de uma vez; `nx.get_edge_attributes(grafo, "weight")` devolve um dicionário
`(u, v) -> peso`, que é passado a `nx.draw_networkx_edge_labels` para escrever o peso
suportado em cima de cada ponte.

O argumento `posicoes` vem de fora justamente para que os dois gráficos do mesmo caso
usem o **mesmo layout**, permitindo comparar um com o outro.

### Célula 6 — `plotar_pontes_de_interesse`

```python
pontes_interesse = list(arvore_maxima.edges())

pontes_descartadas = [
    (origem, destino)
    for origem, destino in grafo.edges()
    if not arvore_maxima.has_edge(origem, destino)
]
```

Separa as arestas em dois conjuntos: as que ficaram na árvore geradora máxima (as pontes
que podem ser usadas pelos caminhoneiros) e as que ficaram de fora.

O desenho é feito em camadas, em vez de uma chamada única, para poder dar estilos
diferentes a cada conjunto:

- `nx.draw_networkx_nodes` + `nx.draw_networkx_labels` — as ilhas;
- `nx.draw_networkx_edges(..., edgelist=pontes_descartadas, ...)` — cinza claro,
  tracejado;
- `nx.draw_networkx_edges(..., edgelist=pontes_interesse, ...)` — vermelho, mais grosso;
- `nx.draw_networkx_edge_labels` — os pesos, sobre todas as arestas.

Como as camadas são desenhadas nessa ordem, as pontes de interesse ficam por cima das
descartadas. Ao final, a função também imprime as duas listas com seus pesos, dando a
resposta textual do item "evidenciar pontes de interesse".

### Célula 7 — execução

```python
casos = ler_casos(arquivo)

print("Casos no arquivo:", len(casos), "\n")

for numero_caso, caso in enumerate(casos, 1):
    grafo, arvore_maxima = resolver_caso(caso)
    ...
    posicoes = nx.spring_layout(grafo, seed=42)

    plotar_grafo_inicial(...)
    plotar_pontes_de_interesse(...)

    print()
    imprimir_consultas(arvore_maxima, caso["sedes"])
```

Junta tudo: lê todos os casos do arquivo e, para cada um, constrói o grafo e a árvore,
imprime ilhas e pontes, desenha os dois gráficos e responde as consultas.

`nx.spring_layout` calcula as posições dos nós por um modelo de força (nós ligados se
atraem, nós em geral se repelem). O `seed=42` fixa o gerador aleatório do layout, de modo
que o desenho é sempre o mesmo entre execuções e os dois gráficos do mesmo caso ficam
alinhados.

`enumerate(casos, 1)` numera os casos a partir de 1 apenas para a rotulagem da saída.

---

## 5. Resumo do fluxo

```
arquivo .txt
     │
     ▼
ler_casos ─────────────► lista de casos {ilhas, pontes, consultas}
     │
     ▼
criar_grafo ───────────► nx.Graph ponderado
     │
     ▼
nx.maximum_spanning_tree (Kruskal, pesos decrescentes)
     │
     ├──► plotar_pontes_de_interesse  (pontes usáveis × descartadas)
     │
     ▼
nx.shortest_path na árvore  ──►  caminho único X→Y
     │
     ▼
min(pesos do caminho)  ──►  peso máximo do caminhão
```

---

## 6. Como executar

1. Colocar o arquivo de entrada na pasta `testes/`.
2. Ajustar a variável `arquivo` na primeira célula com o caminho do arquivo desejado.
3. Executar as células na ordem (as células 1 a 6 apenas definem funções; a célula 7 roda
   tudo).

Arquivos disponíveis em `testes/`:

| Arquivo | Conteúdo |
|---|---|
| `entrada.txt` | exemplo do enunciado |
| `teste_1_exemplo.txt` | exemplo oficial do enunciado |
| `teste_2_ponte_critica.txt` | dois blocos ligados por ponte de gargalo |
| `teste_3_multiplos_casos.txt` | três casos no mesmo arquivo |
| `teste_4_grafo_maior.txt` | 10 ilhas, 16 pontes, respostas sempre por desvio |

As respostas esperadas de cada arquivo estão em `testes/GABARITO.md`.

---

## 7. Funções do NetworkX usadas

| Função | Papel no trabalho |
|---|---|
| `nx.Graph()` | grafo não direcionado, modelagem das pontes de mão dupla |
| `add_nodes_from` | garante que ilhas sem ponte existam no grafo |
| `add_weighted_edges_from` | insere as pontes com o peso no atributo `weight` |
| `nx.maximum_spanning_tree(G, weight, algorithm="kruskal")` | árvore geradora máxima; contém os caminhos de gargalo máximo |
| `nx.shortest_path(T, x, y)` | recupera o caminho único entre `x` e `y` dentro da árvore (BFS, sem peso) |
| `nx.get_edge_attributes(G, "weight")` | dicionário de pesos para rotular as arestas no desenho |
| `nx.spring_layout(G, seed=42)` | posições reprodutíveis dos nós |
| `nx.draw_networkx` | desenho completo do grafo inicial |
| `nx.draw_networkx_nodes` / `_labels` / `_edges` / `_edge_labels` | desenho em camadas, para estilizar pontes de interesse e descartadas |
