import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer


#Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['biology']
pages_collection = db.pages

frontier = ['https://www.cpp.edu/sci/biological-sciences/index.shtml']
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
def parse(html):
    pass

#crawling
def crawlerThread(frontier, num_targets):
    targets_found = 0
    while frontier != 0:
        url = frontier.pop(0)
        html = retrieveUrl(url)
        storePages(url, html)
        if targetPage(html):
            targets_found += 1
            if targets_found == num_targets:
                frontier.clear()
        else:
            for newUrl in parse(html):
                frontier.append(newUrl)
