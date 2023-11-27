import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer


#Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['biology']
pages_collection = db.pages

frontier = ['https://www.cpp.edu/sci/biological-sciences/index.shtml']
visited_links = set()
num_targets = 10

#stores pages
def storePages(url, html):
    pages_collection.insert_one({"url" : url, 'html' : html})

#retrieves URL
def retrieveUrl(url):
    try:
        html = urlopen(url).read()
        return html
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')

#target page
def targetPage(html):
    #Check if it is target page
    pass

#parsing
def parse(html, baseUrl):
    bs = BeautifulSoup(html, 'html.parser')
    links = []

    for link in bs.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(baseUrl, href)
        links.append(full_url)

    return links

#crawling
def crawlerThread(frontier, num_targets):
    targets_found = 0
    while frontier != 0:
        url = frontier.pop(0)
        visited_links.add(url)
        html = retrieveUrl(url)
        storePages(url, html)
        if targetPage(html):
            targets_found += 1
            if targets_found == num_targets:
                frontier.clear()
        else:
            for newUrl in parse(html, url):
                if newUrl not in visited_links and newUrl not in frontier:
                    frontier.append(newUrl)
