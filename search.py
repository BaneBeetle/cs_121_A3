# Implements Boolean retrieval (Milestone 2)

import json
import math
from index import tokenize
import time
from gpt2 import summarize
from simhash import Simhash

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
    for token in query_tokens:
        postings = inverted_index.get(token)
        if not postings:
            return []
        doc_sets.append(set(postings.keys()))
        df = len(postings)
        idf = math.log((total_docs + 1) / (df + 1))
        for doc_id, (tf, url) in postings.items():
            doc_tfidf[doc_id] = doc_tfidf.get(doc_id, 0) + (1 + math.log(tf)) * idf
            doc_urls[doc_id] = url
    if not doc_sets:
        return []
    result_docs = set.intersection(*sorted(doc_sets, key=len))
    ranked_results = sorted(result_docs, key=lambda doc: doc_tfidf.get(doc, 0), reverse=True)
    final_results = [{"url": doc_urls[doc_id]} for doc_id in ranked_results if doc_id in doc_urls]
    from simhash import Simhash
    unique_results = []
    simhashes = []
    for result in final_results:
        s = Simhash(result["url"])
        if any(s.distance(prev) < 13 for prev in simhashes):
            continue
        unique_results.append(result)
        simhashes.append(s)
        if len(unique_results) == top_k:
            break
    return unique_results



def search(query, inverted_index):
    """
    main function to evaluate search
    """

    # Perform Boolean retrieval for the query
    start_time = time.time()
    results = boolean_retrieval(query, inverted_index)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    print(f"Boolean Retrieval {response_time}")

    if results:
        gpt_start = time.time()
        print("Top results:")
        top_5_urls = [result['url'] for result in results]
        print(top_5_urls)
        
        # Get summaries using GPT for all URLs in one API call
        try:
            
            summaries = summarize(top_5_urls)
            if not isinstance(summaries, list) or len(summaries) != len(top_5_urls):
                raise ValueError("Invalid summary format or incorrect number of summaries")

            print(f"Summaries: {summaries}")  # Debugging summaries
        except Exception as e:
            print(f"Error during summarization: {e}")
            summaries = [{"response": "Summary not available"}] * len(top_5_urls)

        # Add summaries to the results
        for i, result in enumerate(results):
            result['summary'] = summaries[i].get('response', 'Summary not available')

        for result in results:
            print(f"URL: {result['url']}\nSummary: {result['summary']}\n")
        gpt_end = time.time()
        return results, response_time
    else:
        print("No documents found for the query.")
        return []

# use this for testing


if __name__ == "__main__":
    index = load_index()
    while True:
        query = input("enter query using Boolean values and exit if 'exit' is input")
        if query == "exit":
            break
        print(search(query))
    # print / return documents matching queries
