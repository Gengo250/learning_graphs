# Terraria Network Analysis

Trabalho final de Teoria dos Grafos sobre fabricação, obtenção e progressão em Terraria. Toda a implementação, as figuras e as respostas ao [enunciado](docs/LEIA.md) estão em [notebooks/analysis.ipynb](notebooks/analysis.ipynb).

## Execução

Na pasta deste projeto, com Python 3.12 e `uv`:

```bash
uv sync
uv run jupyter notebook notebooks/analysis.ipynb
```

Execute todas as células em ordem. Os caminhos funcionam a partir da raiz do projeto ou de `notebooks/`. A análise não exige acesso à internet nem salva gráficos ou resultados em arquivos separados. Para execução integral sem interface:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/analysis.ipynb --ExecutePreprocessor.timeout=300
```

O kernel Jupyter precisa poder abrir sockets locais. As dependências existentes em `pyproject.toml` e `uv.lock` são suficientes.

## Modelo e análise

Duas representações, com papéis separados. Nenhuma medida estrutural do trabalho vem de `G`.

### `G` — grafo semântico

`MultiDiGraph` dirigido com itens, receitas, estações, bosses, marcos, biomas, fontes de drop, ofertas, condições, eventos e bestiário. Cada linha de drop ou oferta é uma rota separada; suas condições e texto pertencem à rota.

- Uma receita exige todos os slots; opções do mesmo slot e receitas distintas são alternativas. Quantidades e identificação dos slots ficam nos atributos. Um caminho isolado não demonstra que uma receita inteira pode ser concluída.
- Os vértices de receita e de rota são nomeados pelo conteúdo, não pelo índice da lista: `recipe:3234` aparece como `Onyx Blaster ⚒ Mythril Anvil`, e receitas alternativas do mesmo produto são numeradas (`Night's Edge ⚒ Demon Altar · alt. 1/2`). As funções `descrever` e `receitas_de`, no notebook, imprimem qualquer vértice sem abrir os JSONs.
- Os 32 bosses de `bosses.json` formam um tipo próprio, com a etapa no rótulo (`pré-Hardmode`, `Hardmode`, `evento`) e sempre a mesma cor. Sacolas de tesouro e contêineres são tipos distintos: `bag` tem 18 vértices e `container` 69, o que mantém visíveis fontes como baús do Dungeon.
- Marcos de `items.json` indicam disponibilidade estimada, não exigência universal. As regras suplementares representam Hardmode, chefes mecânicos e marcos sem criar uma sequência linear de todos os bosses.

### `H` — projeção acadêmica

Projeção simples e não dirigida apenas das relações de ingrediente e produto. Perde direção, quantidades, condições e lógica AND/OR, e não inclui marcos, bosses ou biomas. É a rede efetivamente analisada: distribuições, centralidades, componentes, comparação com ER/WS/BA e nulo de graus, robustez, difusão, preservação e navegação. A execução atual produz 3.773 vértices e 6.692 arestas, acima dos 300 exigidos pelo enunciado.

### Figuras de dependência

O diagrama de dependências usa camadas: o item-alvo no topo e cada nível abaixo a um passo dirigido de distância, de modo que minérios, fontes e bosses ficam na base.

- A figura **padrão é focada**: mostra a cadeia principal de fabricação até uma profundidade configurável e, para cada ingrediente que ela não fabrica, a fonte direta que o entrega. O vértice de rota é dispensado nesse modo, e a célula imprime quantas rotas alternativas ficaram fora do desenho. Para a Terra Blade isso reduz a figura de 105 para 59 vértices sem perder a cadeia nem os bosses.
- `mostrar_item(chave, detalhado=True)` desenha a cadeia inteira com os vértices de rota e suas taxas. O recorte vale só para a figura: `G` não muda.
- A paleta é fixa: item azul-claro, receita âmbar, **boss vermelho em hexágono**, inimigo salmão, contêiner cinza, bioma verde, evento azul-escuro, vendedor magenta, marco roxo em losango, rotas cinza-claro. As arestas diferenciam `produz` (laranja), `ingrediente` (cinza), obtenção (azul-escuro), boss que destrava uma fonte (vermelho tracejado) e marco (roxo tracejado).
- Um marco só aparece quando é a única explicação de um item, caso do Chlorophyte Ore, que não tem receita nem drop.

### Análises acadêmicas

O notebook segue a ordem do enunciado: dados, construção de `G`, progressão, exemplos de dependências, projeção `H`, distribuições de métricas, três vértices mais importantes, comparação com redes sintéticas, classificação da rede, robustez/difusão/preservação/navegação e conclusões.

- **Distribuições:** grau (log-log), intermediação amostrada em 256 origens e clustering local, cada uma com interpretação calculada a partir dos próprios números.
- **Redes sintéticas:** ER, WS, BA e um nulo que preserva a sequência de graus, três realizações cada, com `n` idêntico ao de `H`. ER e o nulo reproduzem `m` exatamente; WS e BA não conseguem porque seus parâmetros são inteiros por vértice, e a diferença é documentada em vez de corrigida à força. Distâncias são estimadas por BFS amostrada e comparadas ao valor exato de `H` como aferição.
- **Três vértices mais importantes:** consenso dos ranks de grau, intermediação e proximidade, com justificativa individual extraída dos dados — receitas que usam o item, estações, famílias de produtos vizinhos e efeito da remoção. A execução atual aponta Torch, Iron Bar e Lead Bar; o notebook mostra que Iron Bar e Lead Bar compartilham a maior parte da vizinhança por causa do grupo `Any Iron Bar` e, por isso, não são hubs independentes.
- **Classificação:** as hipóteses aleatória, livre de escala e small-world são avaliadas separadamente, cada uma contra o modelo de referência adequado, e o resultado distingue o que está sustentado do que não está demonstrado.
- **Robustez:** falha aleatória, ataque estático por grau inicial e ataque adaptativo por grau recalculado.

As conclusões numéricas são sempre calculadas no notebook; nenhum valor é fixado no texto. A relevância medida é topológica e não mede a necessidade de um item para concluir o jogo.

## Dados e limitações

Os JSONs originais vêm de [Terraria Progress Tracker](https://github.com/Doeschi/Terraria-Progress-Tracker), diretório `pipeline/data_readable`, commit `e1726af0908d928a3e2fa437286558827a6dd3b0`; `meta.json` declara Terraria 1.4.5 e data dos dados 2026-10-08. A fonte deriva da [Terraria Wiki](https://terraria.wiki.gg/) e informa licença CC BY-NC-SA 4.0. O [contrato dos dados](https://github.com/Doeschi/Terraria-Progress-Tracker/blob/e1726af0908d928a3e2fa437286558827a6dd3b0/pipeline/data_readable/README.md) descreve os campos.

A base não fornece um modelo geológico de mineração. A explicação textual de Chlorophyte é exibida sem inferir uma localização a partir de receitas. Textos e tokens de condições são preservados, mas não constituem um simulador lógico completo; variantes e rotas não documentadas podem faltar. Para a oferta de Leaf Wings, o texto original explicita a conjunção de Hardmode, noite, Jungle e Plantera. A associação de Mothron a Plantera deixou de ser estimativa: a [página da wiki](https://terraria.wiki.gg/wiki/Mothron) registra a nota de versão 1.4.1 do desktop segundo a qual Mothron só aparece depois de Plantera derrotada, o que vale para a versão 1.4.5 destes dados. Essa é a única aresta que a pesquisa acrescentou a `G` (`boss:plantera → enemy:mothron`), e é o que coloca Plantera junto do Mothron no diagrama em vez de ao lado da Terra Blade. As amostras de caminhos, centralidade e modelos sintéticos não provam lei de potência; o notebook afirma explicitamente que o comportamento livre de escala não está demonstrado e que o small-world não se sustenta no sentido estrito, já que o nulo de graus supera `H` em clustering e em distância. A preservação de informação é tratada como alcançabilidade e redundância estrutural, e essa limitação está declarada no próprio notebook.

## Pesquisa nas wikis

Os JSONs do tracker derivam da Terraria Wiki oficial, mas não explicam a progressão do jogo. As páginas abaixo foram consultadas em 2026-11-07 para entender essa progressão, nomear os vértices e conferir as receitas usadas como exemplo. Elas são a origem do resumo em etapas que está no notebook, na seção "Como o jogo progride, segundo as wikis".

Progressão e bosses:

- [Guide:Game progression](https://terraria.wiki.gg/wiki/Guide:Game_progression) — escada completa, de King Slime a Moon Lord.
- [Hardmode](https://terraria.wiki.gg/wiki/Hardmode) — o que a Wall of Flesh libera e a ordem Cobalt/Palladium → Mythril/Orichalcum → Adamantite/Titanium, cada minério exigindo a picareta do nível anterior.
- [Bosses](https://terraria.wiki.gg/wiki/Bosses) — quais bosses são opcionais e quais travam etapas.
- [Plantera](https://terraria.wiki.gg/wiki/Plantera) — acesso ao Jungle Temple e ao Golem.
- [Mothron](https://terraria.wiki.gg/wiki/Mothron) — "Can now only spawn after Plantera has been defeated", nota da versão 1.4.1 do desktop.
- [Chlorophyte Ore](https://terraria.wiki.gg/wiki/Chlorophyte_Ore) — exige Drax ou Pickaxe Axe, ferramentas que dependem dos três bosses mecânicos; é a razão de `milestoneVia` ser apenas texto no modelo.

Fabricação:

- [Crafting](https://terraria.wiki.gg/wiki/Crafting) — ingredientes, estações e proximidade exigida.
- [Crafting stations](https://terraria.wiki.gg/wiki/Crafting_stations) — estações por etapa e as condições ambientais que o tracker também trata como estação, como Water, Honey, Lava, Snow Biome, Ecto Mist e Graveyard.
- [Recipes](https://terraria.wiki.gg/wiki/Recipes) — organização por estação e receitas alternativas do mesmo item.
- [Alternative crafting ingredients](https://terraria.wiki.gg/wiki/Alternative_crafting_ingredients) — grupos como `Any Wood` e `Any Iron Bar`, que no modelo são as opções dentro de um slot.
- [Shimmer](https://terraria.wiki.gg/wiki/Shimmer) — transmutação por imersão, e não receita; por isso ocupa arestas próprias.

Itens usados nas figuras e nas validações:

- [Terra Blade](https://terraria.wiki.gg/wiki/Terra_Blade), [Excalibur](https://terraria.wiki.gg/wiki/Excalibur) — confirmam True Excalibur e True Night's Edge na Mythril/Orichalcum Anvil, como está em `recipes.json`.
- [Onyx Blaster](https://terraria.wiki.gg/wiki/Onyx_Blaster) — o vértice `recipe:3234`, usado como exemplo de rótulo legível.

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
