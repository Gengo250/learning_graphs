# Trabalho 2 — Referência Completa do Código

Documentação exaustiva do notebook `caminhao_networkx.ipynb`: **cada célula, cada função,
cada parâmetro**, com assinaturas reais, valores padrão, tipos de retorno e justificativa de
uso.

> **Trilogia de documentos**
> - `LEIA.md` — visão geral do trabalho e explicação célula a célula.
> - `TEORIA.md` — matemática: definições, teoremas, demonstrações, complexidade.
> - `CODIGO.md` *(este)* — referência técnica de API: parâmetros, defaults, tipos, erros.

> **Versões verificadas neste projeto:** NetworkX `3.6.1`, matplotlib `3.11.1`, Python 3.
> Todas as assinaturas, valores padrão e comportamentos descritos aqui foram conferidos
> diretamente no código-fonte instalado em `.venv/` e/ou executando o interpretador.

---

## Sumário

1. [Visão geral e inventário](#1-visão-geral-e-inventário)
2. [Célula 0 — imports e configuração](#2-célula-0--imports-e-configuração)
3. [Célula 1 — `ler_casos`](#3-célula-1--ler_casos)
4. [Célula 2 — `criar_grafo`](#4-célula-2--criar_grafo)
5. [Célula 3 — `resolver_caso`](#5-célula-3--resolver_caso)
6. [Célula 4 — `responder_consulta` e `imprimir_consultas`](#6-célula-4--responder_consulta-e-imprimir_consultas)
7. [Célula 5 — `plotar_grafo_inicial`](#7-célula-5--plotar_grafo_inicial)
8. [Célula 6 — `plotar_pontes_de_interesse`](#8-célula-6--plotar_pontes_de_interesse)
9. [Célula 7 — execução](#9-célula-7--execução)
10. [Tabela mestra de parâmetros usados](#10-tabela-mestra-de-parâmetros-usados)
11. [Parâmetros não usados que valem conhecer](#11-parâmetros-não-usados-que-valem-conhecer)
12. [Sintaxe e built-ins de Python usados](#12-sintaxe-e-built-ins-de-python-usados)
13. [Fluxo de dados e tipos](#13-fluxo-de-dados-e-tipos)
14. [Erros possíveis e o que significam](#14-erros-possíveis-e-o-que-significam)
15. [Como adaptar o notebook](#15-como-adaptar-o-notebook)

---

## 1. Visão geral e inventário

### 1.1 Estrutura do notebook

| Célula | Tipo | Conteúdo | Executa algo? |
|---|---|---|---|
| 0 | código | imports + variável `arquivo` | sim (define estado) |
| 1 | código | `def ler_casos` | não (só define) |
| 2 | código | `def criar_grafo` | não |
| 3 | código | `def resolver_caso` | não |
| 4 | código | `def responder_consulta`, `def imprimir_consultas` | não |
| 5 | código | `def plotar_grafo_inicial` | não |
| 6 | código | `def plotar_pontes_de_interesse` | não |
| 7 | código | script principal | **sim** (todo o trabalho) |

As células 1–6 apenas registram funções no namespace. Nada acontece até a célula 7.
Consequência prática: **é preciso executar as células na ordem**; rodar a 7 sem as
anteriores gera `NameError`.

### 1.2 Inventário completo de funções externas

| Origem | Função / atributo | Onde é usada |
|---|---|---|
| Python built-in | `open`, `map`, `int`, `range`, `len`, `list`, `zip`, `min`, `enumerate`, `print` | células 1, 2, 4, 6, 7 |
| `str` | `.split()`, `.strip()` | célula 1 |
| NetworkX — estrutura | `nx.Graph`, `.add_nodes_from`, `.add_weighted_edges_from`, `.nodes`, `.edges`, `.has_edge`, `G[u][v]` | células 2, 4, 6, 7 |
| NetworkX — algoritmos | `nx.maximum_spanning_tree`, `nx.shortest_path` | células 3, 4 |
| NetworkX — utilidades | `nx.get_edge_attributes` | células 5, 6 |
| NetworkX — layout | `nx.spring_layout` | célula 7 |
| NetworkX — desenho | `nx.draw_networkx`, `nx.draw_networkx_nodes`, `nx.draw_networkx_labels`, `nx.draw_networkx_edges`, `nx.draw_networkx_edge_labels` | células 5, 6 |
| matplotlib | `plt.figure`, `plt.title`, `plt.axis`, `plt.legend`, `plt.show` | células 5, 6 |

Total: **5 funções de algoritmo/estrutura do NetworkX**, **5 de desenho**, **5 de
matplotlib**, **10 built-ins**.

---

## 2. Célula 0 — imports e configuração

```python
import networkx as nx
import matplotlib.pyplot as plt

arquivo = "testes/entrada.txt"
```

### 2.1 `import networkx as nx`

Biblioteca de grafos. O apelido `nx` é a convenção universal da comunidade (equivalente a
`np` para NumPy e `pd` para pandas) — usá-lo torna o código legível para qualquer pessoa que
conheça a biblioteca.

O que o NetworkX entrega aqui: (a) as **estruturas de dados** de grafo (`nx.Graph`), (b) os
**algoritmos** prontos (Kruskal, BFS) e (c) a **camada de desenho** sobre o matplotlib.

### 2.2 `import matplotlib.pyplot as plt`

`pyplot` é a interface de estado ("qual figura está ativa agora") do matplotlib. O NetworkX
**não desenha sozinho**: `nx.draw_*` apenas adiciona artistas (coleções de linhas, círculos,
textos) aos eixos ativos do matplotlib. Por isso `plt.figure`, `plt.title` e `plt.show`
precisam ser chamados manualmente.

### 2.3 `arquivo = "testes/entrada.txt"`

Caminho **relativo**, resolvido a partir do *current working directory* do kernel Jupyter —
que é a pasta onde o notebook está (`trabalho-2/`). Por isso `testes/entrada.txt` funciona
sem prefixo.

É o único ponto de configuração do notebook: trocar essa string é tudo o que se precisa
fazer para processar outro caso de teste.

> Se o kernel for iniciado de outra pasta, o caminho quebra com `FileNotFoundError`. A
> alternativa robusta seria `pathlib.Path(__file__).parent`, que não existe em notebook;
> em notebook o equivalente é deixar o caminho relativo mesmo.

---

## 3. Célula 1 — `ler_casos`

```python
def ler_casos(arquivo):
    with open(arquivo, encoding="utf-8") as arquivo_entrada:
        linhas = [linha.split() for linha in arquivo_entrada if linha.strip()]

    casos = []
    indice = 0

    while indice < len(linhas):
        numero_ilhas, numero_pontes, numero_sedes = map(int, linhas[indice])
        indice += 1

        pontes = []
        for _ in range(numero_pontes):
            origem, destino, peso = map(int, linhas[indice])
            pontes.append((origem, destino, peso))
            indice += 1

        sedes = []
        for _ in range(numero_sedes):
            sede, deposito = map(int, linhas[indice])
            sedes.append((sede, deposito))
            indice += 1

        casos.append({
            "numero_ilhas": numero_ilhas,
            "pontes": pontes,
            "sedes": sedes,
        })

    return casos
```

**Responsabilidade:** converter texto em estrutura de dados. Nenhuma lógica de grafo aqui.

### 3.1 `open(arquivo, encoding="utf-8")`

Assinatura relevante: `open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, ...)`

| Parâmetro | Valor usado | Default | Por quê |
|---|---|---|---|
| `file` | `arquivo` | — | caminho do arquivo de entrada |
| `mode` | *(omitido)* | `'r'` | leitura em modo texto — é o que queremos |
| `encoding` | `"utf-8"` | `None` (depende do SO) | **explícito de propósito**: sem ele, o Python usa o encoding padrão da plataforma, que varia entre Linux/Windows. Fixar UTF-8 torna a leitura determinística em qualquer máquina — importante porque o arquivo do professor pode vir de outro sistema |

### 3.2 `with ... as arquivo_entrada`

O `with` é um **gerenciador de contexto**: garante `arquivo_entrada.close()` mesmo se ocorrer
exceção no meio da leitura. Evita vazamento de descritor de arquivo. É a forma canônica em
Python — abrir sem `with` seria considerado erro de estilo.

### 3.3 A list comprehension de leitura

```python
linhas = [linha.split() for linha in arquivo_entrada if linha.strip()]
```

Três mecanismos em uma linha:

**(a) `for linha in arquivo_entrada`** — objetos de arquivo em modo texto são **iteráveis
por linha**, e a iteração é *lazy* (lê sob demanda, não carrega tudo na RAM de uma vez).
Cada `linha` vem com o `\n` no final.

**(b) `if linha.strip()`** — filtro. `str.strip()` sem argumentos remove espaços, tabs e
quebras de linha das duas pontas. O resultado entra num contexto booleano: string vazia é
`False`, qualquer outra é `True`. Efeito: **linhas em branco são descartadas**, o que deixa
a leitura imune a linhas vazias no meio ou no fim do arquivo (muito comum em arquivos
gerados por editores diferentes).

**(c) `linha.split()`** — `str.split(sep=None, maxsplit=-1)`. Chamado **sem argumentos**, e
isso é relevante: com `sep=None`, o Python usa o modo "whitespace", que

- divide por qualquer sequência de espaços, tabs ou quebras de linha;
- **colapsa separadores consecutivos** (`"1   2"` → `['1','2']`, e não `['1','','','2']`);
- ignora whitespace nas bordas (o `\n` final some sozinho).

Se fosse `split(" ")`, dois espaços seguidos produziriam um token vazio e `int('')` quebraria.
Chamar sem argumento é o que torna o parser tolerante à formatação.

Resultado: `linhas` é uma `list[list[str]]`, por exemplo
`[['4','5','4'], ['1','2','9'], ...]`.

### 3.4 O cursor `indice` e o `while`

O parser é um **autômato com cursor explícito**. `indice` aponta para a próxima linha ainda
não consumida, e cada bloco avança o cursor exatamente pelo número de linhas que consumiu.

```
while indice < len(linhas):     # enquanto sobrar linha, há outro caso de teste
    lê cabeçalho (1 linha)      → indice += 1
    lê P pontes  (P linhas)     → indice += P
    lê S sedes   (S linhas)     → indice += S
```

**É esse `while` que dá suporte à OBS5 do enunciado** ("podem ter mais de um caso teste no
mesmo arquivo"). Como as quantidades vêm no cabeçalho, o parser sabe exatamente onde cada
caso termina — não precisa de separador nem de marcador de fim.

Por que não um `for`? Porque o número de casos **não é conhecido de antemão**; ele é
descoberto consumindo o arquivo. `while` com condição sobre o cursor é a construção correta.

### 3.5 `map(int, linhas[indice])` e desempacotamento

```python
numero_ilhas, numero_pontes, numero_sedes = map(int, linhas[indice])
```

- `map(function, iterable)` aplica `int` a cada token da linha. Em Python 3 devolve um
  **iterador preguiçoso**, não uma lista — não é problema aqui porque o desempacotamento o
  consome imediatamente.
- `int(x)` converte `'9'` → `9`. Lança `ValueError` se o token não for numérico (útil: falha
  cedo e alto se o arquivo estiver mal formatado).
- O **desempacotamento múltiplo** (`a, b, c = iterável`) exige que haja exatamente 3
  elementos; com número diferente, `ValueError: not enough values to unpack`. Isso funciona
  como uma validação implícita do formato do arquivo.

### 3.6 `for _ in range(numero_pontes)`

- `range(n)` gera `0, 1, ..., n−1` — aqui só importa **quantas** iterações, não o valor.
- `_` é a convenção Python para "variável de descarte": sinaliza ao leitor que o índice do
  laço não é usado. Não é palavra reservada, é só um nome.

O mesmo padrão se repete para as consultas com `range(numero_sedes)`.

### 3.7 As tuplas `(origem, destino, peso)` e `(sede, deposito)`

As pontes são guardadas como **triplas** exatamente no formato que
`add_weighted_edges_from` espera (Seção 4.3) — decisão deliberada: evita conversão depois.

As consultas são **pares**. A nomenclatura `sede`/`deposito` vem do enunciado original do
problema (o caminhão sai de uma sede e vai a um depósito).

> **Detalhe de vocabulário:** a variável se chama `numero_sedes` mas representa `S`, o número
> de **consultas**. É o nome do enunciado, mantido por fidelidade.

### 3.8 Retorno

```python
[
  {"numero_ilhas": int, "pontes": list[tuple[int,int,int]], "sedes": list[tuple[int,int]]},
  ...
]
```

Um dicionário por caso de teste. Usar dicionário em vez de tupla dá **nomes** aos campos, o
que torna `caso["pontes"]` autoexplicativo em todas as funções seguintes.

### 3.9 Complexidade

`O(P + S)` de tempo e memória por caso; cada linha é lida e convertida exatamente uma vez.

---

## 4. Célula 2 — `criar_grafo`

```python
def criar_grafo(caso):
    grafo = nx.Graph()
    grafo.add_nodes_from(range(1, caso["numero_ilhas"] + 1))
    grafo.add_weighted_edges_from(caso["pontes"], weight="weight")
    return grafo
```

**Responsabilidade:** traduzir o dicionário do parser para o objeto de grafo do NetworkX.

### 4.1 `nx.Graph()`

O NetworkX tem quatro classes de grafo:

| Classe | Direcionado? | Arestas paralelas? | Serve aqui? |
|---|---|---|---|
| **`nx.Graph`** | não | não | ✅ **escolhida** |
| `nx.DiGraph` | sim | não | ❌ ponte é mão dupla |
| `nx.MultiGraph` | não | sim | só se houver pontes paralelas |
| `nx.MultiDiGraph` | sim | sim | ❌ |

**Justificativa de `nx.Graph`:** uma ponte é atravessável nos dois sentidos com a mesma carga
máxima, o que é exatamente a semântica de aresta não direcionada. Usar `DiGraph` exigiria
inserir cada ponte duas vezes e, pior, `maximum_spanning_tree` **não aceita grafos
direcionados** (lançaria erro).

Internamente, `nx.Graph` é um **dicionário de dicionários de dicionários**:
`G._adj[u][v] → dict de atributos`. Consultas de adjacência são `O(1)` médio.

### 4.2 `add_nodes_from(nodes_for_adding, **attr)`

Assinatura real: `add_nodes_from(self, nodes_for_adding, **attr)`

| Parâmetro | Valor usado | Papel |
|---|---|---|
| `nodes_for_adding` | `range(1, I + 1)` | iterável de vértices (aceita `range`, lista, gerador, ou pares `(nó, dict)`) |
| `**attr` | *(nenhum)* | atributos aplicados a todos os nós inseridos; não precisamos de nenhum |

**Por que essa linha é obrigatória.** `add_weighted_edges_from` cria automaticamente os
vértices que aparecem em alguma aresta. Uma **ilha isolada** — que existe no arquipélago mas
não tem nenhuma ponte — nunca apareceria. Isso causaria dois problemas:

1. `grafo.nodes` teria menos de `I` vértices, e a saída "Ilhas:" mentiria;
2. uma consulta envolvendo essa ilha lançaria `NodeNotFound` em vez do erro semanticamente
   correto (não há caminho).

`range(1, I + 1)` produz `1, 2, ..., I` — o `+1` existe porque `range` é **exclusivo no
limite superior**, e o início em `1` porque o enunciado diz explicitamente que "as ilhas são
contadas a partir de 1".

Inserir um nó que já existe é **idempotente**: não duplica nem sobrescreve.

### 4.3 `add_weighted_edges_from(ebunch_to_add, weight="weight", **attr)`

Assinatura real: `add_weighted_edges_from(self, ebunch_to_add, weight='weight', **attr)`

| Parâmetro | Valor usado | Default | Papel |
|---|---|---|---|
| `ebunch_to_add` | `caso["pontes"]` | — | iterável de **triplas** `(u, v, peso)` |
| `weight` | `"weight"` | `'weight'` | **nome do atributo** onde o terceiro elemento da tripla será gravado |
| `**attr` | *(nenhum)* | — | atributos extras para todas as arestas |

**Sobre o parâmetro `weight="weight"`.** Ele é passado explicitamente mesmo sendo o valor
padrão. É uma escolha de clareza: deixa visível no código **qual chave** os algoritmos vão
procurar depois. `"weight"` é o nome canônico do NetworkX — praticamente toda função
ponderada da biblioteca usa `weight='weight'` como default. Escolher outro nome (por exemplo
`"carga"`) funcionaria, desde que **todas** as chamadas seguintes recebessem
`weight="carga"`; qualquer esquecimento faria o algoritmo tratar o grafo como não ponderado.

Efeito de uma tripla `(1, 2, 9)`:

```python
G[1][2] == {'weight': 9}       # verificado
G[2][1] == {'weight': 9}       # mesma aresta, grafo não direcionado
```

**Comportamento com duplicatas:** inserir `(1,2,9)` e depois `(1,2,3)` **sobrescreve** — a
aresta fica com peso `3`, o último lido (verificado). Ver Seção 14.

### 4.4 Retorno

Um objeto `nx.Graph` com `I` nós e até `P` arestas.

---

## 5. Célula 3 — `resolver_caso`

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

**Responsabilidade:** produzir os dois objetos que o resto do notebook consome — o grafo
original (para desenhar) e a árvore (para responder).

### 5.1 `nx.maximum_spanning_tree` — todos os parâmetros

Assinatura real (NetworkX 3.6.1):

```python
nx.maximum_spanning_tree(G, weight='weight', algorithm='kruskal',
                         ignore_nan=False, *, backend=None, **backend_kwargs)
```

| Parâmetro | Valor usado | Default | Descrição completa |
|---|---|---|---|
| `G` | `grafo` | — | grafo não direcionado. `DiGraph` não é aceito |
| `weight` | `"weight"` | `'weight'` | nome do atributo de aresta a **maximizar**. Precisa casar com o usado em `add_weighted_edges_from`. Arestas sem esse atributo contam como peso `1` |
| `algorithm` | `"kruskal"` | `'kruskal'` | qual algoritmo usar. Aceita `'kruskal'`, `'prim'` e `'boruvka'` |
| `ignore_nan` | *(omitido)* | `False` | se `True`, arestas com peso `NaN` são ignoradas; se `False`, um `NaN` lança `ValueError`. Manter `False` é mais seguro: pesos inteiros nunca deveriam virar `NaN`, e se virarem é bug que queremos ver |
| `backend` / `**backend_kwargs` | *(omitidos)* | `None` | despacho para backends alternativos (GPU, paralelo). Irrelevante nesta escala |

**Por que `algorithm="kruskal"` explícito?** Mesmo sendo o default, explicitar documenta a
escolha — e a OBS4 do enunciado exige justificar funções prontas e entender seus parâmetros.
A justificativa teórica está em `TEORIA.md`, Seção 7.6: Kruskal processa as arestas da mais
forte para a mais fraca, o que espelha a narrativa do problema e é fácil de reproduzir à mão
na defesa.

### 5.2 O que acontece por dentro

Lendo o fonte (`networkx/algorithms/tree/mst.py`):

1. `maximum_spanning_tree` chama `maximum_spanning_edges`, que chama `kruskal_mst_edges`
   com `minimum=False`;
2. com `minimum=False`, a ordenação é `sorted(open_edges, key=itemgetter(0), reverse=True)` —
   ou seja, **peso decrescente**. Não há negação de pesos, apenas inversão da ordem;
3. um `nx.utils.UnionFind` (`subtrees`) controla as componentes; cada aresta é aceita apenas
   se `subtrees[u] != subtrees[v]`;
4. a `UnionFind` do NetworkX implementa **compressão de caminho** (no `__getitem__`) e
   **união por tamanho** (campo `weights`), dando custo `O(α(n))` amortizado por operação.

Complexidade: `O(P log P)`, dominada pela ordenação.

### 5.3 Retorno

Um **novo objeto** `nx.Graph` (não é uma view nem uma referência ao original):

- contém **todos** os `I` nós;
- contém `I − 1` arestas se `G` for conexo;
- **preserva os dicionários de atributos** das arestas, então `T[u][v]["weight"]` funciona
  diretamente — é por isso que `responder_consulta` consegue ler pesos da árvore;
- se `G` for **desconexo**, devolve uma **floresta geradora máxima** (uma árvore por
  componente), apesar do nome da função. Verificado: com `G` de 4 nós e só a aresta `(1,2)`,
  o retorno tem 4 nós e 1 aresta, e `nx.is_connected` é `False`.

### 5.4 Por que devolver os dois objetos

```python
return grafo, arvore_maxima
```

- `grafo` é necessário para o desenho: só ele conhece as **pontes descartadas**, que precisam
  aparecer em cinza no segundo gráfico;
- `arvore_maxima` é o que responde as consultas.

Python empacota os dois em uma **tupla** automaticamente; o chamador desempacota com
`grafo, arvore_maxima = resolver_caso(caso)`.

---

## 6. Célula 4 — `responder_consulta` e `imprimir_consultas`

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

**Responsabilidade:** aplicar o Teorema 6.1 do `TEORIA.md` — recuperar o caminho único na
árvore e devolver seu gargalo.

### 6.1 `nx.shortest_path` — todos os parâmetros

Assinatura real:

```python
nx.shortest_path(G, source=None, target=None, weight=None,
                 method='dijkstra', *, backend=None, **backend_kwargs)
```

| Parâmetro | Valor usado | Default | Descrição |
|---|---|---|---|
| `G` | `arvore_maxima` | — | **a árvore**, não o grafo original. É o ponto central da solução |
| `source` | `inicio` | `None` | vértice de origem. Se `None`, calcula de todos os nós |
| `target` | `fim` | `None` | vértice de destino. Se `None`, calcula para todos |
| `weight` | **omitido** | `None` | nome do atributo de peso. **Omitir é intencional** — ver 6.2 |
| `method` | *(omitido)* | `'dijkstra'` | `'dijkstra'` ou `'bellman-ford'`. **Irrelevante aqui**, porque é sobrescrito quando `weight=None` |
| `backend`, `**backend_kwargs` | *(omitidos)* | `None` | despacho alternativo |

### 6.2 Por que `weight` é omitido — a justificativa exata

Lendo o fonte (`networkx/algorithms/shortest_paths/generic.py`, linha 138):

```python
method = "unweighted" if weight is None else method
```

Ou seja: **ao omitir `weight`, o parâmetro `method='dijkstra'` é descartado** e o NetworkX
usa `nx.bidirectional_shortest_path` — uma **BFS bidirecional**, que minimiza o *número de
arestas*, não a soma dos pesos.

Isso é correto e desejado por três motivos encadeados:

1. **Dentro de uma árvore existe exatamente um caminho entre dois vértices**
   (`TEORIA.md`, Teorema 3.1(4)). Logo "caminho mais curto" e "o caminho" são o mesmo objeto
   — a busca não está otimizando nada, apenas **recuperando**.
2. **Passar `weight="weight"` seria um erro conceitual.** Faria o algoritmo minimizar a
   *soma* dos pesos, que não tem significado no problema do caminhão (o custo de um caminho
   é o `min`, não a soma — ver `TEORIA.md`, Seção 2.3). O resultado numérico seria o mesmo
   (o caminho é único de qualquer forma), mas o código comunicaria uma modelagem errada.
3. **BFS é mais barata.** `O(V + E) = O(I)` numa árvore, sem heap, contra `O(E log V)` do
   Dijkstra.

Retorno: uma **lista de vértices** `[inicio, ..., fim]`, por exemplo `[4, 2, 3]`.

### 6.3 `zip(caminho, caminho[1:])` — o pareamento

`nx.shortest_path` devolve **vértices**, mas precisamos dos **pesos das arestas**. A conversão
é feita com o idioma de janela deslizante:

```python
caminho        = [4, 2, 3]
caminho[1:]    = [2, 3]           # slicing: tudo a partir do índice 1
zip(...)       → (4,2), (2,3)     # pares consecutivos
```

- `zip(*iterables)` combina posição a posição e **para no mais curto** — por isso o resultado
  tem `len(caminho) − 1` pares, exatamente o número de arestas do caminho;
- `caminho[1:]` cria uma cópia rasa da lista sem o primeiro elemento. Para os tamanhos deste
  trabalho o custo é irrelevante;
- `for origem, destino in zip(...)` desempacota cada par diretamente nas duas variáveis.

Uma alternativa equivalente seria `for i in range(len(caminho)-1)` com indexação manual — o
`zip` é preferido por ser mais legível e não ter risco de erro de índice.

### 6.4 `arvore_maxima[origem][destino]["weight"]`

Três indexações encadeadas, que refletem a estrutura interna dict-of-dicts:

```python
arvore_maxima[origem]              # → AtlasView: {vizinho: {atributos}}
arvore_maxima[origem][destino]     # → {'weight': 7}
arvore_maxima[origem][destino]["weight"]   # → 7
```

Forma equivalente e um pouco mais explícita: `arvore_maxima.edges[origem, destino]["weight"]`.
As duas custam `O(1)` médio (lookup de dicionário).

Como o grafo é não direcionado, `T[2][4]` e `T[4][2]` devolvem o **mesmo dicionário**
(verificado) — a ordem em que o par sai do `zip` não importa.

### 6.5 `min(pesos_do_caminho)`

`min(iterable)` devolve o menor elemento. É a tradução literal de

```
cap(Q) = min w(e)     para e ∈ Q
```

**Atenção:** `min([])` lança `ValueError: min() iterable argument is empty` (verificado).
Isso acontece se `inicio == fim`, pois o caminho tem zero arestas. Ver Seção 14.3.

### 6.6 `imprimir_consultas`

```python
def imprimir_consultas(arvore_maxima, sedes):
    for inicio, fim in sedes:
        caminho, peso_maximo = responder_consulta(arvore_maxima, inicio, fim)

        print(f"{inicio} → {fim}")
        print(f"Caminho: {caminho}")
        print(f"Peso máximo: {peso_maximo}\n")
```

- itera as consultas **na ordem em que aparecem no arquivo** — requisito do enunciado, já que
  a saída esperada é uma linha por consulta na mesma ordem;
- `for inicio, fim in sedes` desempacota cada tupla `(X, Y)` direto no cabeçalho do laço;
- **f-strings** (`f"..."`) interpolam expressões entre chaves em tempo de execução;
- o `\n` no final da terceira linha cria a linha em branco que separa visualmente as
  consultas;
- a linha `Peso máximo:` é **a resposta oficial** do problema; `Caminho:` é evidência de
  auditoria, para a banca conferir a rota escolhida.

---

## 7. Célula 5 — `plotar_grafo_inicial`

```python
def plotar_grafo_inicial(grafo, posicoes, titulo):
    plt.figure(figsize=(8, 6))
    nx.draw_networkx(
        grafo,
        posicoes,
        with_labels=True,
        node_color="lightblue",
        node_size=900,
        edge_color="gray",
        width=2,
        font_weight="bold",
    )

    pesos = nx.get_edge_attributes(grafo, "weight")
    nx.draw_networkx_edge_labels(grafo, posicoes, edge_labels=pesos)

    plt.title(titulo)
    plt.axis("off")
    plt.show()
```

**Responsabilidade:** item "gerar grafo inicial e plotar" (1 ponto do enunciado).

### 7.1 `plt.figure(figsize=(8, 6))`

| Parâmetro | Valor | Default | Descrição |
|---|---|---|---|
| `figsize` | `(8, 6)` | `(6.4, 4.8)` | largura × altura **em polegadas** |

Com `figure.dpi = 100` (default do matplotlib, verificado), `(8, 6)` polegadas resultam em
**800 × 600 pixels**. A chamada cria uma figura nova e a torna a figura ativa — sem ela,
todos os gráficos do laço seriam desenhados **empilhados na mesma figura**.

### 7.2 `nx.draw_networkx` — como ela distribui os parâmetros

Assinatura: `nx.draw_networkx(G, pos=None, arrows=None, with_labels=True, **kwds)`

Essa é uma **função de conveniência**. Lendo o fonte (`nx_pylab.py`, linhas 1328–1355), ela:

1. monta o conjunto de parâmetros válidos a partir das assinaturas de
   `draw_networkx_nodes`, `draw_networkx_edges` e `draw_networkx_labels`;
2. **lança `ValueError` se receber um parâmetro que não pertence a nenhuma das três** —
   proteção útil contra erro de digitação;
3. reparte os `**kwds` entre as três funções e chama as três em sequência:
   nós → arestas → rótulos.

Parâmetros usados no notebook e para onde cada um vai:

| Parâmetro | Valor | Default | Vai para | Efeito |
|---|---|---|---|---|
| `G` | `grafo` | — | todas | o grafo a desenhar |
| `pos` | `posicoes` | `None` | todas | dicionário `{nó: array([x, y])}`. Se `None`, a função chama `spring_layout` sozinha — o que daria **layouts diferentes** nos dois gráficos |
| `with_labels` | `True` | `True` | controle | se `True`, desenha os números das ilhas dentro dos círculos |
| `node_color` | `"lightblue"` | `'#1f78b4'` | nós | cor de preenchimento. Aceita nome CSS, hex, RGB ou lista/array (uma cor por nó) |
| `node_size` | `900` | `300` | nós **e** arestas | área do marcador em pontos². `900` é 3× o padrão, necessário para caber rótulos em negrito |
| `edge_color` | `"gray"` | `'k'` (preto) | arestas | cor das linhas |
| `width` | `2` | `1.0` | arestas | espessura da linha em pontos |
| `font_weight` | `"bold"` | `'normal'` | rótulos | peso da fonte dos números das ilhas |

> **Nuance de `node_size`:** ele aparece na assinatura **das duas** funções (nós e arestas).
> Em `draw_networkx_edges` ele serve para encurtar a linha e não invadir o círculo do nó —
> mas, para grafos **não direcionados**, as arestas são desenhadas como `LineCollection` e
> `node_size` só é realmente usado quando há setas (`FancyArrowPatch`) ou laços (verificado no
> fonte). Aqui, portanto, ele só afeta o tamanho dos círculos.

### 7.3 `nx.get_edge_attributes(G, name, default=None)`

| Parâmetro | Valor usado | Default | Descrição |
|---|---|---|---|
| `G` | `grafo` | — | grafo de origem |
| `name` | `"weight"` | — | nome do atributo a extrair |
| `default` | *(omitido)* | `None` | se informado, arestas sem o atributo entram no dicionário com esse valor; se `None`, são **omitidas** |

Retorno verificado: `{(1, 2): 9, (1, 3): 0, (2, 3): 8, (2, 4): 7, (3, 4): 4}` — um dicionário
`{(u, v): peso}`, com o par na ordem em que a aresta foi inserida.

### 7.4 `nx.draw_networkx_edge_labels`

Assinatura completa:

```python
nx.draw_networkx_edge_labels(G, pos, edge_labels=None, label_pos=0.5, font_size=10,
    font_color='k', font_family='sans-serif', font_weight='normal', alpha=None,
    bbox=None, horizontalalignment='center', verticalalignment='center', ax=None,
    rotate=True, clip_on=True, node_size=300, nodelist=None,
    connectionstyle='arc3', hide_ticks=True)
```

| Parâmetro | Valor usado | Default | Descrição |
|---|---|---|---|
| `G`, `pos` | `grafo`, `posicoes` | — | grafo e posições (as mesmas do desenho, senão os rótulos ficam deslocados) |
| `edge_labels` | `pesos` | `None` | dicionário `{(u,v): texto}`. Se `None`, o NetworkX usa o dicionário de atributos completo como texto |

Parâmetros deixados no default que valem conhecer: `label_pos=0.5` (rótulo no meio da
aresta; `0` = na origem, `1` = no destino), `rotate=True` (o texto acompanha o ângulo da
aresta), `font_size=10`, `bbox` (caixa de fundo atrás do texto — útil quando o rótulo fica
ilegível sobre a linha).

### 7.5 `plt.title`, `plt.axis("off")`, `plt.show()`

- `plt.title(titulo)` — título do eixo ativo. O texto é montado com f-string na célula 7.
- `plt.axis("off")` — desliga os eixos, ticks e a moldura. Sem isso, o gráfico apareceria com
  uma escala numérica `x`/`y` que **não tem significado nenhum** (as coordenadas do
  `spring_layout` são arbitrárias). Desligar não é estética, é evitar leitura errada.
- `plt.show()` — renderiza e "fecha" a figura ativa. Em notebook, garante que a imagem
  apareça na saída da célula **naquele ponto** e que o próximo `plt.figure` comece limpo.

---

## 8. Célula 6 — `plotar_pontes_de_interesse`

```python
def plotar_pontes_de_interesse(grafo, arvore_maxima, posicoes, titulo):
    pontes_interesse = list(arvore_maxima.edges())

    pontes_descartadas = [
        (origem, destino)
        for origem, destino in grafo.edges()
        if not arvore_maxima.has_edge(origem, destino)
    ]
    ...
```

**Responsabilidade:** item "evidenciar pontes de interesse" (2 pontos do enunciado).

### 8.1 A separação em dois conjuntos

- `arvore_maxima.edges()` devolve uma **`EdgeView`** — uma *view* dinâmica, não uma lista.
  `list(...)` materializa em `[(1,2), (2,3), (2,4)]`.
- A list comprehension filtra as arestas do grafo original que **não** estão na árvore.
- `has_edge(u, v)` devolve `bool` em `O(1)` médio, e em grafo não direcionado
  `has_edge(u,v) == has_edge(v,u)` — então a ordem em que a aresta sai de `grafo.edges()`
  não importa.

Resultado no exemplo: interesse `[(1,2),(2,3),(2,4)]`, descartadas `[(1,3),(3,4)]`.

### 8.2 Por que desenhar em camadas em vez de uma chamada só

`nx.draw_networkx` aplica **um estilo único** a todas as arestas. Para dar cores, espessuras
e traços diferentes a dois subconjuntos, é preciso chamar as funções de baixo nível
separadamente. As quatro camadas, **nesta ordem**:

| Ordem | Chamada | Papel |
|---|---|---|
| 1 | `draw_networkx_nodes` | círculos das ilhas |
| 2 | `draw_networkx_labels` | números das ilhas |
| 3 | `draw_networkx_edges(edgelist=pontes_descartadas, ...)` | cinza tracejado |
| 4 | `draw_networkx_edges(edgelist=pontes_interesse, ...)` | vermelho grosso |
| 5 | `draw_networkx_edge_labels` | pesos sobre todas |

A ordem importa: o matplotlib desenha na ordem de chamada, então **as pontes de interesse
ficam por cima das descartadas** em cruzamentos.

### 8.3 `nx.draw_networkx_nodes` — parâmetros

Assinatura completa:

```python
nx.draw_networkx_nodes(G, pos, nodelist=None, node_size=300, node_color='#1f78b4',
    node_shape='o', alpha=None, cmap=None, vmin=None, vmax=None, ax=None,
    linewidths=None, edgecolors=None, label=None, margins=None, hide_ticks=True)
```

| Parâmetro | Valor usado | Default | Descrição |
|---|---|---|---|
| `G`, `pos` | `grafo`, `posicoes` | — | grafo e coordenadas |
| `node_color` | `"lightblue"` | `'#1f78b4'` | mesma cor do primeiro gráfico, para comparação visual |
| `node_size` | `900` | `300` | mesmo tamanho do primeiro gráfico |
| `nodelist` | *(omitido)* | `None` = todos | permitiria desenhar só um subconjunto de nós |
| `node_shape` | *(omitido)* | `'o'` | marcador do matplotlib: `'o'` círculo, `'s'` quadrado, `'^'` triângulo, `'d'` losango… |
| `edgecolors` / `linewidths` | *(omitidos)* | `None` | cor e espessura da **borda** do círculo |

Retorno: um `PathCollection` do matplotlib.

### 8.4 `nx.draw_networkx_labels` — parâmetros

| Parâmetro | Valor usado | Default | Descrição |
|---|---|---|---|
| `G`, `pos` | `grafo`, `posicoes` | — | — |
| `font_weight` | `"bold"` | `'normal'` | negrito, para os números destacarem sobre o azul |
| `labels` | *(omitido)* | `None` | dicionário `{nó: texto}`. Omitido ⇒ usa `str(nó)`, que é o número da ilha |
| `font_size`, `font_color`, `font_family` | *(omitidos)* | `12`, `'k'`, `'sans-serif'` | tipografia |

### 8.5 `nx.draw_networkx_edges` — parâmetros (a função mais importante desta célula)

Assinatura completa:

```python
nx.draw_networkx_edges(G, pos, edgelist=None, width=1.0, edge_color='k', style='solid',
    alpha=None, arrowstyle=None, arrowsize=10, edge_cmap=None, edge_vmin=None,
    edge_vmax=None, ax=None, arrows=None, label=None, node_size=300, nodelist=None,
    node_shape='o', connectionstyle='arc3', min_source_margin=0, min_target_margin=0,
    hide_ticks=True)
```

**Chamada 1 — pontes descartadas:**

| Parâmetro | Valor | Default | Descrição |
|---|---|---|---|
| `edgelist` | `pontes_descartadas` | `None` = todas | **o parâmetro-chave**: restringe o desenho a esse subconjunto de arestas |
| `edge_color` | `"lightgray"` | `'k'` | cinza claro = "existe, mas não interessa" |
| `width` | `2` | `1.0` | espessura |
| `style` | `"dashed"` | `'solid'` | traço. Aceita `'solid'`, `'dashed'`, `'dotted'`, `'dashdot'` ou uma tupla de *dash pattern* |
| `label` | `"Pontes descartadas"` | `None` | **texto para a legenda** — ver 8.6 |

**Chamada 2 — pontes de interesse:**

| Parâmetro | Valor | Descrição |
|---|---|---|
| `edgelist` | `pontes_interesse` | as `I − 1` arestas da MaxST |
| `edge_color` | `"red"` | vermelho = destaque, a resposta visual do item de 2 pontos |
| `width` | `3.5` | quase o dobro das descartadas, reforçando a hierarquia visual |
| `label` | `"Pontes de interesse"` | entrada da legenda |

Parâmetro relevante deixado no default: `arrows=None` — com `None`, o NetworkX usa
`LineCollection` para grafos não direcionados (mais rápido) e setas só para direcionados.
Como nosso grafo é `nx.Graph`, saem linhas simples, que é o correto para pontes de mão dupla.

### 8.6 `label` + `plt.legend(loc="best")`

Detalhe que costuma falhar em outros trabalhos e **aqui funciona** (verificado executando):
`draw_networkx_edges` devolve um `LineCollection` com o `label` definido, e o matplotlib
inclui coleções rotuladas na legenda. A saída do teste foi:

```
retorno draw_networkx_edges: LineCollection  label= Pontes descartadas
legenda entradas: ['Pontes descartadas', 'Pontes de interesse']
```

`plt.legend(loc="best")` — `loc` aceita `'best'`, `'upper right'`, `'upper left'`,
`'lower left'`, `'lower right'`, `'right'`, `'center left'`, `'center right'`,
`'lower center'`, `'upper center'`, `'center'`. Com `'best'`, o matplotlib procura o canto
com menos sobreposição com os dados — a escolha certa quando o layout do grafo muda a cada
caso de teste.

### 8.7 A saída textual

```python
print("Pontes de interesse:", list(arvore_maxima.edges(data="weight")))
```

`G.edges(data="weight")` com `data` recebendo uma **string** devolve triplas
`(u, v, valor_do_atributo)` — verificado: `[(1, 2, 9), (1, 3, 0), ...]`.

Variações do parâmetro `data`:

| Chamada | Retorno |
|---|---|
| `G.edges()` | `(u, v)` |
| `G.edges(data=True)` | `(u, v, {'weight': 9})` — dict completo |
| `G.edges(data="weight")` | `(u, v, 9)` — só o valor |
| `G.edges(data="weight", default=0)` | idem, com fallback para arestas sem o atributo |

Para as descartadas, como elas são pares `(u, v)` sem peso, o peso é buscado no grafo
original com `grafo[origem][destino]["weight"]` dentro de uma list comprehension.

Essa impressão é o que dá a **resposta textual** do item "evidenciar pontes de interesse" —
o gráfico mostra, o `print` documenta.

---

## 9. Célula 7 — execução

```python
casos = ler_casos(arquivo)

print("Casos no arquivo:", len(casos), "\n")

for numero_caso, caso in enumerate(casos, 1):
    grafo, arvore_maxima = resolver_caso(caso)

    print(f"===== Caso {numero_caso} =====")
    print("Ilhas:", list(grafo.nodes))
    print("Pontes:", list(grafo.edges(data="weight")))
    posicoes = nx.spring_layout(grafo, seed=42)

    plotar_grafo_inicial(grafo, posicoes, f"Caso {numero_caso} - Ilhas e pontes")
    plotar_pontes_de_interesse(
        grafo, arvore_maxima, posicoes, f"Caso {numero_caso} - Pontes de interesse",
    )

    print()
    imprimir_consultas(arvore_maxima, caso["sedes"])
```

### 9.1 `enumerate(casos, 1)`

`enumerate(iterable, start=0)` devolve pares `(índice, elemento)`. O segundo argumento
`start=1` faz a numeração começar em 1, para a saída dizer "Caso 1" em vez de "Caso 0" — puro
rótulo, não afeta a lógica.

### 9.2 `nx.spring_layout` — todos os parâmetros

Assinatura real (NetworkX 3.6.1):

```python
nx.spring_layout(G, k=None, pos=None, fixed=None, iterations=50, threshold=0.0001,
    weight='weight', scale=1, center=None, dim=2, seed=None, store_pos_as=None,
    *, method='auto', gravity=1.0)
```

| Parâmetro | Valor usado | Default | Descrição |
|---|---|---|---|
| `G` | `grafo` | — | grafo a posicionar |
| `seed` | `42` | `None` | semente do gerador aleatório. **Crítico** — ver 9.3 |
| `k` | *(omitido)* | `None` | distância ideal entre nós; `None` ⇒ `1/√n` |
| `pos` | *(omitido)* | `None` | posições iniciais; permite partir de um layout dado |
| `fixed` | *(omitido)* | `None` | lista de nós que não se movem (exige `pos`) |
| `iterations` | *(omitido)* | `50` | número de iterações da simulação de forças |
| `threshold` | *(omitido)* | `1e-4` | critério de parada antecipada por convergência |
| `weight` | *(omitido)* | `'weight'` | **atenção** — ver 9.4 |
| `scale` | *(omitido)* | `1` | escala final das coordenadas |
| `center` | *(omitido)* | `None` = origem | centro do desenho |
| `dim` | *(omitido)* | `2` | dimensão do espaço (2D) |
| `store_pos_as` | *(omitido)* | `None` | se informado, grava as posições como atributo dos nós |
| `method` | *(omitido)* | `'auto'` | `'force'` (Fruchterman-Reingold) se `len(G) < 500`, senão `'energy'`. Com nossos grafos pequenos, sempre `'force'` |
| `gravity` | *(omitido)* | `1.0` | só usado por `method='energy'` |

**O algoritmo:** Fruchterman-Reingold, um modelo físico de molas — nós ligados por aresta se
atraem, todos os nós se repelem mutuamente, e a simulação roda `iterations` passos buscando
equilíbrio. O resultado é um desenho onde vértices muito conectados ficam próximos.

Retorno: `dict` `{nó: numpy.ndarray([x, y])}`.

### 9.3 Por que `seed=42`

O layout parte de posições **aleatórias**. Sem semente fixa:

- os dois gráficos do mesmo caso teriam **layouts diferentes**, impossibilitando comparar o
  grafo completo com as pontes de interesse;
- cada execução do notebook geraria um desenho diferente, atrapalhando a conferência do
  trabalho.

Verificado: duas chamadas com `seed=42` produzem posições **idênticas**. O valor `42` não tem
significado técnico — é qualquer inteiro fixo.

É por isso também que `posicoes` é calculado **uma vez** na célula 7 e passado como argumento
às duas funções de plotagem, em vez de cada uma calcular o seu.

### 9.4 Achado importante: o layout usa os pesos das pontes

`spring_layout` tem `weight='weight'` **por padrão**, e nosso grafo tem exatamente esse
atributo. Consequência: **a força de atração de cada mola é proporcional ao peso da ponte** —
pontes fortes puxam as ilhas para perto, pontes fracas quase não puxam.

Medido no exemplo do enunciado (distância euclidiana no layout):

| Aresta | Peso | Distância com `weight` padrão | Distância com `weight=None` |
|---|---|---|---|
| `1–2` | 9 | 1.005 | 1.308 |
| `3–4` | 4 | 0.995 | 1.320 |
| `1–3` | **0** | **1.912** | 1.308 |

A ponte de peso `0` fica visivelmente mais esticada. Isso é, por acaso, **favorável** ao
trabalho: o desenho já sugere visualmente quais pontes são fracas. Mas é um efeito colateral
não planejado, e vale saber explicá-lo se a banca perguntar por que a ponte inútil aparece
tão longe. Para um layout puramente topológico, bastaria `nx.spring_layout(grafo, seed=42,
weight=None)`.

### 9.5 `grafo.nodes` e `grafo.edges(data="weight")`

- `grafo.nodes` é uma **`NodeView`**; `list(...)` materializa `[1, 2, 3, 4]`. A ordem é a de
  inserção (garantida pelos dicionários do Python 3.7+), então as ilhas saem em ordem
  numérica graças ao `add_nodes_from(range(...))`.
- `grafo.edges(data="weight")` já foi descrita em 8.7.

Essas duas linhas atendem ao item **"carregar arquivo corretamente" (1 ponto)**: imprimem o
que foi de fato lido, permitindo conferir contra o arquivo de entrada.

### 9.6 Ordem das operações no laço

```
resolver_caso   → grafo + árvore          (computação)
print           → ilhas e pontes          (evidência de leitura)
spring_layout   → posições compartilhadas (determinismo visual)
plotar inicial  → gráfico 1               (1 pt)
plotar interesse→ gráfico 2 + listas      (2 pts)
imprimir_consultas → respostas            (2 pts)
```

É a ordem dos itens de avaliação do enunciado — deliberado, para a apresentação seguir o
mesmo roteiro da correção.

---

## 10. Tabela mestra de parâmetros usados

| # | Função | Parâmetro | Valor | Default | Motivo da escolha |
|---|---|---|---|---|---|
| 1 | `open` | `encoding` | `"utf-8"` | plataforma | determinismo entre SOs |
| 2 | `str.split` | `sep` | *(omitido)* | `None` | modo whitespace: colapsa espaços múltiplos |
| 3 | `add_nodes_from` | `nodes_for_adding` | `range(1, I+1)` | — | garante ilhas isoladas |
| 4 | `add_weighted_edges_from` | `weight` | `"weight"` | `'weight'` | chave canônica do NetworkX |
| 5 | `maximum_spanning_tree` | `weight` | `"weight"` | `'weight'` | atributo a maximizar |
| 6 | `maximum_spanning_tree` | `algorithm` | `"kruskal"` | `'kruskal'` | ordem decrescente espelha o problema; `O(P log P)` |
| 7 | `shortest_path` | `weight` | **omitido** | `None` | força BFS; o caminho na árvore é único |
| 8 | `plt.figure` | `figsize` | `(8, 6)` | `(6.4, 4.8)` | 800×600 px, legível no notebook |
| 9 | `draw_networkx` | `with_labels` | `True` | `True` | mostrar o número da ilha |
| 10 | `draw_networkx` | `node_color` | `"lightblue"` | `'#1f78b4'` | contraste com o vermelho das pontes |
| 11 | `draw_networkx` | `node_size` | `900` | `300` | caber rótulo em negrito |
| 12 | `draw_networkx` | `edge_color` | `"gray"` | `'k'` | neutro no gráfico 1 |
| 13 | `draw_networkx` | `width` | `2` | `1.0` | visibilidade |
| 14 | `draw_networkx` | `font_weight` | `"bold"` | `'normal'` | leitura sobre o azul |
| 15 | `get_edge_attributes` | `name` | `"weight"` | — | extrair pesos para rótulos |
| 16 | `draw_networkx_edge_labels` | `edge_labels` | `pesos` | `None` | escrever só o número, não o dict |
| 17 | `draw_networkx_edges` | `edgelist` | subconjunto | `None` | **separar interesse × descartadas** |
| 18 | `draw_networkx_edges` | `style` | `"dashed"` | `'solid'` | descartadas visualmente secundárias |
| 19 | `draw_networkx_edges` | `label` | texto | `None` | alimentar a legenda |
| 20 | `plt.legend` | `loc` | `"best"` | `'best'` | layout varia por caso |
| 21 | `plt.axis` | — | `"off"` | — | coordenadas não têm significado |
| 22 | `spring_layout` | `seed` | `42` | `None` | reprodutibilidade e layout comum |
| 23 | `enumerate` | `start` | `1` | `0` | rotular "Caso 1" |

---

## 11. Parâmetros não usados que valem conhecer

Perguntas prováveis do tipo "e se você quisesse...":

| Objetivo | Como fazer |
|---|---|
| Usar Prim em vez de Kruskal | `nx.maximum_spanning_tree(G, algorithm="prim")` — mesmo resultado (ver `TEORIA.md`, Cor. 6.3) |
| Usar Borůvka | `algorithm="boruvka"` |
| Obter a árvore **mínima** | `nx.minimum_spanning_tree(...)` — responde o gargalo mínimo, o problema dual |
| Só as arestas, sem construir o grafo | `nx.maximum_spanning_edges(G, algorithm="kruskal", data=True)` — devolve um gerador |
| Layout que ignora os pesos | `nx.spring_layout(G, seed=42, weight=None)` (ver 9.4) |
| Layout determinístico sem física | `nx.circular_layout(G)`, `nx.shell_layout(G)`, `nx.kamada_kawai_layout(G)` |
| Rótulo de aresta sem rotação | `nx.draw_networkx_edge_labels(..., rotate=False)` |
| Caixa branca atrás do peso | `nx.draw_networkx_edge_labels(..., bbox=dict(facecolor="white", edgecolor="none"))` |
| Pontes paralelas na entrada | usar `nx.MultiGraph` (ver Seção 14.4) |
| Salvar a figura em arquivo | `plt.savefig("caso1.png", dpi=150, bbox_inches="tight")` antes de `plt.show()` |
| Gargalo sem construir a árvore | `nx.maximum_bottleneck_path`… **não existe** no NetworkX; seria preciso implementar Dijkstra maximin manualmente (`TEORIA.md`, Seção 10.1) |

---

## 12. Sintaxe e built-ins de Python usados

| Recurso | Exemplo no notebook | O que faz |
|---|---|---|
| Gerenciador de contexto | `with open(...) as f:` | fecha o arquivo automaticamente |
| List comprehension | `[linha.split() for linha in f if linha.strip()]` | mapear + filtrar em uma expressão |
| Desempacotamento múltiplo | `a, b, c = map(int, linha)` | atribuir vários nomes de uma vez; valida a aridade |
| Variável de descarte | `for _ in range(n)` | sinaliza que o índice não é usado |
| Slicing | `caminho[1:]` | sublista a partir do índice 1 |
| `zip` | `zip(caminho, caminho[1:])` | janela deslizante de pares consecutivos |
| `min` | `min(pesos_do_caminho)` | menor elemento; `ValueError` se vazio |
| `enumerate(it, start)` | `enumerate(casos, 1)` | pares `(índice, item)` |
| f-string | `f"Caso {numero_caso}"` | interpolação de expressões |
| Tupla de retorno | `return grafo, arvore_maxima` | devolver dois valores |
| Dicionário literal | `{"numero_ilhas": ..., ...}` | registro com campos nomeados |
| Indexação encadeada | `T[u][v]["weight"]` | navegar o dict-of-dicts do NetworkX |
| Booleano implícito | `if linha.strip()` | string vazia é falsa |

---

## 13. Fluxo de dados e tipos

```
"testes/entrada.txt"                                        str
        │
        ▼  ler_casos
list[dict]                                                  [{"numero_ilhas": int,
                                                               "pontes": list[(int,int,int)],
                                                               "sedes":  list[(int,int)]}]
        │
        ▼  criar_grafo
nx.Graph                                                    I nós, ≤P arestas, attr "weight"
        │
        ▼  nx.maximum_spanning_tree
nx.Graph (árvore)                                           I nós, I−1 arestas
        │
        ├──► arvore.edges() ──► list[(int,int)] ──► desenho vermelho
        │
        ▼  nx.shortest_path
list[int]  (ex.: [4, 2, 3])
        │
        ▼  zip + indexação
list[int]  (ex.: [7, 8])                                    pesos das arestas
        │
        ▼  min
int  (ex.: 7)                                               resposta da consulta
```

| Função | Recebe | Devolve |
|---|---|---|
| `ler_casos` | `str` (caminho) | `list[dict]` |
| `criar_grafo` | `dict` (caso) | `nx.Graph` |
| `resolver_caso` | `dict` (caso) | `tuple[nx.Graph, nx.Graph]` |
| `responder_consulta` | `nx.Graph`, `int`, `int` | `tuple[list[int], int]` |
| `imprimir_consultas` | `nx.Graph`, `list[tuple]` | `None` (imprime) |
| `plotar_grafo_inicial` | `nx.Graph`, `dict`, `str` | `None` (desenha) |
| `plotar_pontes_de_interesse` | `nx.Graph`, `nx.Graph`, `dict`, `str` | `None` (desenha + imprime) |

---

## 14. Erros possíveis e o que significam

### 14.1 `FileNotFoundError`
O caminho em `arquivo` não existe a partir do diretório do kernel. Conferir se o notebook foi
aberto de dentro de `trabalho-2/`.

### 14.2 `NetworkXNoPath: No path between X and Y`
**Verificado.** As ilhas `X` e `Y` estão em componentes conexas diferentes. Nesse caso
`maximum_spanning_tree` devolveu uma **floresta**, não uma árvore. Teoricamente a resposta é
"nenhum caminhão chega" (`−∞`). Se o caso de teste do professor puder ser desconexo, seria
preciso envolver a consulta em `try/except` ou testar `nx.has_path(arvore, X, Y)` antes.

### 14.3 `ValueError: min() iterable argument is empty`
**Verificado.** Ocorre quando `inicio == fim`: o caminho é `[X]`, com zero arestas, e
`min([])` falha. Semanticamente a resposta seria `+∞` (o caminhão não atravessa ponte
alguma). Um caso de teste com `X == Y` quebraria o notebook.

### 14.4 Peso errado com pontes paralelas
**Verificado.** Como `nx.Graph` não admite arestas paralelas,
`add_weighted_edges_from([(1,2,9), (1,2,3)])` deixa a aresta com peso `3` — **a última lida,
não a maior**. Para o problema do gargalo, a correta seria a de maior peso. Se a entrada
puder ter duas pontes ligando as mesmas ilhas, é preciso usar `nx.MultiGraph` ou filtrar
mantendo o máximo por par antes de inserir.

### 14.5 `NodeNotFound`
Uma consulta cita uma ilha fora do intervalo `1..I`. Indica arquivo de entrada inconsistente
com o cabeçalho.

### 14.6 `ValueError: Received invalid argument(s): ...`
Erro específico de `nx.draw_networkx`: um parâmetro passado não pertence a nenhuma das três
funções de desenho que ela encapsula. Normalmente é erro de digitação (`node_colour` em vez
de `node_color`).

### 14.7 `NameError: name 'ler_casos' is not defined`
A célula 7 foi executada sem rodar as células 1–6 antes.

### 14.8 Laços (`u == v`)
**Verificado:** um laço é aceito pelo `nx.Graph`, mas nunca entra na árvore, porque os dois
extremos já estão na mesma componente. Comportamento correto, nada a corrigir.

---

## 15. Como adaptar o notebook

| Quero… | Mudança |
|---|---|
| Rodar outro caso de teste | trocar a string `arquivo` na célula 0 |
| Rodar todos os testes | envolver a célula 7 em um laço sobre `os.listdir("testes")` |
| Trocar o algoritmo de MaxST | `algorithm="prim"` ou `"boruvka"` na célula 3 |
| Sair só com os números (formato do juiz) | substituir os três `print` de `imprimir_consultas` por `print(peso_maximo)` |
| Tratar `X == Y` | `if inicio == fim: return [inicio], float("inf")` no início de `responder_consulta` |
| Tratar grafo desconexo | `if not nx.has_path(arvore_maxima, inicio, fim): return None, float("-inf")` |
| Salvar os gráficos | `plt.savefig(f"caso{n}.png", dpi=150, bbox_inches="tight")` antes de `plt.show()` |
| Layout ignorando pesos | `nx.spring_layout(grafo, seed=42, weight=None)` |
| Consultas mais rápidas | pré-processar LCA com binary lifting (`TEORIA.md`, Seção 9.3) |
