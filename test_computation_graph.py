from computation_graph import Graph

def test_extract():
    g = Graph()
    code = "def test(): if x: return 1"
    res = g.extract(code)
    assert 'def' in res
    assert 'if' in res
    assert 'return' in res
    print("test_extract: PASS")

def test_build():
    g = Graph()
    code = "def test(): return 1"
    g.build(code)
    assert len(g.nodes) > 0
    assert len(g.edges) > 0
    assert 'def' in g.nodes
    assert 'return' in g.nodes
    print("test_build: PASS")

def test_weights():
    g = Graph()
    code = "def a(): return 1\ndef b(): return 2"
    g.build(code)
    weights = g.getWeights()
    assert len(weights) > 0
    for (u, v), w in weights.items():
        assert 0.0 <= w <= 1.0
    print("test_weights: PASS")

def test_buildFromFiles():
    g = Graph()
    g.buildFromFiles(['example.py'])
    assert len(g.nodes) > 0
    assert len(g.edges) > 0
    print("test_buildFromFiles: PASS")

def test_getInfo():
    g = Graph()
    code = "def test(): return 1"
    g.build(code)
    info = g.getInfo()
    assert 'nodes' in info
    assert 'edges' in info
    assert len(info['nodes']) > 0
    print("test_getInfo: PASS")

if __name__ == "__main__":
    test_extract()
    test_build()
    test_weights()
    test_buildFromFiles()
    test_getInfo()
    print("all tests passed")

