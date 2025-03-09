// Interface to structure the response from Flask
var _a, _b;
(_a = document.getElementById('search-form')) === null || _a === void 0 ? void 0 : _a.addEventListener('submit', function (event) {
    event.preventDefault(); // prevents form from refreshing when u submit
    performSearch();
});
(_b = document.getElementById('summary-toggle')) === null || _b === void 0 ? void 0 : _b.addEventListener('change', function () {
    if (this.checked) {
        displaySummaries(true);
    }
    else {
        displaySummaries(false);
    }
});
var currentResults = [];
function performSearch() {
    var query = document.getElementById('query').value;
    var errorMessage = document.getElementById('errorMessage');
    var resultsDiv = document.getElementById('results');
    var searchTimeDisplay = document.getElementById('search-time');
    var searchWithSummaryTimeDisplay = document.getElementById('search-with-summary-time');
    // clear previous results
    if (resultsDiv)
        resultsDiv.innerHTML = '';
    if (errorMessage)
        errorMessage.innerHTML = '';
    if (searchTimeDisplay)
        searchTimeDisplay.innerHTML = '';
    if (searchWithSummaryTimeDisplay)
        searchWithSummaryTimeDisplay.innerHTML = '';
    // basic validation for query
    if (!query.trim()) {
        if (errorMessage)
            errorMessage.textContent = "Please enter a search term.";
        return;
    }
    var startTime = performance.now();
    // make a request to Flask backend
    fetch("http://127.0.0.1:5000/search?query=".concat(encodeURIComponent(query)))
        .then(function (response) { return response.json(); })
        .then(function (data) {
        var endTime = performance.now(); // End timer
        var responseTime = (endTime - startTime);
        var adjustedTime = (responseTime - data.gpt_time).toFixed(2); // gpt_time represents total time during summary creation
        if (data.error) {
            if (errorMessage)
                errorMessage.textContent = data.error;
            return;
        }
        console.log("Search Results:", data); // Debugging log
        displayResults(data.results, adjustedTime, responseTime);
    })
        .catch(function (error) {
        if (errorMessage)
            errorMessage.textContent = "An error occurred during the search.";
        console.error('Error:', error);
    });
}
function displayResults(result, responseTime, fulltime) {
    var resultsDiv = document.getElementById('results');
    var searchWithSummaryTimeDisplay = document.getElementById('search-with-summary-time');
    if (resultsDiv) {
        if (result.length === 0) {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        }
        else {
            resultsDiv.innerHTML = "<p>Search Time: ".concat(responseTime, " ms</p>") + result.map(function (result) { return "\n            <div class=\"result\">\n                    <a href=\"".concat(result.url, "\" target=\"_blank\">").concat(result.url, "</a>\n                    <p>").concat(result.summary, "</p>\n            </div>  \n            "); }).join('');
        }
    }
    if (searchWithSummaryTimeDisplay) {
        searchWithSummaryTimeDisplay.innerHTML = "Search + GPT Summaries Time: ".concat(fulltime, " ms");
    }
}
function displaySummaries(show) {
    var resultsDiv = document.getElementById('results');
    if (resultsDiv) {
        resultsDiv.innerHTML = currentResults.map(function (res) { return "\n        <div class=\"result-item\">\n            <a href=\"".concat(res.url, "\" target=\"_blank\">").concat(res.url, "</a>\n            <p>").concat(show ? res.summary : "Summary hidden", "</p>\n        </div>  \n        "); }).join('');
    }
}
