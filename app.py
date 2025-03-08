from flask import Flask, request, jsonify
import os
import openai
import pinecone
from dotenv import load_dotenv
from database import get_law_by_id
from vector_search import search_law

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set API keys securely
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=pinecone_api_key)
index = pc.Index("legal-assistant")

@app.route('/law/<int:law_id>', methods=['GET'])
def get_law(law_id):
    """
    API endpoint to retrieve a law by its ID.
    """
    law = get_law_by_id(law_id)
    if not law:
        return jsonify({"error": "Law not found"}), 404

    return jsonify({
        "id": law[0],
        "title": law[1],
        "content": law[2]
    })

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    best_match = search_law(question)

    return jsonify({
        "question": question,
        "answer": best_match
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
