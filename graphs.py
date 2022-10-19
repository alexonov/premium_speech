import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn


def traverse(graph, start, node):
    graph.depth[node.name()] = node.shortest_path_distance(start)
    for child in node.hyponyms():
        graph.add_edge(node.name(), child.name())  # [_add-edge]
        traverse(graph, start, child)  # [_recursive-traversal]


def hyponym_graph(start):
    G = nx.Graph()  # [_define-graph]
    G.depth = {}
    traverse(G, start, start)
    return G


def graph_draw(graph):
    nx.draw_shell(graph,
                  node_size=[16 * graph.degree(n) for n in graph],
                  node_color=[graph.depth[n] for n in graph],
                  with_labels=False
    )
    plt.show()


if __name__ == '__main__':
    dog = wn.synset('tree.n.01')
    graph = hyponym_graph(dog)
    graph_draw(graph)

