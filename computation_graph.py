import keyword
from collections import defaultdict
from typing import Dict, List, Tuple

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    HAS_VIZ = True
except ImportError:
    HAS_VIZ = False

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(int)
        self.seq = []
        
    def extract(self, code: str) -> List[str]:
        res = []
        for line in code.split('\n'):
            if line.strip().startswith('#'):
                continue
            for word in line.split():
                w = word.strip('.,;:()[]{}"\'').lower()
                if keyword.iskeyword(w):
                    res.append(w)
        return res
    
    def _addEdges(self, seq: List[str]):
        for i in range(len(seq) - 1):
            self.edges[(seq[i], seq[i + 1])] += 1
    
    def build(self, code: str):
        self.seq = self.extract(code)
        if not self.seq:
            return
        self.nodes.update(self.seq)
        self._addEdges(self.seq)
    
    def buildFromFiles(self, paths: List[str]):
        for path in paths:
            with open(path, 'r', encoding='utf-8') as f:
                seq = self.extract(f.read())
            if not seq:
                continue
            self.seq.extend(seq)
            self.nodes.update(seq)
            self._addEdges(seq)
    
    def getWeights(self) -> Dict[Tuple[str, str], float]:
        out = defaultdict(int)
        for (u, v), cnt in self.edges.items():
            out[u] += cnt
        return {(u, v): cnt / out[u] if out[u] > 0 else 0.0 
                for (u, v), cnt in self.edges.items()}
    
    def getInfo(self) -> Dict:
        weights = self.getWeights()
        return {
            'nodes': list(self.nodes),
            'edges': [
                {
                    'from': u,
                    'to': v,
                    'count': self.edges[(u, v)],
                    'weight': weights[(u, v)]
                }
                for (u, v) in self.edges.keys()
            ]
        }
    
    def print(self):
        info = self.getInfo()
        print("nodes:", len(info['nodes']), "edges:", len(info['edges']))
        for e in sorted(info['edges'], key=lambda x: x['weight'], reverse=True):
            print(e['from'], "->", e['to'], ":", round(e['weight'], 3))
    