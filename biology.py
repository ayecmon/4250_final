import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List


def main():
    # Connect to MongoDB
    seed_urls = ['https://www.cpp.edu/sci/biological-sciences/index.shtml']
    frontier = CrawlerFrontier(seed_urls)
    num_targets = 10
    crawlerThread(frontier, num_targets)


class CrawlerFrontier:
    def __init__(self, seed_frontier: List[str]):
        self.frontier = seed_frontier
        self.visited_links = set()
# stores pages


def storePages(url, html):
    try:
        client = MongoClient('localhost', 27017)
        db = client['biology']
        pages_collection = db.pages
    except Exception:
        print("unable to connect to db")
    try:
        pages_collection.insert_one({"url": url, 'html': html})
    except Exception:
        print("error adding the page to db")


# retrieves URL
def retrieveUrl(url):
    try:
        html = urlopen(url).read()
        return html
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')


# target page
def targetPage(html):
    # Check if it is target page
    bs = BeautifulSoup(html, 'html.parser')
    if (bs.find('ul', {'class': 'fac-nav'})
            and bs.find('div', {'class': 'fac-staff'})):
        return True
    return False

    pass


# parsing
def parse(html, baseUrl):
    bs = BeautifulSoup(html, 'html.parser')
    links = []

    for link in bs.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(baseUrl, href)
        links.append(full_url)

    return links


# crawling
def crawlerThread(frontier: CrawlerFrontier, num_targets: int):
    targets_found = 0
    visited_links = frontier.visited_links
    frontier = frontier.frontier
    while len(frontier) != 0:
        url = frontier.pop(0)
        visited_links.add(url)
        html = retrieveUrl(url)
        # returns none if bad html
        if (html):
            storePages(url, html)
            if targetPage(html):
                print("found a target page: ", url)
                targets_found += 1
                if targets_found == num_targets:
                    frontier.clear()
            else:
                for newUrl in parse(html, url):
                    if newUrl not in visited_links and newUrl not in frontier:
                        frontier.append(newUrl)


if __name__ == "__main__":
    main()
