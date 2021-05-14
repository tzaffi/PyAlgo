# PyAlgo
Some Data Structures and Algorithms in Python

## Disjoint Sets aka Union/Find
[code](https://github.com/tzaffi/PyAlgo/blob/main/data_structures/union_find.py)

## Balanced Tree Data Structure (someone else's)
After several tries, I finally found a [good 'nuff explanation](https://bradfieldcs.com/algos/trees/avl-trees/). I was inspired by their code (but mostly wrote my own interpretation).

## My Own AVL Tree with a SortedList Implementation to Boot
[code](https://github.com/tzaffi/PyAlgo/blob/main/data_structures/zree.py)

#### TODO: add a SortedDict Implementation

## DAG Based String Processing Data Structures
### Trie (Including Radix Sort)
[code](https://github.com/tzaffi/PyAlgo/blob/main/data_structures/zrie.py#L56)

### Deterministic Finite Automaton (Including DFA Minimization Algo and an Unbounded Iterator!!!)
[code](https://github.com/tzaffi/PyAlgo/blob/main/data_structures/zrie.py#L118)


### Decision Grid
[code](https://github.com/tzaffi/PyAlgo/blob/main/data_structures/decision_grid.py)

Build a very small 2-monotonic-variable decider. EG:
```python
>>> from data_structures.decision_grid import DecisionGrid
>>> 
>>> dg_def = {
...     2: 20,   # x < 2      ==> 20 <= y
...     6: 10,   # 2 <= x < 6 ==> 10 <= y
...     8:  5,   # 6 <= x < 8 ==>  5 <= y
...              # 8 <= x     ==> APPROVE
... }
>>> print(DecisionGrid(dg_def))
y
20|********
10|XX******
 5|XXXX****
 0|XXXXXX**
--+0 2 6 8 x
```
