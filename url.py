import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

invalid_urls = set()
seen_urls = set()

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Display each url requested')
parser.add_argument('-u', '--url', required=True,
                    help='The base url to crawl')
args = parser.parse_args()

base_url = args.url


def findUrls(url, parent):
    if url in seen_urls:
        return
    if args.verbose:
        print(url)
    seen_urls.add(url)
    page = ""
    try:
        r = requests.get(url, timeout=1)
        if r.status_code == 404:
            print("Invalid :")
            print(url)
            print("Found in ->" + parent)
            invalid_urls.add(url)
            return
        if base_url not in url:
            return
        page = r.text
    except:
        pass

    soup = BeautifulSoup(page, 'html.parser')
    urls = {urljoin(url, anchor.get('href'))
            for anchor in soup.find_all('a')}

    for newUrl in urls - {None, ""}:
        findUrls(newUrl, url)


findUrls(base_url, "Base request")

print("Total urls checked : " + str(len(seen_urls)))

print("Invalid urls : " + str(len(invalid_urls)))
