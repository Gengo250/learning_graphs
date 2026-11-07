# Terraria Network Analysis

Trabalho final de Grafos: dependências de crafting e relações documentadas do Terraria.
A implementação completa está em [`notebooks/analysis.ipynb`](notebooks/analysis.ipynb).
O notebook refatora a primeira etapa existente, preserva suas dependências e responde às
questões de [`docs/LEIA.md`](docs/LEIA.md) com resultados calculados.

## Executar

Na pasta `src/grafos_network/workspace_university/trabalho-3/`:

```bash
uv sync
uv run jupyter notebook notebooks/analysis.ipynb
```

Selecione **Python 3 (ipykernel)** e execute todas as células em ordem. O notebook confere
que o kernel pertence à `.venv` do projeto. Os caminhos funcionam tanto a partir da raiz
do projeto quanto de `notebooks/`. Python 3.12 e dependências são gerenciados por `uv.lock`;
não foram necessárias novas dependências.

Execução integral sem interface:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/analysis.ipynb --ExecutePreprocessor.timeout=240
```

A execução foi verificada com Python 3.12.13 e NetworkX 3.7. Leva cerca de 35 segundos
nesta máquina, variando conforme o hardware. Não consulta a internet nem grava gráficos,
CSVs ou arquivos de resultados: as figuras e tabelas permanecem no notebook.
Em um sandbox que bloqueie sockets locais, o kernel Jupyter precisa da permissão correspondente.

## Representações

| Grafo | Significado | Vértices | Arestas |
|---|---|---:|---:|
| `G` | `DiGraph`: ingrediente → produto, preservado da primeira etapa | 3.773 | 7.045 |
| `G_full` | `MultiDiGraph`: entidades e relações documentadas | 10.672 | 28.710 |
| `H` | Projeção simples não dirigida de crafting, principal acadêmica | 3.773 | 6.692 |
| `H_full` | Projeção simples de todas as relações, somente descritiva | 10.672 | 28.150 |

Contagens da execução validada; o notebook as recalcula. `H` é reconstruído por caminhos
Item → Receita → Item em `G_full` e conferido contra `G`. As comparações sintéticas usam
somente `H`; não misturam métricas de representações diferentes.

Os slots de uma receita são requisitos conjuntos; opções de um grupo e receitas distintas
são alternativas. `recipes_desktop` e os nós de receita conservam requisitos, quantidades,
estações e campos originais. `G.edges[u, v]['uses']` registra cada uso. Quantidades e
probabilidades de drop **não são pesos de aresta**.

A refatoração substitui validações redundantes por verificações de integridade e elimina
o cálculo manual de posições/interseções no desenho da Terra Blade. A figura usa
`multipartite_layout` e mantém todos os ancestrais: 32 itens e 40 relações, incluindo minérios.

## Fontes e versões

Fonte dos 12 JSONs: **[Terraria Progress Tracker](https://github.com/Doeschi/Terraria-Progress-Tracker)**,
de Doeschi, diretório `pipeline/data_readable`. Dados derivados da
[Terraria Wiki](https://terraria.wiki.gg/), sob **CC BY-NC-SA 4.0**, conforme a documentação da fonte.
Os JSONs são distribuídos sem alterações; a transformação analítica acontece somente em memória.

- Commit fixado: `e1726af0908d928a3e2fa437286558827a6dd3b0` (2026-10-25).
- `meta.json`: `dataVersion = 2026-10-08`, `gameVersion = 1.4.5`.
- Arquivos complementares obtidos em 2026-11-01.
- Os três arquivos anteriores foram preservados byte a byte e conferidos por hash contra a fonte.
- [Contrato dos datasets](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/README.md).
- [Regras do pipeline](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/mapping.toml), consultadas para distinguir agrupamento, progressão e pré-requisitos.

| Arquivo | Uso |
|---|---|
| `items.json` (existente) | Identidade por `key`, categorias, obtenção, biomas/eventos agregados e progressão |
| `recipes.json` (existente) | Receitas, grupos alternativos, estações, condições ambientais e Shimmer |
| `milestones.json` (existente) | Marcos de disponibilidade estimada pelo tracker |
| `biomes.json` | Nomes e IDs dos biomas |
| `bosses.json` | Bosses e agrupamento de fontes de drop |
| `bestiary.json` | Criaturas, tipos, localização e IDs de NPC |
| `drops.json` | Fontes, linhas de drops, probabilidades, quantidades e grupos |
| `vendors.json` | Identificação dos vendedores |
| `shops.json` | Ofertas e condições por linha |
| `events.json` | Identificação dos eventos |
| `conditions.json` | Definições dos tokens de condição |
| `meta.json` | Versões declaradas pelo produtor da base |

Não foram baixados arquivos de imagens, textos de introdução, conjuntos de armaduras ou
Extractinator: não são necessários às relações analisadas. Não existe JSON específico de
geração geológica de minérios no inventário consultado.

## Relações e cobertura

`G_full` tem 13 tipos de vértices e 21 tipos de relação. Inclui ingredientes/receitas/produtos,
estações e suas alternativas, condições ambientais de crafting, Shimmer, encontro de criaturas
em biomas, eventos, drops de criaturas, conteúdo de sacolas/contêineres, vendedores,
contextos de venda/drop e disponibilidade por milestone. Cada aresta guarda proveniência;
linhas condicionais mantêm os dados originais. Boss → fonte é agrupamento, não drop direto.

**Biomas exigem interpretação:** `items.biomes` descreve obtenção por drops/vendas, não geração
de minérios. Ecto Mist/Graveyard e Snow Biome são condições explícitas de crafting;
a primeira equivalência é corroborada pela [Wiki](https://terraria.wiki.gg/wiki/Ecto).
Um minério participar de uma receita não torna seu bioma uma condição da receita.

| Dados | Integrados / originais |
|---|---:|
| Itens desktop | 6.184 / 6.186 |
| Receitas | 3.655 / 3.655 |
| Linhas Shimmer | 287 / 287 (402 arestas após expansão de grupos) |
| Linhas de drops | 3.677 / 3.680 |
| Linhas de lojas | 817 / 817 |
| Entradas do bestiário | 546 / 546 |
| Fontes de drops | 487 / 488 |

Três drops e uma fonte foram excluídos por plataforma; nenhum relacionamento foi completado
por hipótese. As 37 fontes desktop sem correspondência inequívoca no bestiário permanecem
como `drop_source`. Não são referências quebradas. `G_full` tem 85 componentes fracas,
9.134 fortes e 83 isolados; `G` tem 62 componentes fracas e nenhum isolado.

## Análises implementadas

- Estrutura, densidade, graus de entrada/saída, componentes, clustering e assortatividade.
- Distâncias por BFS amostrada e limites explícitos para o diâmetro da maior componente.
- Degree, betweenness amostrada, closeness e PageRank; rankings separados e três destaques por consenso de ranks.
- Comunidades Louvain, tamanhos, categorias, biomas informados e milestones.
- ER G(n,m), WS, BA e nulo com sequência de graus preservada: cinco realizações por modelo.
- Falhas aleatórias (dez repetições) e ataques estáticos por grau e betweenness.
- Eficiência, difusão por BFS, pontes, articulações, blocos biconexos e caminhos reais.
- Onze figuras, incluindo distribuições de grau, centralidades e clustering, comparações sintéticas e subgrafos legíveis.

Semente base 42; caminhos usam até 128 origens e betweenness até 256. PageRank tem α=0,85,
tolerância explícita e limite de iterações. O nulo realiza 5m trocas duplas aceitas, mantendo
o grau de cada vértice. WS usa k=4 e β=0,1; BA usa m=2. Diferenças de densidade impostas
pelos parâmetros inteiros são exibidas nas tabelas.

## Resultados e interpretação

Na projeção acadêmica, os destaques pelo consenso declarado são **Torch, Stone Block e Iron Bar**.
A maior componente reúne 3.599 itens (95,4%). Grau médio: 3,55; clustering: 0,0323;
assortatividade: −0,2228; distância média estimada na maior componente: 5,66 ± 0,14
(erro padrão por amostragem de origens). O diâmetro dessa componente está entre 21 e 24.

Com 10% dos itens removidos, a maior componente retém 80,8% do total original nas falhas
aleatórias, 2,0% no ataque por grau e 2,6% por betweenness. São resultados de conectividade,
não uma simulação completa de crafting. Existem 1.548 pontes e 446 articulações.

H apresenta hubs e caminhos curtos, com clustering maior que ER. Entretanto, esse clustering
é menor que o do nulo que preserva os graus: **não há classificação inequívoca como small-world**.
A heterogeneidade se aproxima qualitativamente de um aspecto de BA, mas **não foi comprovada
uma lei de potência**. As evidências e ressalvas estão nas respostas calculadas do notebook.

## Verificação e limites

`uv sync` e a execução integral de todas as células passaram. As verificações cobrem identidade,
referências, quantidades, registros de drops/lojas, cobertura e equivalência exata do crafting.
Os vértices, arestas e ocorrências de receitas foram comparados com a execução anterior.
Nenhum JSON original, documento da disciplina ou outro trabalho foi alterado.

Limitações principais: geração de minérios ausente; variantes sem correspondência segura;
progressão estimada pelo tracker; diferentes dificuldades/seeds coexistem na base; condições
textuais não formam um simulador lógico. A projeção H perde direção, condições e AND/OR.
Os métodos aproximados, amostras sintéticas e heurística de comunidades têm limites explícitos.
Não foram criados módulos `.py`, estrutura de framework, pastas de resultados ou testes externos.

## Integridade dos arquivos

Os SHA256 abaixo identificam os arquivos utilizados. Os links apontam para a revisão fixada.

| Arquivo | SHA256 |
|---|---|
| [items.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/items.json) | `ee7318eb8c82142d95b12871766fe8471e715eda0ab33eaf79512db1b96fc20a` |
| [recipes.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/recipes.json) | `3623d67cbf4ddf3aa5ca97c1c609a7114f56632d156354da3b968d746083ab47` |
| [milestones.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/milestones.json) | `495fb8c8722692782c0ffe765adc2fa702f0f09398fc8ba3afbdd7c75915c2d6` |
| [biomes.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/biomes.json) | `ac5677d59853bc8f3de60d7024d824018e583971fb567779045d3fed4c4a79c1` |
| [bosses.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/bosses.json) | `0209fd589d7df8190371d82c985a5a67c495d95f13aa90a7271ab60af2d4a0cf` |
| [bestiary.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/bestiary.json) | `299016cf1a66b7d1bb79f61f5c793368e5235d6fd6d24c89c1d9c6e0133668a5` |
| [drops.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/drops.json) | `ac1e46a564f2dc5b820738104734e7ab71e90572117f9b48f033f3a47244e2f6` |
| [vendors.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/vendors.json) | `a7658362f552e761043386ef659cc0d592804d72202aa3d7f18938d8700e8f79` |
| [shops.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/shops.json) | `917719526b8e3cf048eb5070949ca8f8500a7deaafccb368ba8fa4c62c633f65` |
| [events.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/events.json) | `a30b6171b75131341024839b7a84274d9a815044d69d46cc6cb63b9ba771e503` |
| [conditions.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/conditions.json) | `74fc79319f9a7e7559d8a4d58a6c142ba79e93ba68dd68580117b848a495465a` |
| [meta.json](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/meta.json) | `6a0564cc3b893dbda58b8d33f729c22a6e321b28a9d5174a681396706897653f` |
