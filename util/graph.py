from collections import Counter
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

from util.node import Node, Prenode


@dataclass_json
@dataclass
class CitationGraph:
    title: str
    k: int
    seed_title_ids: list[str]
    keywords: list[list[str]]
    filter_by_title: bool
    search_direction: str
    pending_prenodes: list[Prenode] = field(default_factory=list)
    nodes: list[Node] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)

    def paper_id_exists(self, paper_id: str) -> bool:
        for node in self.nodes:
            if node.paper_id == paper_id:
                return True
        return False

    def find_by_paper_id(self, paper_id: str) -> Node:
        for node in self.nodes:
            if node.paper_id == paper_id:
                return node
        return None

    def paper_id_to_title(self, paper_id: str) -> str:
        node = self.find_by_paper_id(paper_id)
        return node.title if node else ""

    def filename(self) -> str:
        return (
            f"{self.title}_k{self.k}_{'_'.join(['_'.join(k) for k in self.keywords])}"
        )

    def update_k(self, title: str, new_k: int):
        node = self.find_by_paper_id(title)
        if node is None:
            return
        if node.curr_k <= new_k or self.k <= new_k:
            return
        if node.curr_k == self.k:  # update k and extend the graph
            self.nodes.remove(node)
            self.pending_prenodes.append(Prenode(curr_k=new_k, paper_id=node.paper_id))
        else:  # only update k
            node.curr_k = new_k
            for parent_title, child_title in self.edges:
                if parent_title == title:
                    self.update_k(child_title, new_k + 1)

    def init_seed(self):
        if not self.nodes:
            for seed_url in self.seed_title_ids:
                self.pending_prenodes.append(Prenode(curr_k=0, paper_id=seed_url))

    def step(self) -> bool:
        if self.pending_prenodes:
            curr_prenodes = []
            while len(curr_prenodes) < 400:
                prenode = self.pending_prenodes.pop()
                if prenode.curr_k <= self.k and not self.paper_id_exists(
                    prenode.paper_id
                ):
                    curr_prenodes.append(prenode)
                elif self.paper_id_exists(prenode.paper_id):
                    self.update_k(prenode.paper_id, prenode.curr_k)  # update k
                if not self.pending_prenodes:
                    break

            if not curr_prenodes:
                return False

            nodes, pending_nodes = Node.from_prenodes(
                curr_prenodes,
                self.keywords,
                self.filter_by_title,
                self.search_direction,
            )

            self.edges.extend(
                [
                    (
                        (node.parent_id, node.paper_id)
                        if self.search_direction == "past"
                        else (node.paper_id, node.parent_id)
                    )
                    for node in nodes
                ]
            )

            self.nodes.extend(nodes)
            self.pending_prenodes.extend(pending_nodes)

            return True
        else:
            return False

    def dump_json_file(self, alternative_filename: str = None):
        title = alternative_filename if alternative_filename else self.title
        with open(f"output/checkpoint/{self.filename()}.json", "w") as f:
            f.write(self.to_json(indent=4))

    def export_dot_file(self, min_impact: int = 3):
        counter = Counter([child for _, child in self.edges])
        edges = [
            (parent, child)
            for parent, child in self.edges
            if (counter[child] >= min_impact or counter[parent] >= min_impact)
            and self.find_by_paper_id(child) is not None
            and self.find_by_paper_id(parent) is not None
            # and self.find_by_paper_id(child).title.strip() != ""
            # and "quantum" in self.find_by_paper_id(child).title.lower()
        ]
        nodes = sorted(
            set([node for edge in edges for node in edge]),
            key=lambda x: counter[x],
            reverse=True,
        )
        node_to_index = {node: i for i, node in enumerate(nodes)}

        nxgraph = nx.DiGraph()
        nxgraph.add_nodes_from([(i, {"title": i}) for i, _ in enumerate(nodes)])

        edges_index = [
            (node_to_index[parent], node_to_index[child]) for parent, child in edges
        ]

        nxgraph.add_edges_from(edges_index)

        write_dot(nxgraph, f"output/dot/{self.filename()}.dot")

        with open(f"output/index/{self.filename()}_index.txt", "w") as f:
            f.writelines(
                [
                    f"{i:4} {self.paper_id_to_title(node)} ({counter[node]}, {node})\n"
                    for i, node in enumerate(nodes)
                ]
            )

        for node in nodes:
            print(f'"{node}",')

    @staticmethod
    def from_json_file(filename: str) -> "CitationGraph":
        with open(filename, "r") as f:
            return CitationGraph.from_json(f.read())


if __name__ == "__main__":
    quantum_seed_url_list = [
        # PLDI 2023
        # An Automata-Based Framework for Verification and Bug Hunting in Quantum Circuits
        "https://dl.acm.org/doi/10.1145/3591270",
        # Synthesizing Quantum-Circuit Optimizers
        "https://dl.acm.org/doi/10.1145/3591254",
        # PLDI 2022
        # Algebraic reasoning of Quantum programs via non-idempotent Kleene algebra
        "https://dl.acm.org/doi/10.1145/3519939.3523713",
        # Giallar: push-button verification for the qiskit Quantum compiler
        "https://dl.acm.org/doi/10.1145/3519939.3523431",
        # Quartz: superoptimization of Quantum circuits
        "https://dl.acm.org/doi/10.1145/3519939.3523433",
        # PLDI 2021
        # Gleipnir: toward practical error analysis for Quantum programs
        "https://dl.acm.org/doi/10.1145/3453483.3454029",
        # Quantum abstract interpretation
        "https://dl.acm.org/doi/10.1145/3453483.3454061",
        # Unqomp: synthesizing uncomputation in Quantum circuits
        "https://dl.acm.org/doi/10.1145/3453483.3454040",
        # PLDI 2020
        # On the principles of differentiable quantum programming languages
        "https://dl.acm.org/doi/abs/10.1145/3385412.3386011",
        # Silq: A High-Level Quantum Language with Safe Uncomputation and Intuitive Semantics
        "https://dl.acm.org/doi/10.1145/3385412.3386007",
        # POPL 2023
        # CoqQ: Foundational Verification of Quantum Programs
        "https://dl.acm.org/doi/10.1145/3571222",
        # Qunity: A Unified Language for Quantum and Classical Computing
        "https://dl.acm.org/doi/10.1145/3571225",
        # POPL 2022
        # A Quantum interpretation of separating conjunction for local reasoning of Quantum programs based on separation logic
        "https://dl.acm.org/doi/10.1145/3498697",
        # Quantum information effects
        "https://dl.acm.org/doi/10.1145/3498663",
        # Semantics for variational Quantum programming
        "https://dl.acm.org/doi/10.1145/3498687",
        # Twist: sound reasoning for purity and entanglement in Quantum programs
        "https://dl.acm.org/doi/10.1145/3498691",
        # POPL 2021
        # A verified optimizer for Quantum circuits
        "https://dl.acm.org/doi/10.1145/3434318",
        # POPL 2020
        # Full abstraction for the quantum lambda-calculus
        "https://dl.acm.org/doi/10.1145/3371131",
        # Relational proofs for quantum programs
        "https://dl.acm.org/doi/10.1145/3371089",
        # OOPSLA 2023
        # Modular Component-Based Quantum Circuit Synthesis
        "https://dl.acm.org/doi/10.1145/3586039",
        # OOPSLA 2022
        # Bugs in Quantum computing platforms: an empirical study
        "https://dl.acm.org/doi/10.1145/3527330",
        # On incorrectness logic for Quantum programs
        "https://dl.acm.org/doi/10.1145/3527316",
        # Tower: data structures in Quantum superposition
        "https://dl.acm.org/doi/10.1145/3563297",
        # Verified compilation of Quantum oracles
        "https://dl.acm.org/doi/10.1145/3563309",
        # OOPSLA 2020
        # Assertion-based optimization of Quantum programs
        "https://dl.acm.org/doi/10.1145/3428201",
        # Enabling accuracy-aware Quantum compilers using symbolic resource estimation
        "https://dl.acm.org/doi/10.1145/3428198",
        # Projection-based runtime assertions for testing and debugging Quantum programs
        "https://dl.acm.org/doi/10.1145/3428218",
        # ICSE 2023
        # MorphQ: Metamorphic Testing of the Qiskit Quantum Computing Platform
        "https://dl.acm.org/doi/abs/10.1109/ICSE48619.2023.00202",
        # The Smelly Eight: An Empirical Study on the Prevalence of Code Smells in Quantum Computing
        "https://dl.acm.org/doi/abs/10.1109/ICSE48619.2023.00041",
        # ASE 2021
        # QDiff: Differential Testing of Quantum Software Stacks
        "https://dl.acm.org/doi/10.1109/ASE51524.2021.9678792",
    ]
    # graph = CitationGraph(
    #     title="quantum_pl",
    #     seed_title_ids=quantum_seed_url_list,
    #     k=3,
    # )
    # graph = CitationGraph.from_json_file("quantum_pl.json")

    # graph.init_seed()

    while True:
        if graph.step():
            print(f"Nodes: {len(graph.nodes)}, Pending: {len(graph.pending_prenodes)}")
            graph.dump_json_file()
        else:
            break
