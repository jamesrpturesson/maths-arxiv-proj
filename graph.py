from typing import Hashable, Iterable, Sequence

Vertex = Hashable
Weight = float

class Graph:
    def __init__(self, vertices : Iterable[Vertex] = (), edges : Iterable[Sequence] = ()):
        _verts : dict[Vertex, dict[Vertex, Weight]] = {}
        
