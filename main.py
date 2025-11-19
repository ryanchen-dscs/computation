from computation_graph import Graph
import os
import glob
import sys

def main():
    g = Graph()
    
    if len(sys.argv) > 1:
        dirpath = sys.argv[1]
        if os.path.isfile(dirpath):
            with open(dirpath, 'r') as f:
                g.build(f.read())
        else:
            g.buildFromFiles(glob.glob(os.path.join(dirpath, '**/*.py'), recursive=True))
    else:
        with open('example.py', 'r') as f:
            g.build(f.read())
    
    g.print()
    g.visualize()

if __name__ == "__main__":
    main()
