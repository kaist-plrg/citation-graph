<span style="color:red;font-size:2em">

**⚠️ DO NOT RUN THIS USING PLRG/KAIST WIFI NETWORK ⚠️**

**⚠️ DO NOT RUN THIS USING PLRG/KAIST WIFI NETWORK ⚠️**

**⚠️ DO NOT RUN THIS USING PLRG/KAIST WIFI NETWORK ⚠️**

</span>

# ACM Digital Library Citation Graph Generator

This script generates a citation graph from the ACM Digital Library website.

**Important Notice: Do not run this script using PLRG/KAIST wifi network.** You may be blocked from
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

Execute the script from the command line as follows:

```bash
$ python main.py <seed-url-file> --depth <depth> --min-impact <min-impact>
```

* `<seed-url-file>` : A text file containing URLs from the ACM Digital Library. Each URL serves as a starting point to build the citation graph.
* `<depth>`: The maximum citation depth (optional, default is 2).
* `<min-impact>` The minimum number of citations needed for a paper to be included in the output (optional, default is 3).

### Example

Assuming the seed URLs are in a file named `programming_languages.txt`
```
https://dl.acm.org/doi/10.1145/3591270
https://dl.acm.org/doi/10.1145/3591254
...
```

To generate the graph, run:

```bash
python main.py programming_languages.txt --depth 2 --min-impact 1
```

Next, to visualize the graph using Graphviz:

```bash
brew install graphviz
dot -Tpdf programming_language.dot > programming_language.pdf
```

## Output and Monitoring

* Progress is displayed in the console and saved in JSON format, allowing for
process resumption using the same seed URL file.
* The resulting `programming_languages.dot` and `programming_languages_index.txt`
files contain the citation graph and a list of paper titles indexed by
descending citation count, respectively.


Running the script will generate a dot file `programming_languages.dot` file
(indexed by `programming_languages_index.txt`, which is also generated by the
script) containing the citation graph, which can be visualized using Graphviz:

## Result Visualization
<img width="2447" alt="image" src="https://github.com/kaist-plrg/acm-citgraph-crawler/assets/68288688/9f8c41ce-39b9-4982-b065-1dd643bbc58e">

Explore the titles in the `programming_languages_index.txt` file using index numbers referenced in the dot file.

