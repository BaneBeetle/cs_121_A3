# Implements Boolean retrieval (Milestone 2)

import json
import math
from index import tokenize
import time


def load_index(index_file='index.json'):
    """ Load the inverted index from the disk """
    # idea for performance boost? memory-mapped files (idk gpt said so)
    with open(index_file, 'r', encoding='utf-8') as file:
        inverted_index = json.load(file)
        return inverted_index


def boolean_retrieval(query, inverted_index, top_k=5, total_docs=55393):
    """
        Process a Boolean query using the inverted index.
        Should support AND operations.
        Implements TF-IDF ranking
        """

    query_tokens = tokenize(query)
    doc_sets = []  # list of sets of document IDs per token
    doc_tfidf = {}  # dict to store tf-idf scores
    doc_urls = {}  # map doc_id to URL

    # for each token, get the list of documents
    for token in query_tokens:
        if token in inverted_index:
            postings = inverted_index[token]  # {doc_id: (freq, url)}
            # print(f"Token: {token}, Postings: {postings}, Type: {type(postings)}") <- debugging
            # doc_sets.append(set(postings.keys()))  # collect document IDs

            if isinstance(postings, dict):  # Ensure postings is a dictionary
                doc_sets.append(set(postings.keys()))
            else:
                print("Error: postings is not a dictionary. It is:", type(postings), postings)
                return []  # Return an empty result instead of crashing

            # compute idf
            df = len(postings)
            idf = math.log((total_docs + 1) / (df + 1))

            # compute tf-idf for each doc
            for doc_id, (tf, url) in postings.items():
                tf_idf_score = (1 + math.log(tf)) * idf
                doc_tfidf[doc_id] = doc_tfidf.get(doc_id, 0) + tf_idf_score
                doc_urls[doc_id] = url  # store url
        else:
            return []  # If any token is not found, return empty list

    # Perform intersection (AND) of document sets
    if not doc_sets:
        return []

    result_docs = set.intersection(*doc_sets)

    # rank results by tf idf and return top K (5) urls
    ranked_results = sorted(result_docs, key=lambda doc: doc_tfidf.get(doc, 0), reverse=True)[:top_k]
    return [doc_urls[doc_id] for doc_id in ranked_results if doc_id in doc_urls]


def search(query):
    """
    main function to evaluate search
    """
    
    index_file = 'index.json'
    inverted_index = load_index(index_file)

    # Perform Boolean retrieval for the query
    start_time = time.time()
    results = boolean_retrieval(query, inverted_index)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    print(f"{response_time}")
    if results:
        print("Top results:")
        for url in results:
            print(url)
    else:
        print("No documents found for the query.")

# use this for testing


if __name__ == "__main__":
    index = load_index()
    while True:
        query = input("enter query using Boolean values and exit if 'exit' is input")
        if query == "exit":
            break
        print(search(query))
    # print / return documents matching queries
