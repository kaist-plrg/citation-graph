from typing import Optional

import requests
import os

from dataclasses import dataclass, field
import time
import json
import random

api_key = os.getenv("SS_API_KEY")

if not api_key:
    print("No API key provided. Rate limiting will be enforced.")


def request_uids(paper_ids: list[str]):
    while True:
        if api_key:
            time.sleep(1)
        else:
            time.sleep(5)
        headers = {"x-api-key": api_key} if api_key else {}
        res = requests.post(
            "https://api.semanticscholar.org/graph/v1/paper/batch",
            params={"fields": "title,year,venue,references"},
            json={"ids": paper_ids},
            headers=headers,
            timeout=30,
        )
        if res.status_code == 200:
            return [j for j in res.json() if j is not None]
        else:
            print(f"{res.status_code}: {res.reason} ... Retrying in 5 seconds")


def request_uid(paper_id: str):
    while True:
        if api_key:
            time.sleep(0.1)
        else:
            time.sleep(2)
        headers = {"x-api-key": api_key} if api_key else {}
        res = requests.get(
            f"https://api.semanticscholar.org/v1/paper/{paper_id}",
            params={"fields": "title,year,venue,references"},
            headers=headers,
            timeout=30,
        )
        if res.status_code == 200:
            return res.json()
        else:
            print(f"{res.status_code}: {res.reason} ... Retrying in 5 seconds")


@dataclass
class Prenode:
    curr_k: int
    paper_id: str
    parent_id: str = ""


@dataclass
class Node:
    curr_k: int
    paper_id: str
    title: str
    year: int
    venue: str = ""

    @staticmethod
    def from_paper_id(paper_id: str, curr_k: int) -> tuple["Node", list[Prenode]]:
        res_json = request_uid(paper_id)
        return Node(
            curr_k=curr_k,
            paper_id=res_json["paperId"],
            title=res_json["title"],
            year=res_json["year"],
            venue=res_json.get("venue", ""),
        ), [
            Prenode(
                curr_k=curr_k + 1,
                paper_id=ref_json["paperId"],
                parent_id=paper_id,
            )
            for ref_json in res_json.get("references", [])
        ]

    @staticmethod
    def from_prenodes(prenodes: list[Prenode]) -> tuple[list["Node"], list[Prenode]]:
        nodes = []
        pending_nodes = []

        uids = [prenode.paper_id for prenode in prenodes]

        res_jsons = request_uids(uids)

        for i, res_json in enumerate(res_jsons):
            k = prenodes[i].curr_k
            node_paper_id = res_json["paperId"]
            node_title = res_json["title"]
            node_year = res_json["year"]

            if node_paper_id is None or node_title is None or node_year is None:
                continue

            references = res_json.get("references", [])
            for ref_json in references:
                ref_paper_id = ref_json["paperId"]
                if ref_paper_id:
                    pending_nodes.append(
                        Prenode(
                            curr_k=k + 1,
                            paper_id=ref_paper_id,
                            parent_id=res_json["paperId"],
                        )
                    )
            nodes.append(
                Node(
                    curr_k=k,
                    paper_id=res_json["paperId"],
                    title=res_json["title"],
                    year=res_json["year"],
                    venue=res_json.get("venue", ""),
                )
            )

        return nodes, pending_nodes


if __name__ == "__main__":
    # soup = get_soup("https://dl.acm.org/doi/10.1145/3314221.3314642")
    # print(
    #     Node.from_prenodes(
    #         [
    #             Prenode(0, "649def34f8be52c8b66281af98ae884c09aef38b"),
    #             Prenode(0, "ARXIV:2106.15928"),
    #         ]
    #     )[0]
    # )
    print(Node.from_paper_id("649def34f8be52c8b66281af98ae884c09aef38b", 0)[1])
