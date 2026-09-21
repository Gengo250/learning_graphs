# Trabalho 2 — Fundamentação Teórica

Documento teórico do problema do caminhão: definições formais, o algoritmo utilizado
(Kruskal na versão de maximização), a **árvore geradora máxima** e a demonstração de por
que ela resolve o problema.

> **Trilogia de documentos**
> - `LEIA.md` — visão geral do trabalho e explicação célula a célula.
> - `TEORIA.md` *(este)* — matemática: definições, teoremas, demonstrações, complexidade.
> - `CODIGO.md` — referência técnica de API: parâmetros, defaults, tipos, erros.

---

## Sumário

1. [Notação e definições formais](#1-notação-e-definições-formais)
2. [O problema como um problema maximin](#2-o-problema-como-um-problema-maximin)
3. [Árvores e árvores geradoras](#3-árvores-e-árvores-geradoras)
4. [Árvore geradora máxima](#4-árvore-geradora-máxima)
5. [As duas propriedades estruturais: corte e ciclo](#5-as-duas-propriedades-estruturais-corte-e-ciclo)
6. [Teorema central: a MaxST resolve todos os gargalos](#6-teorema-central-a-maxst-resolve-todos-os-gargalos)
7. [O algoritmo de Kruskal na versão de máximo](#7-o-algoritmo-de-kruskal-na-versão-de-máximo)
8. [Traço completo no exemplo do enunciado](#8-traço-completo-no-exemplo-do-enunciado)
9. [A fase de consultas](#9-a-fase-de-consultas)
10. [Alternativas algorítmicas e comparação](#10-alternativas-algorítmicas-e-comparação)
11. [Casos limites e robustez](#11-casos-limites-e-robustez)
12. [Interpretação: as "pontes de interesse"](#12-interpretação-as-pontes-de-interesse)
13. [Complexidade total da solução](#13-complexidade-total-da-solução)
14. [Mapeamento teoria → NetworkX](#14-mapeamento-teoria--networkx)
15. [Perguntas prováveis de arguição](#15-perguntas-prováveis-de-arguição)
16. [Referências](#16-referências)

---

## 1. Notação e definições formais

### 1.1 Grafo ponderado

O arquipélago é modelado por um **grafo não direcionado ponderado**

```
G = (V, E, w)
```

- `V` — conjunto finito de **vértices** (as ilhas), `|V| = I`, numeradas `1..I`;
- `E ⊆ { {u,v} : u,v ∈ V, u ≠ v }` — conjunto de **arestas** (as pontes), `|E| = P`;
- `w : E → ℤ` — **função peso**, onde `w(e)` é a carga máxima suportada pela ponte `e`.

O grafo é **não direcionado** porque uma ponte é atravessável nos dois sentidos, e é
**simples** (sem laços e sem arestas paralelas) na modelagem adotada — a Seção 11 discute
o que acontece quando a entrada viola essa hipótese.

### 1.2 Passeios, caminhos e conexidade

- Um **passeio** (*walk*) de `x` a `y` é uma sequência alternada
  `x = v0, e1, v1, e2, ..., ek, vk = y` com `ei = {v(i-1), vi} ∈ E`. Vértices podem repetir.
- Um **caminho** (*path*) é um passeio sem repetição de vértices.
- `G` é **conexo** se existe caminho entre todo par de vértices.
- Uma **componente conexa** é uma classe de equivalência da relação "existe caminho entre".

Denotamos por `𝒫(x,y)` o conjunto de todos os caminhos de `x` a `y` em `G`.

### 1.3 Cortes

Dada uma bipartição `V = S ∪ (V∖S)` com `S ≠ ∅` e `S ≠ V`, o **corte** induzido é

```
δ(S) = { {u,v} ∈ E : u ∈ S  e  v ∉ S }
```

ou seja, o conjunto de arestas que "cruzam" a fronteira. Cortes são a ferramenta central
das demonstrações das Seções 5 e 6: toda vez que quebramos uma árvore em duas partes,
qualquer rota alternativa entre as duas partes é obrigada a cruzar o mesmo corte.

### 1.4 Ciclos

Um **ciclo** é um caminho fechado `v0, v1, ..., vk = v0` com `k ≥ 3` e vértices internos
distintos. Um grafo sem ciclos é **acíclico** ou uma **floresta**.

---

## 2. O problema como um problema maximin

### 2.1 Capacidade de um caminho

Um caminhão que percorre o caminho `Q = (e1, ..., ek)` precisa atravessar **todas** as
pontes de `Q`. Logo, a carga máxima que `Q` comporta é limitada pela ponte mais fraca:

```
cap(Q) = min  w(e)          ("gargalo" / bottleneck de Q)
         e ∈ Q
```

Por convenção, o caminho trivial (de `x` para `x`, com zero arestas) tem
`cap = +∞`, porque o mínimo sobre o conjunto vazio é `+∞`.

### 2.2 Enunciado formal

Para cada consulta `(X, Y)`, a resposta pedida é

```
b(X, Y) =   max      cap(Q)   =   max        min   w(e)
          Q ∈ 𝒫(X,Y)              Q ∈ 𝒫(X,Y)  e ∈ Q
```

Esse é o problema do **caminho de gargalo máximo** (*maximum bottleneck path*), também
chamado de **caminho mais largo** (*widest path*) ou **maximum capacity path**. É um
problema **maximin**: maximizamos um mínimo.

### 2.3 Por que não é um problema de caminho mínimo

A diferença é a **operação de agregação ao longo do caminho**:

| Problema | Custo do caminho | Objetivo | Estrutura algébrica |
|---|---|---|---|
| Caminho mínimo (Dijkstra) | `Σ w(e)` | minimizar | semianel `(min, +)` |
| Gargalo máximo (este trabalho) | `min w(e)` | maximizar | semianel `(max, min)` |

Duas consequências matemáticas importantes:

**(a) Atravessar mais pontes não "gasta" capacidade.** Somar não faz sentido aqui: o
caminhão não fica mais pesado por passar em mais pontes. A função `min` é
**idempotente** (`min(a,a) = a`) e **absorvente**: o custo depende apenas do pior elemento,
não da quantidade de elementos. Por isso o caminho ótimo frequentemente é o **mais longo**
em número de arestas.

**(b) Monotonicidade.** Estender um caminho nunca melhora seu gargalo:

```
Q ⊆ Q'  ⟹  cap(Q') ≤ cap(Q)
```

Isso garante a **subestrutura ótima** necessária para algoritmos gulosos: se o melhor
caminho de `X` a `Y` passa por `Z`, seus dois trechos também são ótimos no sentido maximin
restrito. É o análogo do princípio de otimalidade de Bellman para o semianel `(max, min)`.

### 2.4 Caminhos vs. passeios

Poderíamos ter definido o problema sobre passeios em vez de caminhos. Não muda nada:

> **Lema 2.1.** Para todo passeio `W` de `x` a `y` existe um caminho `Q ⊆ W` com
> `cap(Q) ≥ cap(W)`.

*Demonstração.* Se `W` repete um vértice `v`, o trecho entre as duas ocorrências de `v` é
um passeio fechado e pode ser removido, produzindo um passeio menor com o mesmo par de
extremos e cujo conjunto de arestas é subconjunto do original. Pela monotonicidade (2.3b),
o gargalo não diminui. Repetindo até não haver repetição, obtemos um caminho. ∎

Portanto restringir a busca a caminhos simples não perde soluções — o que justifica
trabalhar dentro de uma árvore, onde só existe um caminho por par.

### 2.5 Exemplo concreto do enunciado

Consulta `4 → 3`. Existe a ponte direta `{4,3}` de peso `4`, mas o desvio
`4 → 2 → 3` usa pontes de pesos `7` e `8`:

```
cap(4-3)     = 4
cap(4-2-3)   = min(7, 8) = 7   ← melhor
```

A resposta é `7`. O caminho ótimo é o mais longo — evidência direta de que **caminho mínimo
não resolve este problema**.

Analogamente, a ponte `{1,3}` tem peso `0`: ela existe no grafo, mas nenhum caminhão de peso
positivo passa por ela. Ela nunca aparece em rota ótima quando há alternativa.

---

## 3. Árvores e árvores geradoras

### 3.1 Definições

- **Árvore**: grafo conexo e acíclico.
- **Árvore geradora** (*spanning tree*) de `G`: subgrafo `T = (V, E_T)` com `E_T ⊆ E` que é
  uma árvore e contém **todos** os vértices de `G`.

> **Teorema 3.1 (caracterizações equivalentes).** Para um grafo `T` com `n` vértices, são
> equivalentes:
> 1. `T` é uma árvore;
> 2. `T` é conexo e tem exatamente `n − 1` arestas;
> 3. `T` é acíclico e tem exatamente `n − 1` arestas;
> 4. existe **exatamente um** caminho entre cada par de vértices de `T`;
> 5. `T` é minimalmente conexo (remover qualquer aresta desconecta);
> 6. `T` é maximalmente acíclico (adicionar qualquer aresta cria exatamente um ciclo).

A propriedade **(4)** é a que este trabalho usa diretamente, então vale a demonstração:

> **Demonstração de (1) ⟹ (4).** *Existência*: `T` é conexo, logo há ao menos um caminho.
> *Unicidade*: suponha dois caminhos distintos `Q1 ≠ Q2` de `x` a `y`. A diferença simétrica
> `Q1 Δ Q2` é não vazia e todo vértice nela tem grau par (cada vértice interno contribui com
> 0 ou 2 arestas), o que força a existência de um ciclo — contradizendo a aciclicidade. ∎

A propriedade **(6)** também será usada: acrescentar a `T` uma aresta `g ∉ E_T` cria um
único ciclo, chamado **ciclo fundamental** de `g` em relação a `T`.

### 3.2 Quantas árvores geradoras existem?

Pela **fórmula de Cayley**, o grafo completo `K_n` tem `n^(n−2)` árvores geradoras
(`K_10` já tem 100 milhões). O **Teorema de Kirchhoff (Matrix-Tree)** generaliza para um
grafo qualquer: o número de árvores geradoras é qualquer cofator da matriz laplaciana
`L = D − A`.

A conclusão prática é imediata: **enumerar árvores geradoras é inviável**, e precisamos de
um algoritmo que construa a árvore ótima diretamente. É o que Kruskal faz.

---

## 4. Árvore geradora máxima

### 4.1 Definição

O **peso** de uma árvore geradora `T` é `w(T) = Σ w(e)` para `e ∈ E_T`. Uma **árvore
geradora máxima** (*maximum spanning tree*, MaxST) é uma árvore geradora `T*` tal que

```
w(T*) ≥ w(T)   para toda árvore geradora T de G
```

### 4.2 Dualidade mínimo ↔ máximo

Máximo e mínimo são o mesmo problema a menos de uma transformação que inverte a ordem:

> **Proposição 4.1.** Seja `w'(e) = −w(e)` (ou `w'(e) = C − w(e)` para qualquer constante
> `C`). Então `T` é árvore geradora **máxima** de `(G, w)` se e somente se `T` é árvore
> geradora **mínima** de `(G, w')`.

*Demonstração.* `w'(T) = Σ (−w(e)) = −w(T)` (ou `(n−1)C − w(T)`). Ambas são funções
estritamente decrescentes de `w(T)`, logo maximizar `w(T)` equivale a minimizar `w'(T)`. ∎

Isso significa que **todo teorema de MST vale para MaxST com as desigualdades invertidas**,
e que implementações de MST servem para MaxST trocando o sentido da comparação. O NetworkX
faz exatamente isso: `maximum_spanning_tree` chama a mesma rotina de Kruskal com
`minimum=False`, o que só inverte a ordenação (`sorted(..., reverse=True)`).

### 4.3 Unicidade

> **Proposição 4.2.** Se todos os pesos de `G` são distintos, a MaxST é única.

Com empates a MaxST pode não ser única — mas:

> **Proposição 4.3.** Todas as MaxSTs de `G` têm o **mesmo multiconjunto de pesos**.

*Esboço.* Sejam `T1` e `T2` MaxSTs distintas e `e` a aresta de maior peso em `T1 ∖ T2`
(desempatando por índice). Acrescentar `e` a `T2` cria um ciclo fundamental com alguma
aresta `f ∉ T1` cruzando o corte induzido por `e` em `T1`. Maximalidade de ambas força
`w(e) = w(f)`, e `T2 − f + e` é MaxST mais próxima de `T1`. Indução sobre `|T1 ∖ T2|`. ∎

Isso tem uma consequência importante para o trabalho: **a resposta das consultas não depende
de qual MaxST o algoritmo devolveu** (Corolário 6.3).

---

## 5. As duas propriedades estruturais: corte e ciclo

São os dois lemas que sustentam todos os algoritmos gulosos de árvore geradora. Enunciados
aqui na **versão de maximização**.

### 5.1 Propriedade do corte

> **Teorema 5.1 (cut property, versão máxima).** Seja `S ⊂ V` um corte não trivial e seja
> `e` a aresta de **maior** peso em `δ(S)`. Se `e` é a única de peso máximo no corte, então
> `e` pertence a **toda** MaxST de `G`.

*Demonstração.* Suponha que uma MaxST `T` não contenha `e = {u,v}`, com `u ∈ S`, `v ∉ S`.
O caminho único de `u` a `v` em `T` começa em `S` e termina fora de `S`, logo contém alguma
aresta `f ∈ δ(S)`, com `w(f) < w(e)` pela hipótese de unicidade do máximo. A troca
`T' = T − f + e` é ainda geradora (remover `f` parte `T` em duas componentes, e `e` as
reconecta, pois `e` cruza o mesmo corte) e tem `w(T') = w(T) − w(f) + w(e) > w(T)`,
contradizendo a maximalidade de `T`. ∎

### 5.2 Propriedade do ciclo

> **Teorema 5.2 (cycle property, versão máxima).** Seja `C` um ciclo de `G` e `f` a aresta
> de **menor** peso de `C`. Se `f` é a única de peso mínimo em `C`, então `f` não pertence a
> nenhuma MaxST.

*Demonstração.* Se `f = {u,v}` estivesse em uma MaxST `T`, remover `f` partiria `T` em
componentes `A ∋ u` e `B ∋ v`. O restante do ciclo `C − f` é um caminho de `u` a `v`, logo
contém alguma aresta `g` cruzando o corte `δ(A)`, com `w(g) > w(f)`. Então
`T − f + g` é geradora e mais pesada. Contradição. ∎

Esses dois teoremas dizem, em resumo: **as arestas pesadas de cada corte entram, as arestas
leves de cada ciclo saem**. É exatamente essa intuição que a Seção 6 converte em gargalos.

---

## 6. Teorema central: a MaxST resolve todos os gargalos

Este é o resultado que justifica todo o notebook.

> **Teorema 6.1 (Hu, 1961).** Seja `T` uma árvore geradora máxima de `G` conexo. Para todo
> par `X, Y ∈ V`, o caminho único `Q_T(X,Y)` dentro de `T` é um caminho de gargalo máximo em
> `G`. Ou seja:
>
> ```
> b(X, Y)  =   min   w(e)
>            e ∈ Q_T(X,Y)
> ```

### 6.1 Demonstração (argumento de troca)

Seja `Q_T` o caminho único de `X` a `Y` em `T` e `b = cap(Q_T)` seu gargalo.

**(≥) O caminho da árvore não é melhor que o ótimo.** Trivial: `Q_T` é um caminho de `G`,
logo `b ≤ b(X,Y)` por definição de máximo.

**(≤) Nenhum caminho de `G` é estritamente melhor.** Suponha, por absurdo, que exista
`Q_G ∈ 𝒫(X,Y)` com `cap(Q_G) = b' > b`, isto é, **todas** as arestas de `Q_G` têm peso
`> b`.

1. Seja `f ∈ Q_T` a aresta que realiza o gargalo, `w(f) = b`.
2. Remover `f` de `T` parte a árvore em duas componentes `A` e `B`. Como `f` está no caminho
   de `X` a `Y`, temos `X ∈ A` e `Y ∈ B` (sem perda de generalidade).
3. `Q_G` vai de `X ∈ A` até `Y ∈ B`, portanto **cruza o corte `δ(A)`**: existe
   `g ∈ Q_G ∩ δ(A)`.
4. Por hipótese, `w(g) > b = w(f)`.
5. `T' = T − f + g` é uma árvore geradora: tem `n − 1` arestas e é conexa, pois `g` religa
   `A` a `B`.
6. `w(T') = w(T) − w(f) + w(g) > w(T)`.

O passo 6 contradiz `T` ser máxima. Logo não existe tal `Q_G`, e `b = b(X,Y)`. ∎

O núcleo do argumento é o passo 3: **qualquer rota alternativa é obrigada a cruzar o mesmo
corte que a aresta-gargalo da árvore**. Isso é a propriedade do corte (Teorema 5.1)
aplicada ponto a ponto.

### 6.2 Demonstração alternativa (via propriedade do ciclo)

Seja `g` uma aresta fora de `T` e `C` seu ciclo fundamental. Pela Proposição 4.3 e pelo
Teorema 5.2, `w(g) ≤ w(e)` para toda `e ∈ C − g`. Logo, trocar o uso de `g` pelo trecho
`C − g` (que está inteiramente em `T`) **nunca piora** o gargalo. Aplicando essa substituição
a cada aresta de um caminho ótimo qualquer que esteja fora de `T`, obtemos um passeio contido
em `T` com gargalo `≥` ao original; pelo Lema 2.1 ele contém um caminho de `T` com gargalo
`≥`. Como em `T` só existe um caminho `X→Y`, esse caminho é ótimo. ∎

### 6.3 Corolários

> **Corolário 6.1 (todas as respostas de uma só estrutura).** Uma única MaxST responde
> simultaneamente às `I(I−1)/2` consultas possíveis. Construí-la uma vez por caso de teste
> amortiza o custo entre todas as `S` consultas.

> **Corolário 6.2 (ultrametricidade).** A função `b` satisfaz a **desigualdade ultramétrica
> invertida**:
> ```
> b(x, z) ≥ min( b(x, y), b(y, z) )    para todos x, y, z
> ```
> *Prova:* concatenar um caminho ótimo `x→y` com um ótimo `y→z` produz um passeio cujo
> gargalo é o mínimo dos dois; pelo Lema 2.1 existe caminho `x→z` pelo menos tão bom. ∎
>
> Consequência: `−b` é uma **ultramétrica** sobre `V`, e o problema é matematicamente
> equivalente a *single-linkage clustering* — a MaxST é o dendrograma do agrupamento por
> ligação simples com similaridade `w`.

> **Corolário 6.3 (independência da MaxST escolhida).** Se `T1` e `T2` são MaxSTs de `G`,
> então `cap(Q_T1(X,Y)) = cap(Q_T2(X,Y)) = b(X,Y)` para todo par. Ou seja, empates de peso
> podem mudar **quais** pontes aparecem no desenho, mas **nunca** mudam as respostas
> numéricas do trabalho.

### 6.4 A recíproca é falsa

O Teorema 6.1 diz `MaxST ⟹ árvore de gargalo máximo`. A recíproca **não** vale: existem
árvores geradoras que realizam todos os gargalos ótimos sem ter peso total máximo (elas são
chamadas *minimax/maximin spanning trees*, e formam uma classe estritamente maior). Isso é
útil saber na arguição: usar a MaxST é uma condição **suficiente**, não necessária — mas é
a que temos algoritmo pronto e eficiente para calcular.

---

## 7. O algoritmo de Kruskal na versão de máximo

### 7.1 Ideia

Kruskal é um algoritmo **guloso** que constrói uma floresta crescente:

> Percorra as arestas em ordem **decrescente** de peso. Aceite a aresta se ela conectar duas
> componentes diferentes; descarte se ela fechar ciclo. Pare com `n − 1` arestas.

### 7.2 Pseudocódigo

```
KRUSKAL-MAX(V, E, w):
    T ← ∅
    para cada v ∈ V:
        MAKE-SET(v)                        # cada ilha é sua própria componente

    ordenar E em ordem DECRESCENTE de w

    para cada aresta (u, v) ∈ E nessa ordem:
        se FIND(u) ≠ FIND(v):              # extremos em componentes distintas
            T ← T ∪ {(u, v)}               # aceita: não fecha ciclo
            UNION(u, v)
        # senão: descarta (fecharia ciclo)

    retornar T
```

### 7.3 Corretude

> **Teorema 7.1.** `KRUSKAL-MAX` devolve uma árvore geradora máxima (ou, se `G` for
> desconexo, uma **floresta geradora máxima**: uma MaxST por componente).

*Demonstração (invariante de troca).* O invariante é: *em todo momento, `T` é subconjunto de
alguma MaxST de `G`.*

- **Base.** `T = ∅` é subconjunto de qualquer MaxST.
- **Passo.** Suponha `T ⊆ T*` para alguma MaxST `T*`, e seja `e = {u,v}` a próxima aresta
  aceita. Seja `S` a componente de `T` que contém `u`. Como `e` foi aceita, `v ∉ S`, logo
  `e ∈ δ(S)`. Nenhuma aresta de `δ(S)` foi examinada antes de `e` e aceita (senão `S` seria
  maior), e todas as arestas de `δ(S)` já examinadas e descartadas fechariam ciclo dentro de
  `S`, o que é impossível para arestas de corte. Portanto **`e` é a aresta de maior peso de
  `δ(S)` ainda disponível**, e pela ordenação decrescente `w(e) ≥ w(f)` para toda
  `f ∈ δ(S)`. Se `e ∈ T*`, nada a fazer. Se `e ∉ T*`, o caminho `u→v` em `T*` contém alguma
  `f ∈ δ(S)` com `w(f) ≤ w(e)`; então `T* − f + e` é geradora com peso `≥ w(T*)`, portanto
  também MaxST, e contém `T ∪ {e}`. O invariante se mantém.
- **Término.** O algoritmo para quando nenhuma aresta mais pode ser aceita, isto é, quando
  `T` é maximalmente acíclico dentro de cada componente — uma floresta geradora. Pelo
  invariante, ela está contida em uma MaxST; tendo o mesmo número de arestas, **é** uma
  MaxST. ∎

Note que o passo indutivo é precisamente a **propriedade do corte** (Teorema 5.1), aplicada
com a versão "≤" que tolera empates.

### 7.4 A estrutura union-find

O teste `FIND(u) ≠ FIND(v)` é o coração da eficiência. Usa-se **DSU** (*disjoint-set
union*), que mantém uma partição dinâmica de `V` com duas otimizações:

- **compressão de caminho** (*path compression*): durante `FIND`, todos os nós visitados
  passam a apontar direto para a raiz;
- **união por tamanho/rank**: a árvore menor é pendurada na maior, limitando a altura.

Com as duas, uma sequência de `m` operações sobre `n` elementos custa
`O(m · α(n))`, onde `α` é a **inversa da função de Ackermann** — menor que 5 para qualquer
`n` fisicamente construível. Na prática, tempo constante amortizado.

> A `UnionFind` do NetworkX (`networkx/utils/union_find.py`) implementa exatamente isso:
> compressão de caminho no `__getitem__` e união pelo maior `weights[root]` (tamanho).

### 7.5 Complexidade

| Etapa | Custo |
|---|---|
| Inicializar DSU | `O(I)` |
| Ordenar as `P` arestas | `O(P log P)` |
| `P` operações `FIND`/`UNION` | `O(P · α(I))` |
| **Total** | **`O(P log P)` = `O(P log I)`** |

A última igualdade vale porque `P ≤ I(I−1)/2`, logo `log P ≤ 2 log I`. **A ordenação
domina**: o gargalo do algoritmo não é a teoria de grafos, é o `sort`.

Memória: `O(I + P)`.

### 7.6 Por que Kruskal e não Prim

Ambos são corretos e o notebook poderia usar qualquer um (`algorithm="prim"` no NetworkX).
A escolha por Kruskal neste trabalho se justifica por:

1. **Alinhamento conceitual**: Kruskal processa as arestas da mais forte para a mais fraca,
   que é exatamente a narrativa do problema ("use primeiro as pontes que aguentam mais
   peso"). A cada passo, as componentes do DSU são exatamente os conjuntos de ilhas
   mutuamente alcançáveis com carga `≥ w` atual — uma leitura direta do gargalo.
2. **Grafos esparsos**: para `P` pequeno, `O(P log P)` é ótimo na prática.
3. **Determinismo e verificabilidade**: a ordem de exame das arestas é explicitamente a
   ordenação por peso, fácil de reproduzir à mão na defesa (Seção 8).

Prim seria preferível em grafos muito densos com heap de Fibonacci (`O(P + I log I)`), o
que não é o caso aqui.

---

## 8. Traço completo no exemplo do enunciado

Entrada (`testes/entrada.txt`):

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

### 8.1 Execução de Kruskal-Max

Arestas ordenadas por peso decrescente:
`(1,2,9)`, `(2,3,8)`, `(2,4,7)`, `(3,4,4)`, `(1,3,0)`.

| Passo | Aresta | Peso | `FIND(u)` vs `FIND(v)` | Decisão | Componentes após |
|---|---|---|---|---|---|
| 0 | — | — | — | início | `{1} {2} {3} {4}` |
| 1 | `{1,2}` | 9 | `1 ≠ 2` | **aceita** | `{1,2} {3} {4}` |
| 2 | `{2,3}` | 8 | `{1,2} ≠ {3}` | **aceita** | `{1,2,3} {4}` |
| 3 | `{2,4}` | 7 | `{1,2,3} ≠ {4}` | **aceita** | `{1,2,3,4}` |
| 4 | `{3,4}` | 4 | mesma componente | descarta (ciclo `3-2-4-3`) | `{1,2,3,4}` |
| 5 | `{1,3}` | 0 | mesma componente | descarta (ciclo `1-2-3-1`) | `{1,2,3,4}` |

Parou com `3 = I − 1` arestas.

```
Árvore geradora máxima:  T = { (1,2,9), (2,3,8), (2,4,7) }        w(T) = 24
Pontes descartadas:          { (3,4,4), (1,3,0) }
```

Topologia de `T` (estrela centrada em 2):

```
        9          8
   1 ———————— 2 ———————— 3
              |
              | 7
              |
              4
```

*(Valores conferidos executando o notebook: `nx.maximum_spanning_tree` devolve exatamente
essas três arestas.)*

### 8.2 Respostas das consultas

| Consulta | Caminho único em `T` | Pesos | `min` | Saída esperada |
|---|---|---|---|---|
| `1 → 4` | `1 - 2 - 4` | 9, 7 | **7** | 7 ✔ |
| `2 → 1` | `2 - 1` | 9 | **9** | 9 ✔ |
| `3 → 1` | `3 - 2 - 1` | 8, 9 | **8** | 8 ✔ |
| `4 → 3` | `4 - 2 - 3` | 7, 8 | **7** | 7 ✔ |

Bate integralmente com o gabarito do enunciado (`7 9 8 7`).

### 8.3 Leitura das descartadas

- **`{3,4}` com peso 4** — descartada no passo 4 porque fecharia o ciclo `3-2-4-3`. Pela
  propriedade do ciclo (Teorema 5.2), ela é a aresta de menor peso desse ciclo
  (`4 < 7 < 8`), logo não pertence a nenhuma MaxST. E de fato a consulta `4 → 3` prefere o
  desvio (gargalo 7 > 4).
- **`{1,3}` com peso 0** — menor peso do ciclo `1-2-3-1` (`0 < 8 < 9`). Inútil para qualquer
  caminhão de peso positivo.

Esse é o ponto que fecha o item **"evidenciar pontes de interesse"** do enunciado: as
arestas descartadas não são apenas "as que sobraram" — são demonstradamente arestas que
**nenhuma rota ótima precisa usar**.

---

## 9. A fase de consultas

### 9.1 O que precisa ser feito

Pelo Teorema 6.1, responder `(X, Y)` é apenas:

1. recuperar o caminho único `X → Y` dentro de `T`;
2. devolver o mínimo dos pesos das arestas desse caminho.

### 9.2 Por que uma busca sem peso é suficiente

O notebook usa `nx.shortest_path(arvore_maxima, inicio, fim)` **sem** o parâmetro `weight`.
Isso é intencional e teoricamente justificado:

- sem `weight`, o NetworkX roda uma **BFS** e devolve o caminho com menos arestas;
- pelo Teorema 3.1(4), dentro de uma árvore existe **exatamente um** caminho entre dois
  vértices;
- logo "caminho mais curto" e "o caminho" coincidem — a BFS não está otimizando nada, está
  apenas **recuperando** o caminho único.

Passar `weight="weight"` aqui seria um erro conceitual: faria o algoritmo minimizar a
**soma** dos pesos, que não tem significado no problema (Seção 2.3). Como o caminho é único,
nem mudaria o resultado — mas indicaria modelagem errada.

Custo: `O(I)` por consulta (uma árvore tem `I − 1` arestas, então BFS é linear em `I`).

### 9.3 Alternativas mais rápidas para a fase de consultas

Não são necessárias na escala deste trabalho (`OBS3` do enunciado: "não farei grafos tão
grandes"), mas são o que se usaria em competição:

| Técnica | Pré-processamento | Por consulta |
|---|---|---|
| BFS/DFS na árvore (**usada**) | — | `O(I)` |
| **LCA com binary lifting** guardando `min` do salto | `O(I log I)` | `O(log I)` |
| **Kruskal reconstruction tree** + LCA | `O(P log P)` | `O(log I)` ou `O(1)` com Euler tour + sparse table |
| **Tarjan offline** (DSU + LCA offline) | `O((I + S) α(I))` | amortizado quase `O(1)` |

A ideia do **binary lifting** é armazenar, para cada vértice `v` e cada potência `2^k`, o
ancestral `up[v][k]` e o **mínimo peso** `mn[v][k]` no trecho de `v` até esse ancestral.
Subindo `X` e `Y` até o LCA em saltos de potências de 2 e acumulando `min`, obtém-se o
gargalo em `O(log I)`.

---

## 10. Alternativas algorítmicas e comparação

Existem várias formas de resolver caminho de gargalo máximo. Todas foram consideradas; a
MaxST venceu pelo perfil do problema (**muitas consultas sobre o mesmo grafo**).

### 10.1 Dijkstra "maximin" (widest path)

Troca-se a relaxação `dist[v] = min(dist[v], dist[u] + w)` por

```
cap[v] = max( cap[v], min(cap[u], w(u,v)) )
```

e usa-se uma fila de prioridade de **máximo**. Corretude vem do fato de `(max, min)` ser um
semianel com as mesmas propriedades de monotonicidade exigidas por Dijkstra.

Custo: `O(P log I)` **por consulta** → `O(S · P log I)` no total.

### 10.2 Busca binária no peso + teste de conectividade

Binária sobre os pesos distintos; para um limiar `θ`, testar com BFS/DFS se `X` e `Y` estão
conectados usando apenas arestas com `w ≥ θ`.

Custo: `O(P log P)` por consulta.

### 10.3 Algoritmo de Camerini

Usa seleção por mediana (estilo *median of medians*) para particionar as arestas sem
ordenar, alcançando **`O(P)` linear** para um par. Ótimo assintoticamente para consulta
única, mas complexo de implementar e sem ganho aqui.

### 10.4 Prim máximo / Borůvka

Outras construções de MaxST. Prim: `O(P log I)` com heap binário. Borůvka: `O(P log I)`, com
a vantagem de ser naturalmente paralelizável. Resultado equivalente ao de Kruskal
(Corolário 6.3).

### 10.5 Tabela comparativa

| Abordagem | Pré-processamento | Por consulta | Total (`S` consultas) | Adotada |
|---|---|---|---|---|
| **MaxST (Kruskal) + BFS** | `O(P log P)` | `O(I)` | **`O(P log P + S·I)`** | ✅ |
| MaxST + LCA binary lifting | `O(P log P + I log I)` | `O(log I)` | `O(P log P + S log I)` | — |
| Dijkstra maximin | — | `O(P log I)` | `O(S · P log I)` | — |
| Busca binária + BFS | `O(P log P)` (ordenar) | `O(P log P)` | `O(S · P log P)` | — |
| Camerini | — | `O(P)` | `O(S · P)` | — |
| Floyd-Warshall maximin | `O(I³)` | `O(1)` | `O(I³ + S)` | — |

**Justificativa da escolha.** O enunciado fixa um grafo e faz `S` perguntas sobre ele. Toda
abordagem "por consulta" paga o grafo inteiro `S` vezes; a MaxST paga uma vez e depois cada
consulta é linear na árvore. Além disso, só a MaxST entrega **de graça** o item
"evidenciar pontes de interesse" — as outras respondem o número mas não identificam a
sub-rede útil.

> Vale registrar o caso extremo: para `S` muito grande (`S ≫ I²`), Floyd-Warshall na versão
> maximin (`d[i][j] = max(d[i][j], min(d[i][k], d[k][j]))`) daria consultas `O(1)` — mas com
> `O(I³)` de pré-processamento e `O(I²)` de memória, inviável e desnecessário aqui.

---

## 11. Casos limites e robustez

### 11.1 Grafo desconexo

Se o arquipélago tiver ilhas em componentes separadas, **não existe** árvore geradora. O
`nx.maximum_spanning_tree` devolve nesse caso uma **floresta geradora máxima** (todos os
vértices, uma MaxST por componente) — o nome da função é enganoso.

Consequências:
- teoricamente, `b(X,Y) = −∞` (nenhum caminhão chega): a consulta é impossível;
- no código, `nx.shortest_path` lança `NetworkXNoPath` (verificado: *"No path between 1 and 3"*).

O Teorema 6.1 continua válido **dentro de cada componente**.

### 11.2 Consulta trivial `X == Y`

O caminho tem zero arestas; pela convenção da Seção 2.1, `b(X,X) = +∞` (o caminhão já está
no destino, não atravessa ponte alguma). No código, `min([])` lança
`ValueError: min() iterable argument is empty` (verificado). Se o caso de teste do professor
puder conter `X == Y`, é preciso tratar explicitamente.

### 11.3 Peso zero e pesos negativos

- **Peso 0** aparece no próprio enunciado (`1 3 0`). Nada quebra: a ponte existe, entra na
  ordenação e simplesmente perde para qualquer alternativa positiva. Semanticamente, é uma
  ponte que nenhum caminhão carregado atravessa.
- **Pesos negativos** não teriam sentido físico, mas a teoria é indiferente: Kruskal e o
  Teorema 6.1 só dependem da **ordem total** dos pesos, não do sinal.

### 11.4 Arestas paralelas e laços

A modelagem com `nx.Graph` é de grafo **simples**:

- **Arestas paralelas** (duas pontes ligando o mesmo par de ilhas) são colapsadas, e
  `add_weighted_edges_from` mantém **a última lida**, não a de maior peso (verificado:
  `[(1,2,9),(1,2,3)]` resulta em peso `3`). Se a entrada oficial puder conter pontes
  paralelas, seria necessário usar `nx.MultiGraph` ou manter o máximo manualmente.
  Teoricamente, para o problema de gargalo, **só a paralela de maior peso importa**: as
  demais são a aresta de menor peso de um ciclo de tamanho 2 e caem pelo Teorema 5.2.
- **Laços** (`u == v`) são armazenados pelo `nx.Graph` mas nunca entram na árvore, porque
  `FIND(u) == FIND(u)` sempre (verificado). Estão corretamente ignorados.

### 11.5 Empates de peso

Com pesos repetidos a MaxST não é única (Prop. 4.2/4.3), e a árvore concreta depende da
ordem de desempate do `sort` (que em Python é **estável**, preservando a ordem de leitura do
arquivo). Isso pode alterar **quais** pontes aparecem em vermelho no gráfico, mas pelo
Corolário 6.3 **nunca altera as respostas numéricas**. Vale dizer isso explicitamente na
defesa, porque é a pergunta natural do professor ao ver um empate.

---

## 12. Interpretação: as "pontes de interesse"

O enunciado pede (2 pontos) "evidenciar as pontes de interesse, que poderão ser usadas pelos
caminhoneiros". A MaxST responde isso formalmente.

### 12.1 Toda aresta da árvore é útil

> **Proposição 12.1.** Toda aresta `e = {u,v} ∈ T` está em pelo menos uma rota ótima.

*Demonstração.* O caminho único de `u` a `v` em `T` é a própria aresta `e`. Pelo Teorema 6.1,
`b(u,v) = w(e)`. Logo `e` é, sozinha, uma rota ótima para a consulta `(u,v)`. ∎

### 12.2 Nenhuma aresta fora da árvore é necessária

> **Proposição 12.2.** Para toda consulta existe uma rota ótima que usa **apenas** arestas de
> `T`.

*Demonstração.* É o próprio Teorema 6.1: o caminho `Q_T(X,Y)` é ótimo e está contido em `T`. ∎

### 12.3 A nuance dos empates

Com pesos repetidos, uma aresta descartada pode pertencer a **outra** MaxST e estar em uma
rota igualmente ótima. O enunciado correto é portanto:

> As pontes fora da MaxST **nunca são estritamente necessárias**: para cada uma delas
> existe rota alternativa dentro da árvore com gargalo **igual ou melhor**.

Sem empates (pesos todos distintos), a MaxST é única e a separação "útil / inútil" é exata.

### 12.4 Cuidado com o homônimo "ponte"

Em teoria dos grafos, **ponte** (*bridge* ou *cut edge*) é uma aresta cuja remoção aumenta o
número de componentes conexas. O enunciado usa "ponte" no sentido coloquial (a aresta
física). São conceitos diferentes, e vale distinguir na apresentação. A relação entre eles:

> **Proposição 12.3.** Toda cut edge de `G` pertence a **toda** árvore geradora de `G` — em
> particular, à MaxST, independentemente do seu peso.

*Prova:* uma cut edge não pertence a ciclo algum; se fosse omitida, as duas componentes que
ela separa ficariam desconexas na subárvore. ∎

Ou seja: uma ponte que é o único acesso a uma ilha sempre aparece em vermelho no gráfico,
mesmo que seja a mais fraca do arquipélago — e ela é necessariamente o gargalo de toda
consulta que cruza aquele corte. É o "ponto crítico" da rede, e é exatamente isso que o
arquivo `testes/teste_2_ponte_critica.txt` exercita.

### 12.5 Leitura de engenharia

A MaxST tem exatamente `I − 1` arestas. Logo, das `P` pontes do arquipélago:

- `I − 1` formam a **sub-rede logística essencial**;
- `P − I + 1` (o **número ciclomático**, ou primeiro número de Betti do grafo) podem ser
  fechadas para manutenção **sem reduzir a capacidade de nenhuma rota**.

No exemplo: `P − I + 1 = 5 − 4 + 1 = 2` pontes redundantes, exatamente as duas descartadas.

---

## 13. Complexidade total da solução

Para um caso de teste com `I` ilhas, `P` pontes e `S` consultas:

| Fase | Custo de tempo | Memória |
|---|---|---|
| Leitura do arquivo (`ler_casos`) | `O(P + S)` | `O(P + S)` |
| Construção do grafo (`criar_grafo`) | `O(I + P)` | `O(I + P)` |
| MaxST via Kruskal (`resolver_caso`) | `O(P log P)` | `O(I + P)` |
| Cada consulta (BFS na árvore + `min`) | `O(I)` | `O(I)` |
| Todas as `S` consultas | `O(S · I)` | — |
| Plotagem (`spring_layout` iterativo) | `O(k · I²)` por gráfico | `O(I + P)` |
| **Total algorítmico** | **`O(P log P + S · I)`** | **`O(I + P)`** |

Para `K` casos no mesmo arquivo, soma-se sobre os casos. Observe que **a plotagem é a parte
mais cara** em grafos maiores (o layout de molas é quadrático por iteração) — o que é
aceitável porque é requisito visual do enunciado, não do algoritmo.

---

## 14. Mapeamento teoria → NetworkX

| Conceito teórico | Elemento do código | Seção |
|---|---|---|
| `G = (V, E, w)` não direcionado ponderado | `nx.Graph()` + `add_weighted_edges_from(..., weight="weight")` | 1.1 |
| `V = {1..I}`, inclusive ilhas isoladas | `add_nodes_from(range(1, I+1))` | 11.1 |
| Árvore geradora máxima `T*` | `nx.maximum_spanning_tree(G, weight="weight", algorithm="kruskal")` | 4.1 |
| Kruskal decrescente + union-find | interno: `sorted(..., reverse=True)` + `nx.utils.UnionFind` | 7.2, 7.4 |
| Caminho único em árvore (Teor. 3.1(4)) | `nx.shortest_path(T, x, y)` **sem** `weight` (BFS) | 9.2 |
| `cap(Q) = min w(e)` | `min(pesos_do_caminho)` | 2.1 |
| Arestas de interesse `E_T` | `arvore_maxima.edges()` → vermelho | 12.1 |
| Arestas redundantes `E ∖ E_T` | filtro com `not arvore_maxima.has_edge(...)` → cinza tracejado | 12.2 |

A explicação operacional de cada parâmetro está no `LEIA.md`, Seção 4.

---

## 15. Perguntas prováveis de arguição

**Por que não Dijkstra?**
Porque o custo de um caminho não é a soma dos pesos, e sim o mínimo. Dijkstra otimiza no
semianel `(min, +)`; este problema vive no semianel `(max, min)` (Seção 2.3). No exemplo,
Dijkstra escolheria a ponte direta `4-3` (peso 4) quando a resposta certa é o desvio
`4-2-3` (gargalo 7).

**Por que árvore geradora *máxima* e não *mínima*?**
Queremos preservar as pontes mais fortes. A MST mínima faria o oposto e responderia o
**gargalo mínimo** entre os pares — o problema dual (útil, por exemplo, para "qual o
caminho que minimiza a maior altura a escalar").

**Por que a árvore não perde nenhuma solução?**
Teorema 6.1 (Seção 6.1): se houvesse caminho melhor fora da árvore, ele cruzaria o corte da
aresta-gargalo com uma aresta mais pesada, e a troca produziria uma árvore geradora mais
pesada — contradizendo a maximalidade.

**E se houver empate de pesos e a árvore não for única?**
As respostas numéricas são invariantes (Corolário 6.3). Só muda o desenho.

**Qual a complexidade?**
`O(P log P)` para construir a árvore (uma vez por caso) e `O(I)` por consulta:
`O(P log P + S·I)` no total. A ordenação domina.

**Por que `shortest_path` sem `weight`?**
Porque dentro de uma árvore o caminho é único (Teor. 3.1(4)); a BFS só o recupera, não
otimiza nada. Passar `weight` minimizaria a soma, o que não tem significado no problema.

**O que garante que as pontes vermelhas são as "de interesse"?**
Proposição 12.1 (toda aresta da árvore é a rota ótima dos seus próprios extremos) e
Proposição 12.2 (nenhuma aresta de fora é necessária).

**O que acontece se o grafo for desconexo?**
A função devolve uma floresta geradora máxima e as consultas entre componentes distintas não
têm resposta (`−∞`); no código, `NetworkXNoPath` (Seção 11.1).

**Quantas pontes poderiam ser interditadas sem prejuízo?**
`P − I + 1` (número ciclomático) — no exemplo, 2 (Seção 12.5).

---

## 16. Referências

1. **Hu, T. C.** *The maximum capacity route problem.* Operations Research, 9(6), 1961 —
   resultado original relacionando árvore geradora máxima e caminhos de capacidade máxima.
2. **Pollack, M.** *The maximum capacity route through a network.* Operations Research, 8(5),
   1960.
3. **Kruskal, J. B.** *On the shortest spanning subtree of a graph and the traveling salesman
   problem.* Proc. AMS, 7(1), 1956.
4. **Camerini, P. M.** *The min-max spanning tree problem and some extensions.* Information
   Processing Letters, 7(1), 1978 — algoritmo linear para o gargalo.
5. **Tarjan, R. E.** *Efficiency of a good but not linear set union algorithm.* JACM, 22(2),
   1975 — análise `α(n)` do union-find.
6. **Cormen, Leiserson, Rivest, Stein.** *Introduction to Algorithms*, 4ª ed. — Cap. 21
   (estruturas para conjuntos disjuntos) e Cap. 23 (árvores geradoras mínimas: propriedades
   de corte e ciclo).
7. **Ahuja, Magnanti, Orlin.** *Network Flows: Theory, Algorithms and Applications*, 1993 —
   caminhos de gargalo e formulações maximin.
8. **Bondy & Murty.** *Graph Theory*, 2008 — caracterizações de árvores, Cayley,
   Matrix-Tree.
9. Documentação do NetworkX 3.6: `maximum_spanning_tree`, `kruskal_mst_edges`,
   `shortest_path`, `utils.UnionFind`.
