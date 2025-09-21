import os
import re
from dotenv import load_dotenv
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from db_config import get_postgres_conn, get_chroma_client

# -------------------- Environment --------------------
load_dotenv()
os.environ["HF_HOME"] = "D:/huggingface"  # HuggingFace cache path

# -------------------- Load CPU model --------------------
MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

generator = pipeline(
    task="text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1  # CPU
)

llm = HuggingFacePipeline(pipeline=generator, verbose=True)

# -------------------- SQL Prompt --------------------
sql_prompt = PromptTemplate(
    template="""
You are an AI assistant that writes valid PostgreSQL queries ONLY.
Database table: argo_profiles
Columns: PLATFORM_NUMBER, CYCLE_NUMBER, JULD, n_measurements,
         pres_min, pres_max, temp_min, temp_max, temp_mean,
         psal_min, psal_max, psal_mean, lat, lon, data_mode

Examples:
Q: Show average salinity near the equator in March 2025
SQL: SELECT AVG(psal_mean) FROM argo_profiles WHERE lat BETWEEN -1 AND 1 AND JULD BETWEEN '2025-03-01' AND '2025-03-31';

Q: Show minimum pressure recorded
SQL: SELECT MIN(pres_min) FROM argo_profiles;

Question: {question}

⚠️ Important: Return a single valid SQL query only. Do not add explanations.
""",
    input_variables=["question"]
)

sql_chain = sql_prompt | llm

# -------------------- Column Mapping --------------------
COLUMN_MAP = {
    "juld": '"JULD"',
    "julday": '"JULD"',
    "n_measurement": '"n_measurements"',
    "platform": '"PLATFORM_NUMBER"',
    "cycle_number": '"CYCLE_NUMBER"',
    "pres_min": '"pres_min"',
    "pres_max": '"pres_max"',
    "temp_min": '"temp_min"',
    "temp_max": '"temp_max"',
    "temp_mean": '"temp_mean"',
    "psal_min": '"psal_min"',
    "psal_max": '"psal_max"',
    "psal_mean": '"psal_mean"',
    "lat": '"lat"',
    "lon": '"lon"',
    "data_mode": '"data_mode"'
}

def fix_sql_columns(sql_query: str) -> str:
    """Replace columns with proper quoted names, case-insensitive"""
    for wrong, correct in COLUMN_MAP.items():
        sql_query = re.sub(rf'\b{wrong}\b', correct, sql_query, flags=re.IGNORECASE)
    return sql_query

def fix_juld_dates(sql_query: str) -> str:
    """Ensure JULD BETWEEN dates are properly quoted"""
    pattern = r'("JULD") BETWEEN (\S+) AND (\S+)'
    match = re.search(pattern, sql_query)
    if match:
        col, start, end = match.groups()
        if not start.startswith("'"):
            start = f"'{start}'"
        if not end.startswith("'"):
            end = f"'{end}'"
        sql_query = re.sub(pattern, f'{col} BETWEEN {start} AND {end}', sql_query)
    return sql_query

# -------------------- Simple caching --------------------
CACHE = {}

# -------------------- Postgres Query --------------------
def query_postgres(nl_question: str):
    if nl_question in CACHE:
        return CACHE[nl_question]

    conn = get_postgres_conn()
    if not conn:
        return "❌ Could not connect to PostgreSQL"

    sql_query = sql_chain.invoke({"question": nl_question}).strip()
    sql_query = fix_sql_columns(sql_query)
    sql_query = fix_juld_dates(sql_query)

    # Limit results for speed
    if "limit" not in sql_query.lower():
        sql_query += " LIMIT 1000"

    print("Generated SQL:", sql_query)

    try:
        with conn.cursor() as cur:
            cur.execute(sql_query)
            rows = cur.fetchall()
        conn.close()

        if not rows or all(r[0] is None for r in rows):
            result = "ℹ️ Query executed successfully but returned no data."
        else:
            result = rows

        CACHE[nl_question] = result
        return result
    except Exception as e:
        return f"❌ Error executing query: {e}"

# -------------------- Chroma Query --------------------
def query_chroma(nl_question: str):
    if nl_question in CACHE:
        return CACHE[nl_question]

    client = get_chroma_client()
    if not client:
        return "❌ Could not connect to Chroma"

    collection_name = "argo_metadata"
    if collection_name not in [c.name for c in client.list_collections()]:
        collection = client.create_collection(collection_name)
    else:
        collection = client.get_collection(collection_name)

    # Pre-cache sample docs if empty
    if len(collection.get(include=["documents"])["documents"]) == 0:
        collection.add(
            documents=["Sample document 1", "Sample document 2"],
            metadatas=[{"source": "test1"}, {"source": "test2"}],
            ids=["doc1", "doc2"]
        )

    try:
        results = collection.query(query_texts=[nl_question], n_results=3)
        CACHE[nl_question] = results
        return results
    except Exception as e:
        return f"❌ Error querying Chroma: {e}"

# -------------------- Test Run --------------------
if __name__ == "__main__":
    question = "Show me average salinity near the equator in March 2025"
    print("Postgres result:", query_postgres(question))
    print("Chroma result:", query_chroma(question))
