from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

from dataclasses import dataclass, field
import time
import random


def get_soup(url) -> BeautifulSoup:
    time.sleep(random.uniform(5, 10))
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        # "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        # "Cookie": "MAID=xEgbAuerYxK1LjKdveWUPQ==; _hjSessionUser_1290436=eyJpZCI6IjY5ODViOTMyLTg2ZTgtNTg5Ny04Y2QzLWM1NDk2N2VkMThmZSIsImNyZWF0ZWQiOjE2NjI1MzA4MjU4MzIsImV4aXN0aW5nIjp0cnVlfQ==; cookiePolicy=accept; CookieConsent={stamp:%27z4MdrQxcmUPJViYBW2WEH/zLewovHirczYUlazKdoMF7MLOrIIQ8CQ==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1699971954556%2Cregion:%27kr%27}; _ga=GA1.2.620853368.1708648733; _gid=GA1.2.527177585.1715167342; MSopened=02b075ed48492ef0e7598ddf9762f5ef668d7320; MSopened.02b075ed48492ef0e7598ddf9762f5ef668d7320=true; _cfuvid=wl5duXzd2.tKc3yHbU4hYRO36ZFf6vCBODrWdVDW.Uk-1715175656762-0.0.1.1-604800000; cf_clearance=jL4_O8PDrZueNTGGP1yQzHXxn5t6c5j2a2gTpwytFn8-1715185386-1.0.1.1-zI6vO76vDMs0eGTSEngZRsKP0bFvSDVU_ZuVTUJTMOvaukT3e4pp30mKse5nSNwBLhqDr8rw2GWMo01ZxnbDnw; JSESSIONID=b3ec9872-73a3-4903-9d53-dfef1835dd1d; MACHINE_LAST_SEEN=2024-05-08T20%3A18%3A55.504-07%3A00; _hjSession_1290436=eyJpZCI6IjRkZDc0OTA4LWNjODktNDdjOC1hNGQ0LWQ0YjA3MDlhOWZlZSIsImMiOjE3MTUyMjQ3MzY5NTQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _hp2_ses_props.1083010732=%7B%22ts%22%3A1715224736656%2C%22d%22%3A%22dl.acm.org%22%2C%22h%22%3A%22%2Fdoi%2F10.1145%2F3453483.3454029%22%7D; __cf_bm=m9ye8JgjfDxoP3Bx_dk00AM7tHcoQTAQE3WGTuLhGhc-1715226737-1.0.1.1-U42azFyrY6z7a1VKt39TqT1vCnykt8ecA8lPUHxd21rEnps8OOK7MhI7GrMCpr.bQKjxglYkW4YxKcZWX226SQ; cf_clearance=Vvy.lN.6UD88m7pTxO6TCCmUMq3mJKraj_z.JRk2.T8-1715226738-1.0.1.1-LTj2ZSW3_2NWuZAspc0o3L67Z_nYVI3RoO1gEmrnDWj4amNLbdsTXLrPZrs9rtJTNOBAnxL0_aIb8giZMIH5vg; _hp2_id.1083010732=%7B%22userId%22%3A%225161421557096401%22%2C%22pageviewId%22%3A%221952351675772909%22%2C%22sessionId%22%3A%222990868672053676%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_JPDX9GZR59=GS1.2.1715224737.19.1.1715226877.0.0.0; _cfuvid=hSPCbPj.AtA.4if2k7KcQyczMo7ZVvM0MVVjVI53Xak-1715226877294-0.0.1.1-604800000; _gali=disqus_thread",
        "Referer": "https://dl.acm.org/conference/pldi",
        "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        # "Sec-Fetch-Dest": "document",
        # "Sec-Fetch-Mode": "navigate",
        # "Sec-Fetch-Site": "same-origin",
        # "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    session_obj = requests.Session()
    response = session_obj.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_title(soup: BeautifulSoup) -> Optional[str]:
    try:
        title = soup.find("h1", class_="citation__title").text
    except AttributeError:
        try:
            title = soup.find("title").text
        except Exception:
            title = None
    return title


def extract_year(soup: BeautifulSoup) -> Optional[str]:
    try:
        day_month_year = soup.find("span", class_="CitationCoverDate").text
        return day_month_year.split()[-1]  # 01 June 2019 -> [01, June, 2019] -> 2019
    except AttributeError:
        return None


def extract_conference(soup: BeautifulSoup) -> Optional[str]:
    try:
        conf_year = soup.find("span", class_="epub-section__title").text.split(":")[0]
        return "".join([char for char in conf_year if char.isalpha()])
    except AttributeError:
        return None


def extract_ref_list(soup: BeautifulSoup) -> Optional[list[Tag]]:
    ol_tag = soup.find("ol", class_="rlist references__list references__numeric")
    if ol_tag:
        return list(ol_tag.find_all("li"))
    else:
        return None


@dataclass
class Node:
    curr_k: int
    title: str
    parent_title: str = ""
    year: str = ""
    conference: str = ""
    url: str = ""

    @staticmethod
    def from_ref_tag(parent_title: str, ref_tag: Tag, k: int) -> "Node":
        url = None
        for link in ref_tag.find_all("a"):
            image = link.find("img")
            image_title = image.get("alt") if image else None
            if image_title == "Digital Library":
                url = link.get("href")
        content = ref_tag.find("span", class_="references__note").text.strip()
        content_split = content.split(".")

        if len(content_split) >= 2:
            if content_split[1].strip().isdigit():
                if len(content_split) >= 3:
                    content = content_split[2].strip()
            else:
                content = content_split[1].strip()

        full_url = "https://dl.acm.org" + url if url else ""
        return Node(k, content, parent_title=parent_title, url=full_url)

    @staticmethod
    def from_url(url: str, k: int, parent_title: str) -> tuple["Node", list["Node"]]:
        print(url)
        try:
            soup = get_soup(url)
            title = extract_title(soup)
            year = extract_year(soup)
            conference = extract_conference(soup)

            if title is None:
                print("Could not extract title from", url)
                return None, []
            if year is None:
                print("Could not extract year from", url)
                return None, []
            if conference is None:
                print("Could not extract conference from", url)
                return None, []

            ref_list = extract_ref_list(soup)
            ref_list = ref_list if ref_list else []

            children = [
                Node.from_ref_tag(title, ref_tag, k + 1) for ref_tag in ref_list
            ]
            return Node(k, title, parent_title, year, conference, url), children
        except requests.exceptions.HTTPError as e:
            print(e)
            return None, None
        except Exception as e:
            print(e)
            return None, []


@dataclass
class ACMNode:
    title: str
    year: str
    conference: str
    url: str
    children: list[Node] = field(default_factory=list)

    @staticmethod
    def from_url(url: str, depth: int = 1) -> "ACMNode":
        print(url)
        soup = get_soup(url)
        title = extract_title(soup)
        year = extract_year(soup)
        conference = extract_conference(soup)
        if title is None or year is None or conference is None:
            print("Could not extract title, year, or conference from", url)
            return None
        elif depth <= 0:
            return ACMNode(title, year, conference, url)
        else:
            ref_list = extract_ref_list(soup)
            children = [Node.from_ref_tag(ref_tag, depth - 1) for ref_tag in ref_list]
            return ACMNode(title, year, conference, url, children)


if __name__ == "__main__":
    # soup = get_soup("https://dl.acm.org/doi/10.1145/3314221.3314642")
    # print(
    #     extract_ref_list(soup)[-1].find("i").text,
    #     sep="\n" * 2,
    # )

    print(Node.from_url("https://dl.acm.org/doi/10.1145/3314221.3314642", 1, ""))

    # print(extract_title(soup))
    # print(extract_year(soup))
    # print(extract_conference(soup))
