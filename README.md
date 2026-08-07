# Graph Studies with NetworkX

This repository contains study notes and practical exercises focused on graph
theory using Python and the [NetworkX](https://networkx.org/) library. It is a
learning space for experimenting with graph creation, manipulation, analysis,
and visualization.

## Topics Practiced

- Creating graphs, nodes, and edges
- Inspecting graph structure and adjacency relationships
- Calculating node degrees
- Modeling social connections and routes between cities
- Visualizing graphs with NetworkX and Matplotlib

## Project Structure

```text
src/grafos_network/
|-- create_graph.py     # Creates and displays the Petersen graph
|-- graph_friends.py    # Models friendships as a graph
`-- graph_maps_city.py  # Models cities and roads as a graph
```

## Requirements

- Python 3.12 or later
- NetworkX
- Matplotlib

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
uv sync
```

## Running the Examples

Run any exercise from the project root. For example:

```bash
uv run python src/grafos_network/create_graph.py
uv run python src/grafos_network/graph_friends.py
uv run python src/grafos_network/graph_maps_city.py
```

Each script explores a different graph concept and may open a Matplotlib window
to display the resulting graph.

## Purpose

The repository is intended exclusively for learning, experimentation, and
practice with graph concepts and the NetworkX ecosystem.
