// Interface to structure the response from Flask
var _a;
(_a = document.getElementById('search-form')) === null || _a === void 0 ? void 0 : _a.addEventListener('submit', function (event) {
    event.preventDefault(); // prevents form from refreshing when u submit
    performSearch();
});
function performSearch() {
    var query = document.getElementById('query').value;
    var errorMessage = document.getElementById('errorMessage');
    var resultsDiv = document.getElementById('results');
    // clear previous results
    if (resultsDiv)
        resultsDiv.innerHTML = '';
    if (errorMessage)
        errorMessage.innerHTML = '';
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
        var responseTime = (endTime - startTime).toFixed(2);
        if (data.error) {
            if (errorMessage)
                errorMessage.textContent = data.error;
            return;
        }
        displayResults(data.results, responseTime);
    })
        .catch(function (error) {
        if (errorMessage)
            errorMessage.textContent = "An error occurred during the search.";
        console.error('Error:', error);
    });
}
function displayResults(results, responseTime) {
    var resultsDiv = document.getElementById('results');
    if (resultsDiv) {
        if (results.length === 0) {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        }
        else {
            resultsDiv.innerHTML = "<p>Response Time: ".concat(responseTime, " ms</p>") + results.map(function (url) { return "\n            <div class=\"result\">\n                    <a href=\"".concat(url, "\" target=\"_blank\">").concat(url, "</a>\n            </div>  \n            "); }).join('');
        }
    }
}
// <div class="result">
//                     <h3>${result.term}</h3>
//                     <p>Frequency: ${result.frequency}</p>
//                     <p>Found in documents: ${result.documents.join(', ')}</p>
//                 </div>
