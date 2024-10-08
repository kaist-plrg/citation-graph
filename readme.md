# Citation Graph Generator

This script generates a citation graph using Semantic Scholar API

It is recommended to get an API key from Semantic Scholar to avoid rate limiting. ([Link](https://www.semanticscholar.org/product/api#api-key))
If you have an API key, you can set it as an environment variable `SS_API_KEY`.

## Requirements

* Python 3 (tested on 3.12.3)
* Python packages: `pip install -r requirements.txt`

## Usage

Execute the script from the command line as follows:

```bash
$ python main.py <seed-id-file> --depth <depth> --min-impact <min-impact> --keywords <keywords>
```

* `<seed-id-file>` : A text file containing paper IDs from the Semantic Scholar website. To obtain the paper ID, visit the paper page and extract the ID from the URL (e.g., `https://www.semanticscholar.org/paper/paper-title-goes-here/<paper-id>`). Each ID serves as a starting point to build the citation graph.
* `<depth>`: The maximum citation depth (optional, default is 2).
* `<min-impact>` The minimum number of citations needed for a paper to be included in the output (optional, default is 3).
* `<keywords>`: A list of keywords (separated by comma(`OR`) and ".."(`AND`); CNF). Papers are filtered to have at least one of the keywords in their title or abstract (optional, default is empty).
### Example

Assuming the seed paper IDs are in a file named `programming_languages.txt`
```
c54604dcc058b7526035d93646f2d7dec2c46668
064a00bfbead824626f698b8f7595b5a40e8d82b
450fe9db1def1800a98c0a633857b383910e0afc
...
```

To generate the graph, run:

```bash
python main.py programming_languages.txt --depth 2 --min-impact 1 --keywords programming,language
```

Next, to visualize the graph using Graphviz:

```bash
brew install graphviz
dot -Tpdf programming_language.dot > programming_language.pdf
```

## Output and Monitoring

* Progress is displayed in the console and saved in JSON format, allowing for
process resumption using the same seed file.
* The resulting `programming_languages.dot` and `programming_languages_index.txt`
files contain the citation graph and a list of paper titles indexed by
descending citation count, respectively.


Running the script will generate a dot file `programming_languages.dot` file
(indexed by `programming_languages_index.txt`, which is also generated by the
script) containing the citation graph, which can be visualized using Graphviz:

## Result Visualization
<img width="2667" alt="image" src="https://github.com/kaist-plrg/citation-graph/assets/68288688/6986661b-f334-4403-9c10-d8ee51e80a09">


Explore the titles in the `programming_languages_index.txt` file using index numbers referenced in the dot file.

