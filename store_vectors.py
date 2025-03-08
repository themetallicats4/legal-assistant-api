import os
import openai
import pinecone
import psycopg2
from dotenv import load_dotenv
from database import get_all_laws

load_dotenv()

# Set up API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=pinecone_api_key)
index = pc.Index("legal-assistant")

def generate_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def insert_vectors():
    laws = get_all_laws()
    for law in laws:
        law_id, title, content = law
        vector = generate_embedding(content)
        metadata = {"title": title, "content": content}
        index.upsert([(str(law_id), vector, metadata)])

    print("✅ Legal texts stored successfully in Pinecone!")

if __name__ == "__main__":
    insert_vectors()
