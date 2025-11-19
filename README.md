# Computational Graph

This project creates a computation graph from Python programs. Take any Python code, find all the keywords in it, and turn those keywords into nodes in a graph. We then track how keywords move from one to another as the code runs and as they show up in order, which are the edges.

## Function

The extract function scans through Python code and identifies keywords like def, if, for, while, return, and class. Each unique keyword becomes a node, and when keyword A appears followed by keyword B in the code, that forms an edge from A to B. The build method monitors these movements and records them. The getWeights function figures out edge weights based on probability. To be specific, it is the chance that when you are at node A, you will move to node B. This is calculated by counting how many times A transitions to B compared to the total transitions from A.

## How the weights work

Count all movements from a keyword node, then for each specific movement, divide its count by the total outgoing movements from that node. This gives us the probability weight. 
Example: If "if" appears 10 times and 6 of those times it is followed by "return," then the edge from "if" to "return" has a weight of 0.6. The weights always add up to 1.0 for all edges leaving a node.

## Run the program

Run main.py, and it reads example.py. It parses the code, extracts keywords, builds the graph, and displays all the nodes and edges with their respective weights.

To process a specific file or directory, we can pass it as an argument:

```bash
python main.py path/to/file.py
python main.py path/to/directory
```

We can use the Graph class directly:

```
from computation_graph import Graph

g = Graph()
g.build(your_python_code_string)
g.print()
```

To process multiple files from a directory, we can also use buildFromFiles:

```
from computation_graph import Graph
import glob

g = Graph()
files = glob.glob('path/to/python/files/**/*.py', recursive=True)
g.buildFromFiles(files)
g.print()
```

## Structure

- computation_graph.py: Contains the Graph class with methods for extracting keywords, building the graph, and calculating weights
- example.py: Sample Python code to analyze
- main.py: Example script that processes a single file, directory, or example.py by default
- test_computation_graph.py: Unit tests for the Graph class

## Notes

Graph visualization inspiration: https://medium.com/@weidagang/how-computational-graphs-are-built-in-python-6caa868e87cf