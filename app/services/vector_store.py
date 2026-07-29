import chromadb
from sentence_transformers import SentenceTransformer

# Initialize Sentence Transformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize local Vector Database (ChromaDB)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="internship_embeddings")

def add_internship_to_db(internship_id: str, title: str, description: str, skills: str):
    text_to_embed = f"{title} - {description} - Skills: {skills}"
    vector = model.encode(text_to_embed).tolist()
    
    collection.upsert(
        ids=[internship_id],
        embeddings=[vector],
        documents=[text_to_embed],
        metadatas=[{"title": title, "skills": skills}]
    )

def semantic_search_internships(candidate_skills: list, n_results: int = 3):
    query_text = " ".join(candidate_skills)
    query_vector = model.encode(query_text).tolist()
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results
    )
    return results