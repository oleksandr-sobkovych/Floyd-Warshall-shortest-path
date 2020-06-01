"""Analyze the graph."""
from graph import LinkedGraph, LinkedDirectedGraph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random as rd
from math import inf
from typing import Any


# colors used
UI_COL = (120, 255, 200)
BAD_COL = (255, 100, 100)
GOOD_COL = (50, 150, 255)
NEUT_COL = (255, 230, 55)

# space to give for each node text representation
NODE_SPACE = 10

# always round to 2 positions for visual display
DISPLAY_ROUND = 2

# pool for weight generation
MAX_WEIGHT = 10
MIN_WEIGHT = 0
ROUND_POS = NODE_SPACE - 4

# user choices for generation
USER_MATRIX = 1
USER_EDGES = 2
USER_RANDOM = 3


def print_matrix(matrix: np.array, label_map: dict):
    """Print out the matrix.

    :param matrix: 2D weight matrix from the graph
    :param label_map: map of how row numbers relate to node objects
    """
    dimension = len(matrix)
    color_print("Hint:", fg=UI_COL)
    color_print("- color of destination nodes in directed graph", fg=NEUT_COL)
    color_print("- color of source nodes in directed graph", fg=BAD_COL,
                end="\n\n")

    # print first row
    print(" "*NODE_SPACE, end="")
    for i in range(dimension):
        color_print(f"{label_map[i]}".ljust(NODE_SPACE, " "), end="",
                    fg=NEUT_COL)
    print()

    # print the actual matrix
    for i in range(dimension):
        color_print(f"{label_map[i]}".ljust(NODE_SPACE, " "), end="",
                    fg=BAD_COL)
        for ii in range(dimension):
            color_print(f"{matrix[i, ii]}".ljust(NODE_SPACE, " "), fg=GOOD_COL,
                        end="")
        print()
    print()


def floyd(graph: LinkedGraph) -> np.array:
    """Find all shortest path weights in the graph and return them in the form
    of a matrix.

    :param graph: the graph to run Floyd algorithm on
    """
    vert_n = graph.size_vertices()
    label_map = {}

    # assign each matrix row a unique vertex object
    for label, vert in enumerate(graph.vertices()):
        label_map[label] = vert

    # create and fill the matrix according to Floyd
    matrix = np.empty((vert_n, vert_n), dtype=np.float)
    for i in range(vert_n):
        for ii in range(vert_n):
            edge = graph.get_edge(label_map[i].get_label(),
                                  label_map[ii].get_label())
            if i == ii:
                matrix[i, ii] = 0
            elif edge is not None:
                matrix[i, ii] = edge.get_weight()
            else:
                matrix[i, ii] = inf

    color_print(f"Initial matrix:", fg=BAD_COL)
    print_matrix(matrix, label_map)

    # run the Floyd-Warshall algorithm
    for k in range(vert_n):
        for i in range(vert_n):
            for ii in range(vert_n):
                new_sum = round(matrix[i, k] + matrix[k, ii], ROUND_POS)
                if matrix[i, ii] > new_sum:
                    matrix[i, ii] = new_sum

    color_print(f"Resulting matrix of distance weights:", fg=GOOD_COL)
    print_matrix(matrix, label_map)
    return matrix


def color_print(*args: Any, fg: (int, int, int) = None,
                bg: (int, int, int) = None, sep: Any = " ",
                end: Any = "\n"):
    """Print in color.

    :param args: any args to print (as in normal print)
    :param fg: foreground color (a tuple of three ints in RGB format)
    :param bg: background color (a tuple of three ints in RGB format)
    :param sep: separator as in normal print
    :param end: end as in normal print (is not in color)
    """
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


def color_input(prompt: Any, fg: (int, int, int) = None,
                bg: (int, int, int) = None):
    """Input in color RGB.

    :param prompt: prompt as in normal input
    :param fg: foreground color (a tuple of three ints in RGB format)
    :param bg: background color (a tuple of three ints in RGB format)
    :return: decorated input function
    """
    color_print(prompt, end="", fg=fg, bg=bg)
    return input()


def get_weight_matrix(choice: int) -> (np.array, dict, bool):
    """Get weight matrix from the user's input.

    :param choice: user's choice for generation
    :return: a tuple of the 2D weight matrix, map of rows to labels, whether
    the graph is directed
    """
    # get the number of vertices
    while True:
        try:
            vert_n = int(color_input("Enter the number of vertices "
                                     "(int only): ", fg=UI_COL))
            break
        except ValueError:
            color_print("Number of vertices must be int value, try again.",
                        fg=BAD_COL)
    matrix = np.empty((vert_n, vert_n), dtype=np.float)
    label_map = {}

    color_print("\nNote: any connections of vertex to self will be ignored.",
                fg=NEUT_COL)
    color_print("Hint: enter float values. inf represents no connection.\n"
                f"Values will be rounded to {ROUND_POS} positions.",
                fg=GOOD_COL)

    # get connectivity
    if choice == USER_RANDOM:
        while True:
            try:
                connectivity = int(color_input(
                    "Enter connectivity (probability of an edge connecting "
                    "two vertices) of the graph (int between 0 and 100): ",
                    fg=UI_COL
                ))
                assert 0 <= connectivity <= 100
            except (AssertionError, ValueError):
                color_print("Bad connectivity value, try again!", fg=BAD_COL)
            else:
                color_print(f"Connectivity is: {connectivity}%", fg=GOOD_COL,
                            end="\n\n")
                break

    # for every row of the future matrix
    for i in range(vert_n):
        # get the label string for the node
        while True:
            try:
                label = color_input(f"\nEnter label for vertex {i} "
                                    f"(any string with "
                                    f"(0 < length < {NODE_SPACE-3})): ",
                                    fg=UI_COL)
                assert 0 < len(label) < NODE_SPACE-3
            except AssertionError:
                color_print("Bad label length, try again!", fg=BAD_COL)
            else:
                print()
                label_map[i] = label
                break

        # get the matrix row
        if choice == USER_MATRIX:
            while True:
                try:
                    row_value = color_input(
                        f"Enter the {vert_n} weights of row {i}"
                        f"(using ' ' as separator): ", fg=UI_COL)
                    row_value = map(float, row_value.split())
                    matrix[i] = [round(value, ROUND_POS) if value != inf
                                 else inf
                                 for value in row_value]
                except ValueError:
                    color_print("Incorrect input, try again!", fg=BAD_COL)
                else:
                    break

        # get the weights for every edge
        elif choice == USER_EDGES:
            for j in range(vert_n):
                # skip current node
                if j == i:
                    continue
                while True:
                    try:
                        ij_weight = color_input(f"Enter the weight for "
                                                f"({i}, {j}) edge: ",
                                                fg=UI_COL)
                        ij_weight = float(ij_weight)
                        ij_weight = (round(ij_weight, ROUND_POS)
                                     if ij_weight != inf else inf)
                        matrix[i, j] = ij_weight
                    except ValueError:
                        color_print("A weight must be float value, try again.",
                                    fg=BAD_COL)
                    else:
                        break

        # randomly generate the row according to connectivity and weight range
        else:
            for j in range(vert_n):
                if rd.randint(0, 99) < connectivity:
                    # get a random float between MIN_WEIGHT and MAX_WEIGHT
                    val = rd.random() * rd.randint(MIN_WEIGHT, MAX_WEIGHT-1)
                    val = round(val, ROUND_POS)
                    matrix[i, j] = val
                else:
                    matrix[i, j] = inf

    # clear all connections between a node and itself
    for i in range(vert_n):
        matrix[i, i] = inf

    # if matrix is symmetrical the graph is undirected, else directed
    for i in range(vert_n):
        for ii in range(vert_n):
            if matrix[i, ii] != matrix[ii, i]:
                return matrix, label_map, True
    return matrix, label_map, False


def initialize_graph(weight_matrix: np.array, label_map: dict,
                     directed: bool):
    """Create a graph out of weight matrix.

    :param weight_matrix: 2D matrix of weights
    :param label_map: how each row of the matrix relates to node label
    :param directed: whether the graph is directed
    :return: the generated graph
    """
    if directed:
        graph = LinkedDirectedGraph()
    else:
        graph = LinkedGraph()
    vert_n = len(weight_matrix)

    # add all vertices
    for i in range(vert_n):
        graph.add_vertex(label_map[i])

    if directed:
        # add necessary edges
        for i in range(vert_n):
            for ii in range(vert_n):
                if weight_matrix[i, ii] != inf:
                    try:
                        graph.add_edge(label_map[i], label_map[ii],
                                       weight_matrix[i, ii])
                    except AttributeError:
                        continue
    else:
        # add necessary edges with regard to symmetrical nature of the matrix
        for i in range(vert_n):
            for ii in range(i):
                if weight_matrix[i, ii] != inf:
                    try:
                        graph.add_edge(label_map[i], label_map[ii],
                                       weight_matrix[i, ii])
                    except AttributeError:
                        continue

    print(graph)
    return graph


def show_graph(graph: LinkedGraph, directed: bool):
    """Display the graph with matplotlib.pyplot.

    :param graph: graph to display
    :param directed: whether the graph is directed
    """
    if directed:
        display_graph = nx.DiGraph()
    else:
        display_graph = nx.Graph()

    # add all nodes for display
    for node in graph.vertices():
        display_graph.add_node(node.get_label())

    # add all edges for display
    for edge in graph.edges():
        vertices = tuple(map(lambda v: v.get_label(), edge.get_vertices()))
        display_graph.add_edge(*vertices, weight=edge.get_weight())

    pos = nx.spring_layout(display_graph)
    edge_labels = {}

    if directed:
        # add edge labels, add two weights if connection goes both ways
        for u, v, d in display_graph.edges(data=True):
            edge_labels[(u, v)] = f"{round(d['weight'], DISPLAY_ROUND)}"
            if (v, u) in edge_labels:
                edge_labels[(u, v)] += f",{edge_labels.pop((v, u))}"
    else:
        # add edge labels
        edge_labels = {(u, v): round(d['weight'], DISPLAY_ROUND)
                       for u, v, d in display_graph.edges(data=True)}

    # draw and display the graph
    nx.draw_networkx_edge_labels(display_graph, pos, edge_labels)
    nx.draw(display_graph, pos, with_labels=True)
    plt.show()


def main():
    """Get the input, display the graph and analyze it."""
    # get the graph generation method
    while True:
        try:
            choice = color_input("To initialize the graph using weight matrix "
                                 "enter: 1\nTo initialize by weight of each "
                                 "edge enter: 2\nTo initialize connections "
                                 "randomly enter: 3\n",
                                 fg=UI_COL)
            choice = int(choice)
            assert choice in (USER_MATRIX, USER_EDGES, USER_RANDOM)
        except (ValueError, AssertionError):
            color_print("Invalid input. Try again!", fg=BAD_COL)
        else:
            color_print("Processing...", fg=GOOD_COL)
            break

    # generate the graph (added for scalability, uses LinkedGraph ADT)
    weight_matrix, label_map, directed = get_weight_matrix(choice)
    final_graph = initialize_graph(weight_matrix, label_map, directed)

    # display the graph or skip
    if color_input("Display the graph? (y/n)\n", fg=UI_COL) == "y":
        color_print("Displaying...", fg=GOOD_COL, end="\n\n")
        show_graph(final_graph, directed)

    # run the floyd algorithm for the graph
    color_print("Path finding...", fg=GOOD_COL, end="\n\n")
    floyd(final_graph)


if __name__ == '__main__':
    main()
