// Interface to structure the response from Flask

interface SearchResult {
    term: string;
    frequency: number;
    documents: number[];
}

function performSearch(): void {
    const query = (document.getElementById('searchInput') as HTMLInputElement).value;
    const errorMessage = document.getElementById('errorMessage');
    const resultsDiv = document.getElementById('results');

    // clear previous results
    if (resultsDiv) resultsDiv.innerHTML = '';
    if (errorMessage) errorMessage.innerHTML = '';

    // basic validation for query
    if (!query.trim()) {
        if (errorMessage) errorMessage.textContent = "Please enter a search term.";
        return;
    }

    // make a request to Flask backend
    fetch(`http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                if (errorMessage) errorMessage.textContent = data.error;
                return;
            }
            displayResults(data.results);
        })
        .catch(error => {
            if (errorMessage) errorMessage.textContent = "An error occurred during the search.";
            console.error('Error:', error);
        });
}

function displayResults(results: SearchResult[]): void {
    const resultsDiv = document.getElementById('results');
    if (resultsDiv) {
        if (results.length === 0) {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        } else {
            resultsDiv.innerHTML = results.map(result => `
                <div class="result">
                    <h3>${result.term}</h3>
                    <p>Frequency: ${result.frequency}</p>
                    <p>Found in documents: ${result.documents.join(', ')}</p>
                </div>
            `).join('');
        }
    }
}
