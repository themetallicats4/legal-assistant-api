import os
import openai
import pinecone
from dotenv import load_dotenv
from vector_search import search_law

load_dotenv()

# Initialize Pinecone
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = pinecone.Pinecone(api_key=pinecone_api_key)
index = pc.Index("legal-assistant")

if __name__ == "__main__":
    user_question = input("Bir soru sorun: ")
    best_match = search_law(user_question)
    print(f"📜 **Hukuki Açıklama:**\n{best_match}")
