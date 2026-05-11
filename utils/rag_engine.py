import chromadb
import uuid

# =========================================
# CHROMA CLIENT
# =========================================
client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="ticket_knowledge"
)

# =========================================
# STORE DOCUMENT
# =========================================
def store_document(text):

    doc_id = str(uuid.uuid4())

    collection.add(
        documents=[text],
        ids=[doc_id]
    )

# =========================================
# SEARCH DOCUMENTS
# =========================================
def search_documents(query, n_results=3):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results["documents"][0]

    return documents