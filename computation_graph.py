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
    
    def visualize(self, filename='graph.png'):
        if not HAS_VIZ:
            print("networkx and matplotlib required")
            return
        
        G = nx.DiGraph()
        weights = self.getWeights()
        
        for (u, v), w in weights.items():
            G.add_edge(u, v, weight=w)
        
        pos = nx.spring_layout(G, k=25, iterations=1000, seed=42)
        
        if 'continue' in pos and 'else' in pos and 'return' in pos:
            else_x, else_y = pos['else']
            return_x, return_y = pos['return']
            continue_x = (else_x + return_x) / 2
            continue_y = (else_y + return_y) / 2
            pos['continue'] = (continue_x, continue_y)
        
        plt.figure(figsize=(24, 20))
        
        weights_list = [G[u][v]['weight'] for u, v in G.edges()]
        
        node_size = 2500
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=node_size, alpha=0.9, node_shape='o')
        nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')
        
        nx.draw_networkx_edges(G, pos, width=[w*4 + 1 for w in weights_list],
                              alpha=0.7, edge_color='gray', arrows=True, 
                              arrowsize=25, arrowstyle='->', 
                              connectionstyle='arc3,rad=0', node_size=node_size)
        
        edge_labels = {(u, v): str(round(w, 2)) for (u, v), w in weights.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=16, 
                                    bbox=dict(boxstyle='round,pad=0.3', 
                                             facecolor='white', alpha=0.8))
        
        plt.title("Python Keyword Transition Computational Graph", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
