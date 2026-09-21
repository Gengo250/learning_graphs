# Casos de teste - Trabalho 2 (problema do caminhao)

## O que o problema pede

Para cada consulta `X Y`, a resposta e o **peso maximo de caminhao** que consegue ir da
ilha `X` ate a ilha `Y`. Um caminho so suporta o peso da sua ponte mais fraca, e o
caminhoneiro escolhe o melhor caminho. Logo:

```
resposta(X, Y) = max        ( min  peso(e) )
                caminhos P            e em P
```

Isso e o **caminho de gargalo maximo** (maximum bottleneck path / widest path).

As respostas abaixo foram calculadas por um solver independente (Dijkstra maximin, sem
arvore geradora) e conferidas contra a abordagem do notebook (`nx.maximum_spanning_tree`
+ `nx.shortest_path`). O teste 1 reproduz exatamente o gabarito oficial do enunciado,
o que valida o solver de referencia.

## Formato dos arquivos

Mesmo formato de `entrada.txt`:

```
I P S
A1 B1 P1
...
Ap Bp Pp
X1 Y1
...
Xs Ys
```

Arquivos com mais de um caso de teste seguidos sao permitidos (OBS5 do enunciado) e o
teste 3 exercita isso.

---

## teste_1_exemplo.txt - exemplo oficial do enunciado

Regressao basica: 4 ilhas, 5 pontes, 4 consultas. Cobre ponte de peso 0 e o caso em que
o caminho direto (4-3 = 4) perde para o desvio (4-2-3 = 7).

| Consulta | Resposta | Caminho otimo |
|---|---|---|
| 1 -> 4 | 7 | 1-2-4 (min 9, 7) |
| 2 -> 1 | 9 | 1-2 direto |
| 3 -> 1 | 8 | 3-2-1 (min 8, 9) |
| 4 -> 3 | 7 | 4-2-3 (min 7, 8) |

Saida esperada:

```
7
9
8
7
```

---

## teste_2_ponte_critica.txt - ponte de corte estrangulando o grafo

6 ilhas, 8 pontes, 5 consultas. Dois blocos fortes (1-2-3 e 4-5-6) ligados apenas pela
ponte 3-4 de peso 2 e pela ponte 2-5 de peso 1. Toda travessia entre blocos fica presa
no gargalo 2, mesmo com pontes de peso 9 e 10 dos dois lados.

| Consulta | Resposta | Por que |
|---|---|---|
| 1 -> 2 | 10 | direto, dentro do bloco |
| 1 -> 6 | 2 | obrigado a usar 3-4 (peso 2); via 2-5 daria 1 |
| 5 -> 6 | 9 | direto, dentro do bloco |
| 2 -> 4 | 2 | 2-3-4, gargalo na ponte 3-4 |
| 1 -> 5 | 2 | 1-3-4-5, gargalo na ponte 3-4 |

Saida esperada:

```
10
2
9
2
2
```

---

## teste_3_multiplos_casos.txt - tres casos no mesmo arquivo

Testa o laco de leitura (OBS5). Se o leitor parar no primeiro cabecalho, o teste falha.

### Caso 1 (3 ilhas, 3 pontes, 2 consultas) - triangulo

| Consulta | Resposta | Por que |
|---|---|---|
| 1 -> 3 | 4 | desvio 1-2-3 (min 5, 4) bate o direto 1-3 = 3 |
| 2 -> 1 | 5 | direto |

### Caso 2 (4 ilhas, 3 pontes, 2 consultas) - caminho simples, sem alternativa

| Consulta | Resposta | Por que |
|---|---|---|
| 1 -> 4 | 1 | caminho unico, gargalo na ponte 2-3 |
| 3 -> 4 | 9 | direto |

### Caso 3 (5 ilhas, 6 pontes, 3 consultas) - ponte de peso 0 e desvios

| Consulta | Resposta | Por que |
|---|---|---|
| 1 -> 2 | 3 | 1-3-4-2; a ponte direta 1-2 tem peso 0 (intransitavel) |
| 1 -> 5 | 3 | 1-3-4-2-5 bate 1-3-4-5 (que daria 2) |
| 4 -> 5 | 3 | 4-2-5 (min 3, 7) bate o direto 4-5 = 2 |

Saida esperada (na ordem, os 3 casos seguidos):

```
4
5
1
9
3
3
3
```

---

## teste_4_grafo_maior.txt - grafo maior com muitos desvios

10 ilhas, 16 pontes, 6 consultas. Nenhuma resposta e o caminho mais curto em numero de
pontes; todas exigem desvio. Pega implementacao que confunde o problema com caminho
minimo.

| Consulta | Resposta | Caminho otimo |
|---|---|---|
| 1 -> 10 | 6 | 1-2-4-6-7-8-9-10 (gargalo na ponte 9-10) |
| 2 -> 9 | 10 | 2-4-6-7-8-9 (gargalo na ponte 6-7) |
| 3 -> 8 | 9 | 3-2-4-6-7-8 (gargalo na ponte 2-3) |
| 1 -> 6 | 11 | 1-2-4-6 (gargalo na ponte 4-6) |
| 5 -> 10 | 6 | 5-6-7-8-9-10 (gargalo na ponte 9-10) |
| 4 -> 7 | 10 | 4-6-7 (gargalo na ponte 6-7) |

Saida esperada:

```
6
10
9
11
6
10
```
