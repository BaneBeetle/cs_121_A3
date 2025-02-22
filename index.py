# Brian Phan
# 84609992
# A3 Indexer

import os
import json
from bs4 import BeautifulSoup
import re
import sys
import nltk
from nltk.corpus import words

nltk.download('words')
word_list = words.words()

'''Create an inverted index for the corpus with data structures designed by you.
• Tokens: all alphanumeric sequences in the dataset.
• Stop words: do not use stopping while indexing, i.e. use all words, even
the frequently occurring ones.
• Stemming: use stemming for better textual matches. Suggestion: Porter
stemming, but it is up to you to choose.
• Important text: text in bold (b, strong), in headings (h1, h2, h3), and
in titles should be treated as more important than the in other places.
Verify which are the relevant HTML tags to select the important words.'''


base_path = "C:\\Users\\lolly\\OneDrive\\Desktop\\Projects\\CS121\\A3\\cs_121_A3\\.gitignore\\DEV"





def writer(index, filename="index.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for key, folders in index.items():
            line = f"{key} {' '.join(folders)}\n"
            f.write(line)


### Reusing A1 Code Part A with slight modifications since I got a 5.9 ###
def tokenize(sentence):
    "Tokenize them paths"

    tokens = [] # set token list

    splits = re.findall(r"[a-zA-Z0-9']+", sentence, re.UNICODE)
    for t in splits:
        # Turn words like "don't" into "dont"
        token = t.replace("'", "").lower()
        if token in word_list:
            tokens.append(token)

    return tokens

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(" ", strip=True)

def deep_getsizeof(obj, seen=None):
    """
    Recursively finds the memory footprint of an object and all of its contents. <- Found code
    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    
    if isinstance(obj, dict):
        size += sum(deep_getsizeof(k, seen) + deep_getsizeof(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_getsizeof(i, seen) for i in obj)
    
    return size

def indexer():

    index = {} # For now, we will use a dictionary but will change this later
    # Key will be token, value will be location

    url_map = {}
    map_counter = 0

    document_counter = 0
    ### Go through the folder containing JSONS, use BeautifulSoup to extract data? ###
    for root, dirs, files in os.walk(base_path):

        for file in files:

            document_counter += 1

            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                
                folder_name = os.path.relpath(file_path, base_path)
                url_map[map_counter] = folder_name

                with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)

                        extracted_words = tokenize(extract_text_from_html(json_data["content"]))

                        for word in extracted_words:
                            if word in index:
                                current_freq, folders = index[word]
                                current_freq += 1

                                if map_counter not in folders:
                                    folders.append(map_counter)

                                index[word] = (current_freq, folders)

                            else:
                                index[word] = (1, [map_counter])
    
                print("Finished processing:", folder_name, "with ID:", map_counter)
                map_counter += 1

    index_size_bytes = deep_getsizeof(index)
    index_size_kb = index_size_bytes / 1024

    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("Unique Tokens:", len(index), "\n")
        f.write("Number of Documents:", document_counter, "\n")
        f.write(f"Index size on disk: {index_size_bytes} bytes ({index_size_kb:.2f} KB)\n")


    return index

if __name__ == "__main__":
    writer(indexer())
