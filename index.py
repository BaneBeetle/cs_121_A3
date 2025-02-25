import os
import json
import re
import sys
import nltk
from nltk.corpus import words
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

# Download required NLTK data and initialize objects
nltk.download('words', quiet=True)
WORD_SET = set(words.words())
PS = PorterStemmer()

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9']+")


BASE_PATH = r"C:\Users\lolly\OneDrive\Desktop\Projects\CS121\A3\cs_121_A3\.gitignore\DEV"

def tokenize(text):

    tokens = TOKEN_PATTERN.findall(text)
    result = []
    for token in tokens:
        token = token.replace("'", "").lower()
        if token in WORD_SET:
            result.append(PS.stem(token))
    return result

def process_file(file_info):

    file_path, doc_id, base_path = file_info
    partial_index = defaultdict(int)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        soup = BeautifulSoup(json_data["content"], 'lxml')

        normal_text = soup.get_text(" ", strip=True)
        normal_tokens = tokenize(normal_text)

        important_tags = soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'title'])
        important_text = " ".join(tag.get_text(" ", strip=True) for tag in important_tags)
        important_tokens = tokenize(important_text)
        
        # Count tokens; give extra weight (e.g., +2) for important tokens
        for token in normal_tokens:
            partial_index[token] += 1
        for token in important_tokens:
            partial_index[token] += 2
        
        result = {token: (freq, {doc_id}) for token, freq in partial_index.items()}
        rel_path = os.path.relpath(file_path, base_path)
        print(f"Finished processing: {rel_path} with ID: {doc_id}")
        return result, doc_id, rel_path
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {}, None, None

def writer(index, filename="index.txt"):
    """Write the inverted index to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        for token, (freq, doc_ids) in index.items():
            line = f"{token} {freq} {' '.join(map(str, doc_ids))}\n"
            f.write(line)

def indexer():
    # Gather all JSON file paths with their assigned document IDs
    file_list = []
    doc_id = 0
    url_map = {}
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                file_list.append((file_path, doc_id, BASE_PATH))

                url_map[doc_id] = os.path.relpath(file_path, BASE_PATH)
                doc_id += 1

    global_index = defaultdict(lambda: [0, set()])  # token -> [frequency, set(doc_ids)]
    document_counter = doc_id

    # Use ProcessPoolExecutor to parallelize file processing
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_file, info) for info in file_list]
        for future in as_completed(futures):
            partial_index, file_id, _ = future.result()
            if file_id is None:
                continue 
            for token, (freq, doc_ids) in partial_index.items():
                global_index[token][0] += freq
                global_index[token][1].update(doc_ids)


    final_index = {token: (freq, list(doc_ids)) for token, (freq, doc_ids) in global_index.items()}

    index_size_bytes = sys.getsizeof(final_index)
    index_size_kb = index_size_bytes / 1024
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(f"Unique Tokens: {len(final_index)}\n")
        f.write(f"Number of Documents: {document_counter}\n")
        f.write(f"Index size on disk: {index_size_bytes} bytes ({index_size_kb:.2f} KB)\n")

    return final_index

if __name__ == "__main__":
    idx = indexer()
    writer(idx)
