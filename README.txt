Galilea Ruiz
Brian Phan

How to Run:
1. Run main.py
2. Once you have ran main.py, search in your folders for "frontend" and double click index.html
3. Once you have launched our front end, type your desired query in the search bar.


Dependencies:
- Python            
- openai            -- For interacting with the GPT API (used in gpt2.py) NOTE: if you wan't to run this locally you NEED an API Key
- python-dotenv     -- To load environment variables from a .env file (used in gpt.py)
- nltk              -- For natural language processing (used in index.py)
- beautifulsoup4    -- For HTML parsing (used in index.py)
- lxml              -- For faster HTML parsing with BeautifulSoup (used in index.py)
- simhash           -- For document similarity (used in index.py)
- flask             -- For the backend server (used in main.py)
- flask-cors        -- To handle CORS in the Flask application (used in main.py)


How to create an Inverted Index:
- Run index.py and modify BasePaths if needed.
