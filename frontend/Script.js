function submitPyLucene() {
  var input = document.getElementById('pyLuceneInput').value;
  fetch('/search_py_lucene', {  // This should match the Flask route
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: input })
  })
  .then(response => response.json())
  .then(data => {
    // Here you'll need to format the data as you want it to appear in the output
    document.getElementById('pyLuceneOutput').innerHTML = 'Output: ' + JSON.stringify(data, null, 2);
  })
  .catch(error => console.error('Error:', error));
}



  
function fetchQueryResults() {
  const queryInput = document.getElementById('queryInput');
  const resultsDiv = document.getElementById('results');

  const query = queryInput.value;
  if (!query) {
      alert("Please enter a query.");
      return;
  }

  resultsDiv.innerHTML = 'Loading...';

  fetch('http://localhost:5001/process_query', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: query }),
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      if (data && data.length > 0) {
          const formattedResults = data.map((item, index) => `<p>${index + 1}. ${item}</p>`).join('');
          resultsDiv.innerHTML = formattedResults;
      } else {
          resultsDiv.innerHTML = '<p>No results found.</p>';
      }
  })
  .catch((error) => {
      console.error('Error:', error);
      resultsDiv.innerHTML = '<p>Error fetching results.</p>';
  });
}
