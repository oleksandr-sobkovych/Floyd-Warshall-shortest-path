"""Test the graph."""


from graph import LinkedGraph, LinkedDirectedGraph
import networkx as nx
import matplotlib.pyplot as plt
from random import randrange
from math import inf


def floyd(graph: LinkedGraph):
    all_verts = graph.size_vertices()
    conv_map = {}
    for label, vert in enumerate(graph.vertices()):
        conv_map[label] = vert
    print(conv_map)
    matrix = []
    for i in range(all_verts):
        matrix.append([])
        for ii in range(all_verts):
            edge = graph.get_edge(conv_map[i].get_label(),
                                  conv_map[ii].get_label())
            if i == ii:
                matrix[-1].append(0)
            elif edge is not None:
                matrix[-1].append(edge.get_weight())
            else:
                matrix[-1].append(inf)

    print()
    for i in range(all_verts):
        print(matrix[i])

    for k in range(all_verts):
        for i in range(all_verts):
            for ii in range(all_verts):
                new_sum = matrix[i][k] + matrix[k][ii]
                if matrix[i][ii] > new_sum:
                    matrix[i][ii] = new_sum

    print()
    for i in range(all_verts):
        print(matrix[i])


if __name__ == '__main__':
    g = LinkedGraph()
    dg = LinkedDirectedGraph()

    for i in range(10):
        g.add_vertex(i)
        dg.add_vertex(i)

    origins = tuple(randrange(0, 10) for _ in range(5))
    dests = tuple(randrange(0, 10) for _ in range(5))

    edges = tuple((i, j) for i, j in zip(origins, dests))
    # edges = ((1, 2), (2, 3), (3, 2), (3, 3), (4, 3), (1, 4))

    for i, j in edges:
        try:
            g.add_edge(i, j, i)
        except AttributeError:
            continue

    for i, j in edges:
        try:
            dg.add_edge(i, j, i)
        except AttributeError:
            continue

    print(g)
    print(dg)
    graph = nx.DiGraph()
    for node in dg.vertices():
        graph.add_node(node.get_label())
    for edge in dg.edges():
        vertices = edge.get_vertices()
        graph.add_edge(vertices[0].get_label(), vertices[1].get_label(),
                       weight=edge.get_weight())
    pos = nx.spring_layout(graph)
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in graph.edges(data=True)])
    nx.draw_networkx_edge_labels(graph, pos, edge_labels)
    nx.draw(graph, pos, with_labels=True)
    plt.show()

    floyd(dg)
