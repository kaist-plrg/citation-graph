from os import path
import argparse

from util.graph import CitationGraph

parser = argparse.ArgumentParser()

parser.add_argument(
    "seed_url_file", type=str, help="file containing acm digital library seed urls"
)
parser.add_argument(
    "--depth",
    type=int,
    default=2,
    help="maximum depth of the graph. default is 2",
)
parser.add_argument(
    "--min-impact",
    type=int,
    default=3,
    help="minimum impact to be included in the final graph. default is 3",
)

if __name__ == "__main__":
    args = parser.parse_args()
    graph_title = args.seed_url_file.split(".")[0]
    min_impact = args.min_impact
    graph_k = args.depth
    if graph_k < 1:
        print("Depth must be greater than 0")
        exit(1)

    if min_impact < 1:
        print("Minimum impact must be greater than 0")
        exit(1)

    with open(args.seed_url_file, "r") as f:
        seed_url_list = [url.strip() for url in f.readlines()]

    if not path.exists(graph_title + ".json"):
        if not path.exists(args.seed_url_file):
            print("Seed file not found")
            exit(1)

        graph = CitationGraph(graph_title, seed_url_list, graph_k)
        graph.init_seed()
    else:
        print("Loading existing json file")
        graph = CitationGraph.from_json_file(graph_title + ".json")

    while True:
        if graph.step():
            print(f"Nodes: {len(graph.nodes)}, Pending: {len(graph.pending_node_list)}")
            graph.dump_json_file()
        else:
            break

    graph.export_dot_file(min_impact)

    print("Done")
