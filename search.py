# Implements Boolean retrieval (Milestone 2)

import json
from index import tokenize

def load_index(index_file = 'index.json'):
    ''' Load the inverted index from the disk '''
    # idea for performance boost? memory-mapped files (idk gpt said so)
    with open(index_file, 'r', encoding='utf-8') as file:
        inverted_index = json.load(file)
        return inverted_index


def boolean_retrieval(query, inverted_index):
    """
        Process a Boolean query using the inverted index.
        Should support AND operations.
        """

    query_tokens = tokenize(query)
    doc_sets = []

    # for each token, get the list of documents
    for token in query_tokens:
        if token in inverted_index:
            doc_sets.append(set(inverted_index[token]))  # Store document IDs as a set
        else:
            return []  # If any token is not found, return empty list

    # Perform intersection (AND) of document sets
    result_docs = set.intersection(*doc_sets)
    return result_docs

def search(query):
    '''
    main function to evaluate boolean search
    '''
    index_file = 'index.json'
    inverted_index = load_index(index_file)

    # Perform Boolean retrieval for the query
    result_docs = boolean_retrieval(query, inverted_index)

    if result_docs:
        print("Documents found:")
        for doc_id in result_docs:
            print(f"Document ID: {doc_id}")
    else:
        print("No documents found for the query.")

# use this for testing

# if __name__ == "__main__":
    # index = load_index()
    # while True:
    # enter query using Boolean values and exit if 'exit' is input
    # process_query
    # print / return documents matching queries