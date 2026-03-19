from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """Returns the embedding for a single string"""
    embedding = model.encode(text)
    return embedding.tolist()

def get_embeddings(texts):
    """Returns embeddings for a list of strings"""
    embeddings = model.encode(texts)
    return embeddings.tolist()
