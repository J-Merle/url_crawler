# url_crawler

Simple scipt to recursively find links on a website and check for dead ones.

## How to use it ?
The script takes the root url you want to crawl as argument.

### Example

If you want to search for dead links on the repository use:

`python url.py https://github.com/J-Merle/url_crawler`

## Dependencies
- [bs4](https://pypi.python.org/pypi/beautifulsoup4/4.3.2 "bs4")
- [requests](https://pypi.python.org/pypi/requests "requests")
- [urllib.parse](https://docs.python.org/3/library/urllib.parse.html "urllib.parse")
