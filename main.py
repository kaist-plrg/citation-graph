from os import path, makedirs
import argparse

from util.graph import CitationGraph

parser = argparse.ArgumentParser()

parser.add_argument("seed_id_file", type=str, help="file containing seed paper ids")
parser.add_argument(
    "--depth",
    type=int,
    default=2,
    help="maximum depth of the graph. default is 2",
)
parser.add_argument(
    "--keywords",
    type=str,
    default="",
    help="Searchs papers whose title or abstract contains the keyword. Separated by comma. default is empty",
)
parser.add_argument(
    "--min-impact",
    type=int,
    default=3,
    help="minimum impact to be included in the final graph. default is 3",
)
parser.add_argument(
    "--filter-by-title", action="store_true", help="filter papers only by title"
)

parser.add_argument(
    "--search-direction",
    type=str,
    default="past",
    help="search direction of the graph. default is past. options: past(to the past), future(to the future)",
)

if __name__ == "__main__":
    args = parser.parse_args()
    graph_title = args.seed_id_file.split(".")[0]
    min_impact = args.min_impact
    graph_k = args.depth
    filter_by_title = args.filter_by_title
    search_direction = args.search_direction
    keywords = [
        [keyword.strip() for keyword in keyword_clause.split(",") if keyword.strip()]
        for keyword_clause in args.keywords.split("..")
        if keyword_clause.strip()
    ]
    if graph_k < 1:
        print("Depth must be greater than 0")
        exit(1)

    if min_impact < 1:
        print("Minimum impact must be greater than 0")
        exit(1)

    if search_direction not in ["past", "future"]:
        print("Invalid search direction")
        exit(1)

    makedirs("output", exist_ok=True)
    makedirs("output/dot", exist_ok=True)
    makedirs("output/index", exist_ok=True)
    makedirs("output/checkpoint", exist_ok=True)

    json_file = f"output/checkpoint/{graph_title}_k{graph_k}_{'_'.join(['_'.join(k) for k in keywords])}.json"
    if not path.exists(json_file):
        if not path.exists(args.seed_id_file):
            print("Seed file not found")
            exit(1)

        with open(args.seed_id_file, "r") as f:
            seed_id_list = [paper_id.strip() for paper_id in f.readlines()]

        graph = CitationGraph(
            title=graph_title,
            k=graph_k,
            seed_title_ids=seed_id_list,
            filter_by_title=filter_by_title,
            search_direction=search_direction,
            keywords=keywords,
        )
        graph.init_seed()
    else:
        print("Loading existing json file")
        graph = CitationGraph.from_json_file(json_file)

    while True:
        if graph.step():
            print(f"Nodes: {len(graph.nodes)}, Pending: {len(graph.pending_prenodes)}")
            graph.dump_json_file()
        else:
            break

    graph.export_dot_file(min_impact)

    print("Done")
