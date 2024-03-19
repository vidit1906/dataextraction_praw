function submitPyLucene() {
    var input = document.getElementById('pyLuceneInput').value;
    fetch('/submit_py_lucene', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: input })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('pyLuceneOutput').textContent = 'Output: ' + data.result;
    })
    .catch(error => console.error('Error:', error));
  }
  
  function submitBERT() {
    var input = document.getElementById('bertInput').value;
    fetch('/submit_bert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: input })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('bertOutput').textContent = 'Output: ' + data.result;
    })
    .catch(error => console.error('Error:', error));
  }
  