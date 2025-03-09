# main.py backend server to handle searches using Flask

from flask import Flask, request, jsonify
from search import search, load_index
from flask_cors import CORS
import time
from gpt2 import summarize

app = Flask(__name__)
CORS(app)


# load inverted index into memory when server starts
try:
    inverted_index = load_index('index.json')
except Exception as e:
    print(f"Error loading index: {e}")
    inverted_index = {}


@app.route('/search', methods=['GET'])
def search_query():
    query = request.args.get('query', '')  # get query from front end
    if not query:
        return jsonify({"error": "No search term provided"}), 400
    print(f"Received search query: {query}")

#    print("First 20 words in the inverted index:", list(inverted_index.keys())[:20])
#    print("Checking inverted index for query terms:", query)
#    for term in query.split():
 #       if term in inverted_index:
 #           print(f"Term '{term}' exists in the index with {len(inverted_index[term])} postings.")
 #       else:
 #           print(f"Term '{term}' is NOT in the index.")
# debugging ^^^


    start_time = time.time()

    # Perform Boolean retrieval with tf-idf ranking
    try:
        results, gpt_time = search(query, inverted_index)

        print(f"Received results: {results}")
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        if not results:
            return jsonify({"error": "No results found"}), 404
        print(f"Search query: '{query}', Response time: {response_time:.2f} ms")

        #top_5_urls = [result['url'] for result in results[:5]]

        #summaries = summarize(top_5_urls)

        #for i, result in enumerate(results[:5]):
        #    result['summary'] = summaries[i].get('response', 'Summary not available')

        #print(f"Results with summaries: {results[:5]}")
 
        return jsonify({"results": results[:5], "gpt_time": gpt_time * 1000})


    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
