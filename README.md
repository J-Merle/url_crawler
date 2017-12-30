# url_crawler

![pylint Score](https://mperlet.github.io/pybadge/badges/9.81.svg)

Simple scipt to recursively find links on a website and check for dead ones.

## How to use it ?
The script takes the root url you want to crawl as argument.

### Example

If you want to search for dead links on the repository use:

`python url.py -u https://github.com/J-Merle/url_crawler`

Type `python url.py --help` for complete parameters list

## Dependencies
- [bs4](https://pypi.python.org/pypi/beautifulsoup4/4.3.2 "bs4")
- [requests](https://pypi.python.org/pypi/requests "requests")
- [urllib.parse](https://docs.python.org/3/library/urllib.parse.html "urllib.parse")
