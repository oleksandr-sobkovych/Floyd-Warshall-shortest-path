"""
Source: https://github.com/anrom7/Graph_linked

Author: Andriy Romaniuk

Author's annotation: Completes the graph module for linked directed graphs
using an adjacency list, adding preconditions and raising exceptions where
relevant.

Note: Entirely modified to support various graphs and to suit PEP
recommendations
"""
from __future__ import annotations
from abstractcollection import AbstractCollection
from typing import Union, Any, Iterator, Optional, Collection


class LinkedEdge:
    """Represent an undirected edge.

    An edge has two vertices, a weight, and a mark attribute.
    """

    def __init__(self, one_vertex: LinkedVertex, other_vertex: LinkedVertex,
                 weight: Union[float, int] = None):
        """Create an edge.

        :param one_vertex: one of the vertices
        :param other_vertex: another vertex
        :param weight: the weight of the edge
        """
        self._vertex1 = one_vertex
        self._vertex2 = other_vertex
        self._weight = weight
        self._mark = False

    def clear_mark(self):
        """Clears the mark on the edge."""
        self._mark = False

    def __hash__(self):
        return (hash(self._vertex1) << int(self._weight)) ^ hash(self._vertex2)

    def __eq__(self, other: LinkedEdge) -> bool:
        """Return True if vertices of the edges match, False otherwise."""
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return ((self._vertex1 == other._vertex1 and
                 self._vertex2 == other._vertex2) or
                (self._vertex1 == other._vertex2 and
                 self._vertex2 == other._vertex1))

    def get_vertices(self) -> (LinkedVertex, LinkedVertex):
        """Return the tuple of vertices."""
        return self._vertex1, self._vertex2

    def get_other_vertex(self, this_vertex: LinkedVertex) -> LinkedVertex:
        """Return the vertex opposite this_vertex."""
        if this_vertex is None or this_vertex == self._vertex2:
            return self._vertex1
        else:
            return self._vertex2

    def get_weight(self) -> Union[int, float]:
        """Return the edge's weight."""
        return self._weight

    def is_marked(self) -> bool:
        """Returns True if the edge is marked, False otherwise."""
        return self._mark

    def set_mark(self):
        """Set the mark on the edge."""
        self._mark = True

    def set_weight(self, weight: Union[int, float]):
        """Set the weight on the edge to given weight."""
        self._weight = weight

    def __repr__(self) -> str:
        """Return the string representation of the edge."""
        return f"{self._vertex1} -- {self._vertex2} : {self._weight}"


class LinkedDirectedEdge(LinkedEdge):
    """Represent a directed edge.

    An edge has a source vertex, a destination vertex,
    a weight, and a mark attribute.
    """

    def __init__(self, from_vertex: LinkedVertex, to_vertex: LinkedVertex,
                 weight: Union[float, int] = None):
        """Create an edge.

        :param from_vertex: the source vertex
        :param to_vertex: the destination vertex
        :param weight: the weight of the edge
        """
        super().__init__(from_vertex, to_vertex, weight)

    def __eq__(self, other: LinkedDirectedEdge) -> bool:
        """Return True if vertices of the edges match, False otherwise."""
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return (self._vertex1 == other._vertex1 and
                self._vertex2 == other._vertex2)

    def get_to_vertex(self) -> LinkedVertex:
        """Return the edge's destination vertex."""
        return self._vertex2

    def __repr__(self) -> str:
        """Return the string representation of the edge."""
        return f"{self._vertex1} -> {self._vertex2} : {self._weight}"


class LinkedVertex:
    """Represent a vertex.

    A vertex has a label, a list of incident edges,
    and a mark attribute.
    """

    def __init__(self, label: Any):
        """Create a vertex.

        :param label: label of the vertex (can be its content)
        """
        self._label = label
        self._edge_list = list()
        # whether it is marked
        self._mark = False

    def __hash__(self):
        return (hash(self._label) << 5) ^ hash(self.__class__.__name__)

    def clear_mark(self):
        """Clear the mark on the vertex."""
        self._mark = False

    def get_label(self) -> Any:
        """Get the label of the vertex."""
        return self._label

    def is_marked(self) -> bool:
        """Return True if the vertex is marked or False otherwise."""
        return self._mark

    def set_label(self, label: Any, g: LinkedGraph):
        """Set the vertex's label to label."""
        g._vertices.pop(self._label, None)
        g._vertices[label] = self
        self._label = label

    def set_mark(self):
        """Set the mark on the vertex."""
        self._mark = True

    def __repr__(self) -> str:
        """Return the string representation of the vertex."""
        return f"v({self._label})"

    def __eq__(self, other: LinkedVertex) -> bool:
        """Return True if the labels are equal, False otherwise."""
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        return self.get_label() == other.get_label()

    # methods for interacting with edges

    def add_edge_to(self, to_vertex: LinkedVertex, weight: Union[int, float]):
        """Connect two vertices with an edge.

        :param to_vertex: vertex to connect to
        :param weight: weight of the edge
        """
        edge = LinkedEdge(self, to_vertex, weight)
        self._edge_list.append(edge)
        to_vertex._edge_list.append(edge)

    def get_edge_to(self, to_vertex: LinkedVertex) -> Optional[LinkedEdge]:
        """Return the connecting edge if it exists, None otherwise."""
        edge = LinkedEdge(self, to_vertex)
        try:
            # Python in operator uses == operator
            return self._edge_list[self._edge_list.index(edge)]
        except ValueError:
            return None

    def incident_edges(self) -> Iterator:
        """Generate the incident edges for this vertex."""
        return iter(self._edge_list)

    def neighboring_vertices(self) -> Iterator:
        """Generate the neighboring vertices for this vertex."""
        for edge in self._edge_list:
            yield edge.get_other_vertex(self)

    def remove_edge_to(self, to_vertex: LinkedVertex):
        """Return True if the edge exists and is removed, False otherwise."""
        edge = LinkedEdge(self, to_vertex)
        try:
            edge_i = self._edge_list.index(edge)
            self._edge_list[edge_i]._edge_list.remove(self)
            self._edge_list.pop(edge_i)
            return True
        except ValueError:
            return False


class LinkedDirectedVertex(LinkedVertex):
    """Represent a vertex in a directed graph.

    A vertex has a label, a list of incident edges,
    and a mark attribute.
    """
    def add_edge_to(self, to_vertex: LinkedVertex, weight: Union[int, float]):
        """Connect two vertices with an edge.

        :param to_vertex: vertex to connect to
        :param weight: weight of the edge
        """
        edge = LinkedDirectedEdge(self, to_vertex, weight)
        self._edge_list.append(edge)

    def get_edge_to(self, to_vertex: LinkedVertex) -> Optional[LinkedEdge]:
        """Return the connecting edge if it exists, None otherwise."""
        edge = LinkedDirectedEdge(self, to_vertex)
        try:
            # Python in operator uses == operator
            return self._edge_list[self._edge_list.index(edge)]
        except ValueError:
            return None

    def remove_edge_to(self, to_vertex: LinkedVertex):
        """Return True if the edge exists and is removed, False otherwise."""
        edge = LinkedDirectedEdge(self, to_vertex)
        try:
            self._edge_list.remove(edge)
            return True
        except ValueError:
            return False


class LinkedGraph(AbstractCollection):
    """Represent an undirected graph.

    A graph has a count of vertices, a count of edges,
    and a dictionary of label/vertex pairs.
    """

    def __init__(self, source_collection: Collection = None):
        self._edge_count = 0
        self._vertices = {}
        AbstractCollection.__init__(self, source_collection)

    def __len__(self) -> int:
        """Return number of the vertices."""
        return self._size

    # Methods for clearing, marks, sizes, string rep

    def clear(self):
        """Clear the graph (revert to initial state)."""
        self._size = 0
        self._edge_count = 0
        self._vertices = {}

    def clear_edge_marks(self):
        """Clear all the edge marks."""
        for edge in self.edges():
            edge.clear_mark()

    def clear_vertex_marks(self):
        """Clear all the vertex marks."""
        for vertex in self.vertices():
            vertex.clear_mark()

    def size_edges(self) -> int:
        """Return the number of edges."""
        return self._edge_count

    def size_vertices(self) -> int:
        """Return the number of vertices."""
        return len(self)

    def __str__(self) -> str:
        """Return the string representation of the graph."""
        return (f"    {self.__class__.__name__.replace('Linked', '')}:\n"
                f"{len(self)} Vertices: "
                f"{', '.join(str(v) for v in self._vertices)}\n"
                f"{self.size_edges()} Edges:\n"
                f"{chr(10).join(str(e) for e in self.edges())}")

    def add(self, label: Any):
        """For compatibility with other collections."""
        self.add_vertex(label)

    # Vertex related methods

    def add_vertex(self, label: Any):
        """Add a vertex to the graph.

        :param label: label of the added vertex
        :raise AttributeError: if a vertex with label
        is already in the graph."""
        if self.contains_vertex(label):
            raise AttributeError(f"Label {label} already in the graph.")
        self._vertices[label] = LinkedVertex(label)
        self._size += 1

    def contains_vertex(self, label: Any) -> bool:
        """Return True if vertex with the label is in the graph, else False."""
        return label in self._vertices

    def get_vertex(self, label: Any) -> LinkedVertex:
        """Get the vertex with label from the graph.

        :param label: label of the desired vertex
        :raise AttributeError: if a vertex with label is not already in the
        graph."""
        if not self.contains_vertex(label):
            raise AttributeError(f"Label {label} not in the graph.")
        return self._vertices[label]

    def remove_vertex(self, label: Any) -> bool:
        """Return True if the vertex was removed, False otherwise."""
        removed_vertex = self._vertices.pop(label, None)
        if removed_vertex is None:
            return False

        # Examine all other vertices to remove edges directed at the removed
        # vertex
        # In the undirected graph these edges are counted once this way
        for vertex in self.vertices():
            if vertex.remove_edge_to(removed_vertex):
                self._edge_count -= 1
        self._size -= 1
        return True

    # Methods related to edges

    def add_edge(self, from_label: Any, to_label: Any,
                 weight: Union[int, float]):
        """Connect the vertices with an edge with the given weight.

        :param from_label:
        :param to_label:
        :param weight:

        :raise AttributeError: if the vertices are not already in the graph
        or they are already connected.
        """
        from_vertex = self.get_vertex(from_label)
        to_vertex = self.get_vertex(to_label)
        if self.get_edge(from_label, to_label):
            raise AttributeError(f"An edge already connects "
                                 f"{from_label} and {to_label}")
        from_vertex.add_edge_to(to_vertex, weight)
        self._edge_count += 1

    def contains_edge(self, from_label: Any, to_label: Any) -> bool:
        """Return True if an edge connects the vertices, False otherwise."""
        return self.get_edge(from_label, to_label) is not None

    def get_edge(self, from_label: Any, to_label: Any) -> LinkedEdge:
        """Return the edge connecting the two vertices.

        Return None if no edge exists.
        :raise AttributeError: if the vertices are not already in the graph.
        """
        from_vertex = self.get_vertex(from_label)
        to_vertex = self.get_vertex(to_label)
        return from_vertex.get_edge_to(to_vertex)

    def remove_edge(self, from_label: Any, to_label: Any) -> bool:
        """Return True if the edge was removed, False otherwise.

        :raise AttributeError: if the vertices are not already in the graph.
        """
        from_vertex = self.get_vertex(from_label)
        to_vertex = self.get_vertex(to_label)
        edge_removed_flag = from_vertex.remove_edge_to(to_vertex)
        if edge_removed_flag:
            self._edge_count -= 1
        return edge_removed_flag

    # Iterators

    def __iter__(self) -> Iterator:
        """Iterate over a view of self (the vertices)."""
        return self.vertices()

    def edges(self) -> Iterator:
        """Iterate over the edges in the graph."""
        result = set()
        for vertex in self.vertices():
            result |= set(vertex.incident_edges())
        return iter(result)

    def vertices(self) -> Iterator:
        """Iterate over the vertices in the graph."""
        return iter(self._vertices.values())

    def incident_edges(self, label: Any) -> Iterator:
        """Iterate over the incident edges of the given vertex.

        :raise AttributeError: if a vertex with label is not already in the
        graph.
        """
        return self.get_vertex(label).incident_edges()

    def neighboring_vertices(self, label: Any) -> Iterator:
        """Iterate over the neighboring vertices of the given vertex.

        :raise AttributeError: if a vertex with label is not already in the
        graph.
        """
        return self.get_vertex(label).neighboring_vertices()


class LinkedDirectedGraph(LinkedGraph):
    """Represent an undirected graph.

    A graph has a count of vertices, a count of edges,
    and a dictionary of label/vertex pairs.
    """

    # Vertex related methods

    def add_vertex(self, label: Any):
        """Add a vertex to the graph.

        :param label: label of the added vertex
        :raise AttributeError: if a vertex with label
        is already in the graph."""
        if self.contains_vertex(label):
            raise AttributeError(f"Label {label} already in the graph.")
        self._vertices[label] = LinkedDirectedVertex(label)
        self._size += 1

    def remove_vertex(self, label: Any) -> bool:
        """Return True if the vertex was removed, False otherwise."""
        removed_vertex = self._vertices.pop(label, None)
        if removed_vertex is None:
            return False

        # Examine all other vertices to remove edges directed at the removed
        # vertex
        for vertex in self.vertices():
            if vertex.remove_edge_to(removed_vertex):
                self._edge_count -= 1

        # Examine all edges from the removed vertex to others
        for edge in removed_vertex.incident_edges():
            self._edge_count -= 1
        self._size -= 1
        return True

    # Iterators

    def edges(self):
        """Supports iteration over the edges in the graph."""
        for vertex in self.vertices():
            yield from vertex.incident_edges()

    def vertices(self):
        """Supports iteration over the vertices in the graph."""
        return iter(self._vertices.values())
