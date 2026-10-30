# Terraria Network Analysis

Ambiente para o estudo de redes do Terraria com Python 3.12 e Jupyter Notebook,
usando `uv` para gerenciar as dependências. Toda a implementação futura será feita
exclusivamente em `notebooks/analysis.ipynb`.

## Estrutura

```text
.
├── data/
│   ├── raw/                 # Dados originais (inicialmente vazio)
│   └── processed/           # Dados processados (inicialmente vazio)
├── notebooks/
│   └── analysis.ipynb       # Notebook de desenvolvimento
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

A pasta `docs/` contém os materiais preexistentes e foi preservada. O ambiente
`.venv/` é criado pelo `uv` e ignorado pelo Git. Esta etapa contém apenas a
configuração do ambiente, sem datasets ou análises.

## Instalação e uso

Com o `uv` instalado, execute no diretório raiz do projeto:

```bash
uv sync
uv run jupyter notebook notebooks/analysis.ipynb
```

O `uv sync` cria ou sincroniza a `.venv` com Python 3.12 usando o `uv.lock`.
As dependências incluem `networkx`, `pandas`, `numpy`, `matplotlib`, `scipy`,
`jupyter` e `ipykernel`. No Jupyter, use o kernel **Python 3 (ipykernel)**;
não é necessário ativar a `.venv` manualmente.
