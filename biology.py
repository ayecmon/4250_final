from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List


def main():
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
        # Connect to mongo
        client = MongoClient('localhost', 27017)
        db = client['biology']
        pages_collection = db.pages
        target_pages_collection = db.target_pages

        #Extract the faculty content
        faculty_content = parse_faculty_content(html)

        # Get the next unique ID for the document
        document_id = target_pages_collection.count_documents({}) + 1

        #Store the page in the database with the URL, HTML, and faculty content
        pages_collection.insert_one({"url": url, 'html': html, 'faculty_content': faculty_content})

        # Check if it's a target page and store in the target pages collection
        if targetPage(html):
            target_pages_collection.insert_one({"_id": document_id, 'faculty_content': faculty_content, 'url': url})
    except Exception:
        print("Error while storing the page in the database.")


# retrieves URL
def retrieveUrl(url):
    print("Attempting to retrieve URL:", url)
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
        href = link['href'].strip()
        full_url = urljoin(baseUrl, href)
        links.append(full_url)

    return links

def parse_faculty_content(html):
    bs = BeautifulSoup(html, 'html.parser')

    fac_staff_div = bs.find('div', {'class': 'fac-staff'})
    accolades_div = bs.find('div', {'class': 'accolades'})
    fac_info_div = bs.find('div', {'class': 'fac-info'})

    # Extract the text content of each <div> element
    fac_staff_content = fac_staff_div.get_text() if fac_staff_div else ''
    accolades_content = accolades_div.get_text() if accolades_div else ''
    fac_info_content = fac_info_div.get_text() if fac_info_div else ''

    # Return or process the extracted content as needed
    return {
        'fac_staff_content': fac_staff_content,
        'accolades_content': accolades_content,
        'fac_info_content': fac_info_content,
    }

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


def build_inverted_index_tfidf():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['biology']
    target_pages_collection = db.target_pages
    inverted_index_collection = db.inverted_index  # New collection for the inverted index
    stop_words = ['I', 'and', 'she', 'She', 'they', 'They', 'her', 'their', 'the']

    # Initialize a TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words=stop_words)

    # Get all documents from the target_pages_collection
    documents = target_pages_collection.find()

    # Initialize the inverted index
    inverted_index = {}

    for doc in documents:
        # Get the document ID and faculty content
        doc_id = doc['_id']
        faculty_content_dict = doc['faculty_content']

        # Combine content from different fields into a single string
        faculty_content = combine_faculty_content(faculty_content_dict)

        # Tokenize and compute TF-IDF values for the faculty content
        tfidf_values = vectorizer.fit_transform([faculty_content])

        # Extract feature names and corresponding TF-IDF values
        feature_names = vectorizer.get_feature_names_out()
        tfidf_dict = dict(zip(feature_names, tfidf_values.toarray()[0]))

        # Update the inverted index with TF-IDF values and document IDs
        for term, tfidf_score in tfidf_dict.items():
            if term not in inverted_index:
                inverted_index[term] = {'doc_ids': [], 'tfidf_scores': {}}

            inverted_index[term]['doc_ids'].append(str(doc_id))  # Convert to string
            inverted_index[term]['tfidf_scores'][str(doc_id)] = tfidf_score

    # Store the inverted index in MongoDB
    inverted_index_collection.insert_one({'inverted_index': inverted_index})

    return inverted_index

def combine_faculty_content(faculty_content_dict):
    # Combine content from different fields into a single string
    fac_staff_content = faculty_content_dict.get('fac_staff_content', '')
    accolades_content = faculty_content_dict.get('accolades_content', '')
    fac_info_content = faculty_content_dict.get('fac_info_content', '')

    combined_content = f"{fac_staff_content} {accolades_content} {fac_info_content}"
    
    return combined_content

if __name__ == "__main__":
    main()
    inverted_index_tfidf = build_inverted_index_tfidf()
    print(inverted_index_tfidf)
