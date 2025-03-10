// Interface to structure the response from Flask


document.getElementById('search-form')?.addEventListener('submit', function (event) {
    event.preventDefault();  // prevents form from refreshing when u submit
    performSearch();
});

document.getElementById('summary-toggle')?.addEventListener('change', function () {
    if ((this as HTMLInputElement).checked) {
        displaySummaries(true);
    } else {
        displaySummaries(false);
    }
});

let currentResults: SearchResult[] = [];

function performSearch(): void {
    const query = (document.getElementById('query') as HTMLInputElement).value;
    const errorMessage = document.getElementById('errorMessage');
    const resultsDiv = document.getElementById('results');
    const searchTimeDisplay = document.getElementById('search-time');
    const searchWithSummaryTimeDisplay = document.getElementById('search-with-summary-time');

    // clear previous results
    if (resultsDiv) resultsDiv.innerHTML = '';
    if (errorMessage) errorMessage.innerHTML = '';
    if (searchTimeDisplay) searchTimeDisplay.innerHTML = '';
    if (searchWithSummaryTimeDisplay) searchWithSummaryTimeDisplay.innerHTML = '';

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
            const responseTime = (endTime - startTime);
            if (data.error) {
                if (errorMessage) errorMessage.textContent = data.error;
                return;
            }
            displayResults(data.results, data.search_time, responseTime);
        })


        .catch(error => {
            if (errorMessage) errorMessage.textContent = "An error occurred during the search.";
                console.error('Error:', error);
        });

}


interface SearchResult {
    url: string;
    summary: string;
}


function displayResults(result: SearchResult[], responseTime: string, fulltime:string): void {
    const resultsDiv = document.getElementById('results');
    const searchWithSummaryTimeDisplay = document.getElementById('search-with-summary-time');

    if (resultsDiv) {
        if (result.length === 0) {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        } else {
            resultsDiv.innerHTML = `<p>Search Time: ${responseTime} ms</p>` + result.map(result => `
            <div class="result">
                    <a href="${result.url}" target="_blank">${result.url}</a>
                    <p>${result.summary}</p>
            </div>  
            `).join('');
        }
    }
    if (searchWithSummaryTimeDisplay) {
        searchWithSummaryTimeDisplay.innerHTML = `Search + GPT Summaries Time: ${fulltime} ms`;
    }
}

function displaySummaries(show: boolean): void {
    const resultsDiv = document.getElementById('results');

    if (resultsDiv) {
        resultsDiv.innerHTML = currentResults.map((res: any) => `
        <div class="result-item">
            <a href="${res.url}" target="_blank">${res.url}</a>
            <p>${show ? res.summary : "Summary hidden"}</p>
        </div>  
        `).join('');
    }
}
