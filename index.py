# index.py: Builds and stores the inverted index (milestone 1)

import os
import json
import sys
import nltk
from nltk.corpus import words
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

nltk.download('words', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
WORD_SET = set(words.words())

PS = PorterStemmer()

# Adjust your base path here
#BASE_PATH = r"/Users/galilearuiz/Desktop/uci/inf141/Assignment3/DEV"

BASE_PATH = r"C:\\Users\\lolly\\OneDrive\Desktop\\Projects\\CS121\A3\\cs_121_A3\\DEV"

from nltk.tokenize import word_tokenize

def tokenize(text): # Sigh, removed my part A
    tokens = word_tokenize(text)
    return [PS.stem(token.lower()) for token in tokens if token.isalnum()]

def process_file(file_info):
    """
    Process a single JSON file and return:
      - partial_index: dict mapping token -> (frequency, {doc_id})
      - doc_id: the document id assigned
      - rel_path: file’s relative path (for URL mapping)
    """
    file_path, doc_id, base_path = file_info
    partial_index = defaultdict(int)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # extract url
        url = json_data.get("url", f"file://{file_path}")  # Default to local path if no URL

        # Use lxml parser for faster processing (install lxml if not already)
        soup = BeautifulSoup(json_data["content"], 'lxml')

        # Normal text tokens
        normal_text = soup.get_text(" ", strip=True)
        normal_tokens = tokenize(normal_text)

        # Extract important text tokens from designated tags
        important_tags = soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'title'])
        important_text = " ".join(tag.get_text(" ", strip=True) for tag in important_tags)
        important_tokens = tokenize(important_text)
        
        # Count tokens; give extra weight (e.g., +2) for important tokens
        for token in normal_tokens:
            partial_index[token] += 1
        for token in important_tokens:
            partial_index[token] += 2
        
        # Convert to the format: {token: {doc_id: (frequency, url)}}
        # result = {token: (freq, {doc_id}) for token, freq in partial_index.items()}
        final_index = {token: {doc_id: (partial_index[token], url)} for token in partial_index}

        rel_path = os.path.relpath(file_path, base_path)
        print(f"Finished processing: {rel_path} with ID: {doc_id}")
        return final_index, doc_id, rel_path

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {}, None, None

def writer(index, filename="index.json"):  # storing everything using JSON might be more space efficient
    """Write the inverted index to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

def indexer():
    # Gather all JSON file paths with their assigned document IDs
    file_list = []
    doc_id = 0
    # url_map = {} <- removed since urls are in index.json

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                file_list.append((file_path, doc_id, BASE_PATH))
                # Store relative path for reference
                # url_map[doc_id] = os.path.relpath(file_path, BASE_PATH)
                doc_id += 1

    global_index = defaultdict(dict)  # (lambda: [0, set()])  # token -> [frequency, set(doc_ids)]
    document_counter = doc_id

    # Use ProcessPoolExecutor to parallelize file processing
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_file, info) for info in file_list]
        for future in as_completed(futures):
            partial_index, file_id, _ = future.result()
            if file_id is None:
                continue  # skip files that caused errors

            # Merge partial index into global index
            for token, postings in partial_index.items():
                if token not in global_index:
                    global_index[token] = {}
                global_index[token].update(postings)  # merges per-token doc_id mappings


    # Report index size and document count --- Used for M1
    index_size_bytes = sys.getsizeof(global_index)
    index_size_kb = index_size_bytes / 1024
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(f"Unique Tokens: {len(global_index)}\n")
        f.write(f"Number of Documents: {document_counter}\n")
        f.write(f"Index size on disk: {index_size_bytes} bytes ({index_size_kb:.2f} KB)\n")

    return global_index

if __name__ == "__main__":
    invert_index = indexer()
    writer(invert_index)
