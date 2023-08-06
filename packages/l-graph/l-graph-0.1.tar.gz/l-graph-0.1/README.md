# lgraph
Python module for working with L-graphs.

## Installation
```sh
pip install lgraph
```

## Creating an L-graph
```python
lg = LGraph(3)

lg.add_edge(lg.initial_main.name, '0')
lg.add_edge('0', '1', label='b', round_trace=')', square_trace='[')
lg.add_edge('1', '2', label='c', square_trace=']')
lg.add_edge('2', lg.final_main.name)

lg.add_edge('0', '0', label='a', round_trace='(')
lg.add_edge('1', '1', label='b', round_trace=')', square_trace='[')
lg.add_edge('2', '2', label='c', square_trace=']')
```

## Saving and loading using files
```python
lg.save('graph_examples/a^n_b^n_c^n')
lg.load('graph_examples/a^n_b^n')
```