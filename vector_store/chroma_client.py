import os
os.environ['ANONYMIZED_TELEMETRY'] = 'False'
import chromadb
from chromadb.config import Settings

CHROMA_DB_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data', 'chroma_db')

class ChromaDBClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaDBClient, cls).__new__(cls)
            # Ensure the directory exists
            os.makedirs(CHROMA_DB_DIR, exist_ok=True)
            cls._instance.client = chromadb.PersistentClient(
                path=CHROMA_DB_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            cls._instance.collection = cls._instance.client.get_or_create_collection(
                name="company_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
        return cls._instance

    def get_collection(self):
        return self.collection

chroma_client = ChromaDBClient()
