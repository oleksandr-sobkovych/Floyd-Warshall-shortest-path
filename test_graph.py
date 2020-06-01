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


def print_color(*args, fg=None, bg=None, sep=" ", end="\n"):
    """Print in color (fg - font, bg - background) in RGB."""
    color_map = f"\33["
    if fg:
        color_map += f"38;2;{fg[0]};{fg[1]};{fg[2]};"
    if bg:
        color_map += f"48;2;{bg[0]};{bg[1]};{bg[2]};"
    if not(bg or fg):
        color_map += "0;"
    color_map = color_map[:-1] + "m"
    print(f"{color_map}", end="")
    print(*args, sep=sep, end="")
    print('\33[0m', end=end)


def input_color(prompt, fg=None, bg=None):
    """Input in color RGB."""
    print_color(prompt, end="", fg=fg, bg=bg)
    return input()


def get_weight_matrix(choice='2'):
    while True:
        try:
            vert_n = int(input("Enter the number of vertexes (int only): "))
            break
        except ValueError:
            print("Number of vertexes must be int value, try again.")
    matrix = []
    for i in range(vert_n):
        matrix.append([])
        if choice == '1':
            while True:
                try:
                    row_value = input(f"Enter the weights of {i}th row"
                                      f" (using ' ' as a separator): ")
                    matrix[-1] = [int(value) for value in row_value.split()]
                    break
                except ValueError:
                    print("Check the correctness of input and try again")

        else:
            for j in range(vert_n):
                while True:
                    try:
                        ij_weight = input(f"Enter the weight of ({i}, {j})"
                                          f" element: ")
                        matrix[-1].append(float(ij_weight))
                        break
                    except ValueError:
                        print(
                            "A weight must be int value, try again.")
    return matrix


def initialize_graph(weight_matrix):
    g = LinkedGraph()
    dg = LinkedDirectedGraph()
    n = len(weight_matrix)

    for i in range(n):
        g.add_vertex(i)
        dg.add_vertex(i)

    for i in range(len(weight_matrix)):
        for j in range(len(weight_matrix)):
            if weight_matrix[i][j] > 0:
                try:
                    dg.add_edge(i, j, weight_matrix[i][j])
                    g.add_edge(i, j, weight_matrix[i][j])
                except AttributeError:
                    continue

    print(g)
    print(dg)
    return dg


def show_graph(dir_graph):
    dg = dir_graph
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


def run_test():
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
    # print_color()


def main():
    choice = input("If you want to initialize the graph, using weight matrix,"
                   " enter 1.\nIf you want to initialize by"
                   " typing each weight of edge, enter 2: ")
    matrix = get_weight_matrix(choice)
    dg = initialize_graph(matrix)
    show_graph(dg)
    floyd(dg)


if __name__ == '__main__':
    main()
