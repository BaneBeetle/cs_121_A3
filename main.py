# main.py backend server to handle searches using Flask

from flask import Flask, request, jsonify
from search import boolean_retrieval, load_index
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# load inverted index into memory when server starts
try:
    inverted_index = load_index('index.json')
except Exception as e:
    print(f"Error loading index: {e}")
    inverted_index = {}

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # get query from front end
    if not query:
        return jsonify({"error": "No search term provided"}), 400

    # Perform Boolean retrieval with tf-idf ranking
    results = boolean_retrieval(query, inverted_index)

    # formatted_results = []
    # for doc_id, (frequency, url) in results.items():
        # formatted_results.append({
            #"term": query,  # The search term
            #"frequency": frequency,  # The term frequency in the document
            #"documents": [url]  # Wrap the URL in an array
        #})
    return jsonify({"results": results})



if __name__ == "__main__":
    app.run(debug=True)
