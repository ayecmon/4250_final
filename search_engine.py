from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from pandas import Index
import numpy

def load_inverted_index():
    client = MongoClient('localhost', 27017)
    db = client['biology']
    inverted_index_collection = db.inverted_index

    # Retrieve the inverted index from MongoDB
    inverted_index_doc = inverted_index_collection.find_one()
    inverted_index = inverted_index_doc.get('inverted_index', {})

    return inverted_index

def search(query, inverted_index):
    # Initialize a TfidfVectorizer with the same stop words
    stop_words = ['I', 'and', 'she', 'She', 'they', 'They', 'her', 'their', 'the']
    vectorizer = TfidfVectorizer(stop_words=stop_words)

    # Tokenize and compute TF-IDF values for the query
    query_tfidf_values = vectorizer.fit_transform([query])
    query_feature_names = vectorizer.get_feature_names_out()

    # Calculate cosine similarity between the query and each document in the inverted index
    similarities = {}
    for term in query_feature_names:
        if term in inverted_index:
            doc_ids = inverted_index[term]['doc_ids']
            for doc_id in doc_ids:
                if doc_id not in similarities:
                    similarities[doc_id] = 0
                if term in inverted_index:
                    term_index = numpy.where(query_feature_names == term)[0]
                    if term_index:
                        similarities[doc_id] += query_tfidf_values[0, term_index[0]] * inverted_index[term]['tfidf_scores'][doc_id]

    # Sort the documents by cosine similarity
    sorted_docs = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    # Retrieve and return the relevant faculty pages
    client = MongoClient('localhost', 27017)
    db = client['biology']
    target_pages_collection = db.target_pages
    relevant_pages = []
    for doc_id, _ in sorted_docs:
        faculty_page = target_pages_collection.find_one({"_id": int(doc_id)})
        relevant_pages.append(faculty_page)

    return relevant_pages

def extract_name_from_fac_info_content(fac_info_content):
    lines = fac_info_content.split('\n')
    return(lines[6])

def printMenu(firstTime):
    print('\n#########################################')
    if firstTime:
        print()
        print("Welcome to the CPP Biology Search Engine!")
    
    query = str(input("Enter a query or press enter or 'q' to quit: "))

    if query == 'q' or query == "":
        exit()
    else:
        return(query)
    
def printResults(results):
    print()
    # Print the relevant faculty names and URLs
    if len(results) > 0:
        for result in results:
            faculty_content = result.get('faculty_content', {}).get('fac_info_content', '')
            faculty_name = extract_name_from_fac_info_content(faculty_content)
            faculty_url = result.get('url', '')
            
            print(f"Professor Name: {faculty_name}")
            print(f"URL: {faculty_url}")
            print()
    else:
        print("No results matched your search")

if __name__ == "__main__":
    # Load the inverted index
    inverted_index = load_inverted_index()
    firstTime = True

    while True:
        index = 0

        query = ""
        query = printMenu(firstTime)

        results = []
        # Example search without pagination
        results = search(query, inverted_index)
        
        # Print the first 5 results
        printResults(results[index:5])

        # Check if there are more results
        if len(results) > 5:
            view_next = input("Press 'n' or 'next' to view the next page, or press Enter to quit: ")
            if view_next.lower() not in {'n', 'next'}:
                break
            else:
                index = index + 5
                printResults(results[index:index+5])

        firstTime = False
