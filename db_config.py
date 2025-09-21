import os
from dotenv import load_dotenv
import psycopg2
import chromadb

# -------------------- Load env --------------------
load_dotenv()
os.environ["HF_HOME"] = "D:/huggingface"  # Ensure HF cache path

# -------------------- PostgreSQL --------------------
def get_postgres_conn():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "sih25"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "root"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432")
        )
        return conn
    except Exception as e:
        print("❌ PostgreSQL connection error:", e)
        return None

# -------------------- ChromaDB --------------------
def get_chroma_client():
    try:
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "D:/chroma_persist")
        client = chromadb.PersistentClient(path=persist_dir)
        return client
    except Exception as e:
        print("❌ ChromaDB connection error:", e)
        return None

# -------------------- Test Connections --------------------
if __name__ == "__main__":
    pg_conn = get_postgres_conn()
    if pg_conn:
        print("✅ Connected to PostgreSQL")
        pg_conn.close()
    chroma_client = get_chroma_client()
    if chroma_client:
        print("✅ Connected to ChromaDB")
