from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from util.node import Node


@dataclass_json
@dataclass
class CitationGraph:
    title: str
    k: int
    seed_url_list: list[str]
    pending_node_list: list[Node] = field(default_factory=list)
    nodes: list[Node] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)

    def title_exists(self, title: str) -> bool:
        for node in self.nodes:
            if node.title == title:
                return True
        return False

    def find_by_title(self, title: str) -> Node:
        for node in self.nodes:
            if node.title == title:
                return node
        return None

    def append_node(self, node: Node):
        self.nodes.append(node)
        if node.parent_title:
            self.edges.append((node.parent_title, node.title))

    def update_k(self, title: str, new_k: int):
        node = self.find_by_title(title)
        if node is None:
            return
        if node.curr_k <= new_k or self.k <= new_k:
            return
        if node.curr_k == self.k:  # update k and extend the graph
            node.curr_k = new_k
            if node.url:
                _, children = Node.from_url(node.url, new_k, node.parent_title)
                children = children if children else []
                for child in children:
                    if child.curr_k <= self.k:
                        self.pending_node_list.append(child)
        else:  # only update k
            node.curr_k = new_k
            for parent_title, child_title in self.edges:
                if parent_title == title:
                    self.update_k(child_title, new_k + 1)

    def append_node_from_url(self, url: str, k: int, parent_title: str = "") -> bool:
        node, children = Node.from_url(url, k, parent_title)
        if children is None:
            return False
        elif not node:
            return True
        self.append_node(node)
        for child in children:
            if child.curr_k <= self.k:
                self.pending_node_list.append(child)
        return True

    def init_seed(self):
        if not self.nodes:
            for seed_url in self.seed_url_list:
                self.append_node_from_url(seed_url, 0)

    def step(self) -> bool:
        if self.pending_node_list:
            node = self.pending_node_list.pop()
            if node.curr_k <= self.k and not self.title_exists(node.title):
                if node.url:
                    append_res = self.append_node_from_url(
                        node.url, node.curr_k, node.parent_title
                    )
                    if not append_res:
                        return False
                else:
                    self.append_node(node)
                    return self.step()
            elif self.title_exists(node.title):
                self.update_k(node.title, node.curr_k)
            return True
        else:
            return False

    def dump_json_file(self, alternative_filename: str = None):
        title = alternative_filename if alternative_filename else self.title
        with open(f"{title}.json", "w") as f:
            f.write(self.to_json(indent=4))

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
    #     title="quantum_test",
    #     seed_url_list=quantum_seed_url_list,
    #     # seed_url_list=["https://dl.acm.org/doi/10.1145/3519939.3523443"],
    #     # seed_url_list=["https://dl.acm.org/doi/10.1145/507669.507658"],
    #     k=2,
    # )
    graph = CitationGraph.from_json_file("quantum_test.json")
    ref_count = dict()https://dl.acm.org/doi/10.1145/3571225
    # for parent, child in graph.edges:

    # graph.init_seed()
    # while True:
    #     if not graph.step():
    #         break
    #     else:
    #         print(f"Nodes: {len(graph.nodes)}, Pending: {len(graph.pending_node_list)}")
    #         graph.dump_json_file()
