// Interface to structure the response from Flask
function performSearch() {
    var query = document.getElementById('searchInput').value;
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
    // make a request to Flask backend
    fetch("http://127.0.0.1:5000/search?query=".concat(encodeURIComponent(query)))
        .then(function (response) { return response.json(); })
        .then(function (data) {
        if (data.error) {
            if (errorMessage)
                errorMessage.textContent = data.error;
            return;
        }
        displayResults(data.results);
    })
        .catch(function (error) {
        if (errorMessage)
            errorMessage.textContent = "An error occurred during the search.";
        console.error('Error:', error);
    });
}
function displayResults(results) {
    var resultsDiv = document.getElementById('results');
    if (resultsDiv) {
        if (results.length === 0) {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        }
        else {
            resultsDiv.innerHTML = results.map(function (result) { return "\n                <div class=\"result\">\n                    <h3>".concat(result.term, "</h3>\n                    <p>Frequency: ").concat(result.frequency, "</p>\n                    <p>Found in documents: ").concat(result.documents.join(', '), "</p>\n                </div>\n            "); }).join('');
        }
    }
}
