from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import json
import os
import numpy as np
from flask_cors import CORS
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

app = Flask(__name__)
CORS(app)  # Enable CORS if your frontend is on a different domain

# Initialize BERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')

# Load the FAISS index
index_loaded = faiss.read_index("sample_code.index")

# Load data to map indices to documents
data_file_path = 'dataset.json'
index_doc = {}
try:
    with open(data_file_path, 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)
        for idx, item in enumerate(data[:500]):  # Assuming you want to map the same items
            body_text = item.get("body", "").strip()
            if body_text:
                index_doc[idx] = body_text
except Exception as e:
    print(f"There was an exception: {str(e)}")

def convert_to_embedding(query):
    tokens = tokenizer.encode_plus(query, max_length=512, truncation=True, padding='max_length', return_tensors='pt')
    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state
    attention_mask = tokens['attention_mask']
    mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, 1)
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)
    mean_pooled = summed / summed_mask
    return mean_pooled[0].cpu().numpy()  # Convert to numpy array for FAISS

@app.route('/process_query', methods=['POST'])
def process_query():
    data = request.json
    query = data.get('query')
    query_embedding = convert_to_embedding(query)
    D, I = index_loaded.search(np.array([query_embedding]), 10)  # Search for top 10 closest embeddings
    
    # Retrieve documents corresponding to the closest embeddings
    results = [index_doc[idx] for idx in I[0] if idx in index_doc]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
