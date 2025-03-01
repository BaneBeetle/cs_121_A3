// Interface to structure the response from Flask

interface SearchResult {
    term: string;
    frequency: number;
    documents: number[];
}

document.getElementById('search-form')?.addEventListener('submit', function (event) {
    event.preventDefault();  // prevents form from refreshing when u submit
    performSearch();
});

function performSearch(): void {
    const query = (document.getElementById('query') as HTMLInputElement).value;
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
    const startTime = performance.now();
    // make a request to Flask backend
    fetch(`http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const endTime = performance.now();  // End timer
            const responseTime = (endTime - startTime).toFixed(2);

            if (data.error) {
                if (errorMessage) errorMessage.textContent = data.error;
                return;
            }
            displayResults(data.results, responseTime);
        })
        .catch(error => {
            if (errorMessage) errorMessage.textContent = "An error occurred during the search.";
            console.error('Error:', error);
        });
}

function displayResults(results: string[], responseTime: string): void {
    const resultsDiv = document.getElementById('results');
    if (resultsDiv) {
        if (results.length === 0) {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        } else {
            resultsDiv.innerHTML = `<p>Response Time: ${responseTime} ms</p>` + results.map(url => `
            <div class="result">
                    <a href="${url}" target="_blank">${url}</a>
            </div>  
            `).join('');
        }
    }
}
// <div class="result">
//                     <h3>${result.term}</h3>
//                     <p>Frequency: ${result.frequency}</p>
//                     <p>Found in documents: ${result.documents.join(', ')}</p>
//                 </div>
