<span style="color:red;font-size:2em">

**⚠️ DO NOT RUN THIS USING PLRG/KAIST WIFI NETWORK ⚠️**

**⚠️ DO NOT RUN THIS USING PLRG/KAIST WIFI NETWORK ⚠️**

**⚠️ DO NOT RUN THIS USING PLRG/KAIST WIFI NETWORK ⚠️**

</span>

# ACM Digital Library Citation Graph Generator

This script generates a citation graph from the ACM Digital Library website.

**Do not run this script using PLRG/KAIST wifi network.** You may be blocked from
accessing the ACM Digital Library website, and the manager of the KAIST Academic
Information Office may come to see you.

It is recommended to run this script using a personal network such as a mobile
hotspot because cellular network on mobile phones always assigns a new IP.

Crawling speed is randomly limited from 5 to 10 seconds per request to avoid being
blocked by the website. The script will take a while to finish, so you can go to
bed after running the script.

## Requirements

* Python 3 (tested on 3.12.3)
* Python packages: `pip install -r requirements.txt`
* Internet connection **(not using PLRG/KAIST network)**

## Usage

```bash
$ python main.py <seed-url-file> --depth <depth> --min-impact <min-impact>
```

* `<seed-url-file>`
  * A file containing seed URLs. Each line should contain a URL of ACM Digital Library page.
  * Using these seed URLs as entry points, the script will generate a citation graph with the specified depth and minimum impact.
* `<depth>` (optional)
  * Maximum citation depth of the citation graph. Default is 2
* `<min-impact>` (optional)
  * Minimum number of citations to include a paper in the output dot file. Default is 3.

Assume that the seed URLs are stored in a file named `programming_languages.txt` that contains the following URLs:
```
https://dl.acm.org/doi/10.1145/3591270
https://dl.acm.org/doi/10.1145/3591254
...
```

Running the script will generate a `programming_languages.dot` file containing the citation graph, which can be visualized using Graphviz:

```bash
$ python main.py programming_languages.txt --depth 2 --min-impact 1  # This will take a while. Good night.
$ brew install graphviz
$ dot -Tpdf programming_language.dot > programming_language.pdf
```

Every progress will be printed on the console and will be saved in JSON files
and can be resumed by running the script again with the same seed URL file.

