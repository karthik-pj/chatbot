from services.embedding_service import get_embedding
from vector_store.chroma_client import chroma_client

def retrieve_context(query, top_k=5):
    query_embedding = get_embedding(query)
    collection = chroma_client.get_collection()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"is_active": True}
    )
    
    if not results['documents'] or not results['documents'][0]:
        return []
        
    return results['documents'][0]
