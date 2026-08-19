from typing import Hashable, Iterable, Iterator, Sequence

Vertex = Hashable
Weight = float

class Graph:

    __slots__ = (_verts) 
    # The _verts dict keeps the edges data by referencing the neighbour to each vert.
    # This decision has been made in order to keep the data tied with one truth.
    # A member v of _vert is a vertex (which is any hashable object)
    # A member t of _vert[s] is an edge s -> t
    # The weight of an edge s -> t is given by _vert[s][t]

    def __init__(self, vertices : Iterable[Vertex] = (), edges : Iterable[Sequence] = ()) -> None:
        _verts : dict[Vertex, dict[Vertex, Weight]] = {} #Initialise _verts
        self.add_vertices(vertices)
        self.add_edges(edges)

    def vertices(self) -> tuple[Vertex, ...]:
        """Returns the tuple of vertices."""
        return tuple(self._verts)
    
    def order(self) -> int:
        """Returns the number of vertices."""
        return len(self._verts)
    
    def size(self) -> int:
        """Returns the number of edges"""
        pass
        # Need to create a edges method which returns an interator of the edges
        # return sum(1 for e in self.edges())
    
    def __iter__(self) -> Iterator[Vertex]:
        return iter(self._verts)
    
    def __contains__(self) -> bool:
        return v in self._verts
    
    def __repr__(self) -> str:
        return "Graph"

    def add_vertex(self, vert : Vertex) -> None:
        if vert not in self._verts:
            self._verts[vert] = {} #add a vertex with no neighbours
    
    def add_vertices(self, verts : Iterable[Vertex]) -> None:
        for vert in verts:
            self.add_vertex(vert)
    
    def add_edge(self, v1 : Vertex, v2 : Vertex, weight : Weight = 1.0) -> None:
        self.add_vertex(v1)
        self.add_vertex(v2)
        self._verts[v1][v2] = weight
        self._verts[v2][v1] = weight
    
    def add_edges(self, edges : Iterable[Sequence]) -> None:
        for e in edges:
            if len(e) == 2:
                self.add_edge(e[0], e[1])
            elif len(e) == 3:
                self.add_edge(e[0], e[1], e[2])
            else:
                raise ValueError(f"Edge has {len(e)} coordinates, should take form (v1, v2) or (v1, v2, w).")
    
    def remove_edge(self, v1 : Vertex, v2 : Vertex) -> None:
        if not self.has_edge(v1, v2):
            raise KeyError("No edge (v1, v2)")
        del self._verts[v1][v2]
        if v1 != v2:
            del self._verts[v2][v1]
    
    def has_edge(self, v1 : Vertex, v2 : Vertex) -> bool:
        return v1 in self._verts and v2 in self._verts[v1]
    
    def has_vertex(self, vert : Vertex) -> bool:
        return vert in self._verts
    
    def get_weight(self, v1 : Vertex, v2 : Vertex) -> Weight:
        """Returns the weight of edge v1 -> v2 if it exists.
        
        :param Vertex v1: The first vertex.
        :param Vertex v2: The second vertex.
        :return: The weight.
        :rtype: Weight
        :raises KeyError: if no edge v1 -> v2 exists.
        """
        if self.has_edge(v1, v2):
            return self._verts[v1][v2]
        else:
            raise KeyError(f"No edge {v1} -> {v2} exists.")
    
    def remove_vertex(self, vert : Vertex) -> None:
        if not has_vertex(self, vert):
            raise KeyError(f"No vertex {vert}.")
        ## remove vertex -vert- after removing all edges depending on it