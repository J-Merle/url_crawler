from urllib.parse import urljoin
import argparse
import requests
from bs4 import BeautifulSoup


def get_urls(url, page):
    """ Get the list of all urls present on a specific page
    Arguments :
    url - the url to extract urls from
    page - the page to extract urls from

    """
    soup = BeautifulSoup(page, 'html.parser')
    return {urljoin(url, anchor.get('href'))
            for anchor in soup.find_all('a')}


class Crawler(object):
    """ Web crawler that can find dead links """

    def __init__(self, root_url, verbosity=False):
        self.invalid_urls = set()
        self.seen_urls = set()
        self.root_url = root_url
        self.verbosity = verbosity

    def report(self):
        """ Print the report of crawling """
        print("Seen urls : {}", len(self.seen_urls))
        print("Invalid urls : {}", len(self.invalid_urls))
        print("\n###########################")
        for url in self.invalid_urls:
            print("Invalid : {0}\nFound in {1}\n".format(url[0], url[1]))
        print("###########################")

    def crawl(self, url, parent_url):
        """ Check each link on a page recursively
        if the link is a subdomain of the root url

        Arguments :
        url - the url to check recursively
        parent_url - the url the current one has been found in
        """

        # We do not check an already seen url
        if url in self.seen_urls:
            return

        self.seen_urls.add(url)

        if self.verbosity:
            print(url)

        try:
            request = requests.get(url, timeout=2)
        except (requests.exceptions.InvalidSchema,
                requests.exceptions.ReadTimeout,
                requests.exceptions.MissingSchema,
                requests.exceptions.InvalidURL,
                requests.exceptions.TooManyRedirects):
            return
        except requests.exceptions.ConnectionError:
            self.invalid_urls.add((url, parent_url))
            return

        # Is it a dead link ?
        if request.status_code == 404:
            self.invalid_urls.add((url, parent_url))
            return

        # We do nothing else if the url is not a subdomain of root url
        if self.root_url not in url:
            return

        urls = get_urls(url, request.text)
        for found_url in urls:
            self.crawl(found_url, url)

    def analyze(self):
        """ Launch the crawler on the root url and print  report """
        print("Start scanning ...")
        self.crawl(self.root_url, "ROOT")
        self.report()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-v', '--verbose', action='store_true',
                        help='Display each url requested')
    PARSER.add_argument('-u', '--url', required=True,
                        help='The base url to crawl')
    ARGS = PARSER.parse_args()
    CRAWLER = Crawler(ARGS.url, ARGS.verbose)
    CRAWLER.analyze()
