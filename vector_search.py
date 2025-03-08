import os
import openai
import pinecone
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = pinecone.Pinecone(api_key=pinecone_api_key)
index = pc.Index("legal-assistant")


def search_law(question):
    query_vector = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=question
    ).data[0].embedding

    results = index.query(vector=query_vector, top_k=3, include_metadata=True)

    if results.matches:
        return results.matches[0].metadata["content"]

    return "No relevant legal text found."
