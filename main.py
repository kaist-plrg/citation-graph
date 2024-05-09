from collections import defaultdict, Counter

import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import write_dot

from util.graph import CitationGraph

if __name__ == "__main__":
    graph = CitationGraph.from_json_file("quantum_test.json")

    counter = Counter([child for _, child in graph.edges])

    print(*counter.most_common(10), sep="\n")

    edges_filtered = [
        (parent, child) for parent, child in graph.edges if counter[child] > 2
    ]

    nodes_filtered = list(set([node for edge in edges_filtered for node in edge]))
    node_to_index = {node: i for i, node in enumerate(nodes_filtered)}

    nxgraph = nx.DiGraph()
    nxgraph.add_nodes_from([(i, {"title": i}) for i, node in enumerate(nodes_filtered)])

    citations = [
        (node_to_index[parent], node_to_index[child])
        for parent, child in edges_filtered
    ]

    nxgraph.add_edges_from(citations)

    write_dot(nxgraph, "quantum_test.dot")

    with open("quantum_test.txt", "w") as f:
        f.writelines([f"{i:3} {node}\n" for i, node in enumerate(nodes_filtered)])

    # # Position nodes using the spring layout
    # pos = nx.kamada_kawai_layout(nxgraph)
    # # pos = nx.circular_layout(nxgraph)
    # # pos = nx.spring_layout(nxgraph)

    # # Draw nodes
    # nx.draw(
    #     nxgraph,
    #     pos,
    #     with_labels=False,
    #     node_color="skyblue",
    #     node_size=100,
    #     edge_color="k",
    #     linewidths=1,
    #     font_size=2,
    # )

    # # Draw node labels
    # labels = nx.get_node_attributes(nxgraph, "title")
    # nx.draw_networkx_labels(nxgraph, pos, labels, font_size=8)

    # # Draw edges with arrows
    # nx.draw_networkx_edges(
    #     nxgraph, pos, edgelist=citations, arrowstyle="->", arrowsize=5
    # )

    # # Show the nxgraph
    # plt.show()
