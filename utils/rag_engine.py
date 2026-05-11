import pandas as pd

from langchain_core.documents import Document

from langchain_chroma import Chroma

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

# =========================================
# EMBEDDING MODEL
# =========================================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================
# CHROMA VECTOR DATABASE
# =========================================
vector_db = Chroma(
    collection_name="ticket_ai",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)

# =========================================
# DATAFRAME → DOCUMENTS
# =========================================
def dataframe_to_documents(df):

    documents = []

    for idx, row in df.iterrows():

        content = f"""
Telecom KPI Record

Year: {row['Year']}
Month: {row['Month']}

Area: {row['Area']}
Regional: {row['Regional']}
NOP: {row['NOP']}

Total Tickets: {row['Total_Tickets']}
Total Incident: {row['Total_Incident']}
Total Event: {row['Total_Event']}

Incident Takeover: {row['Total_Incident_Takeover']}
Event Takeover: {row['Total_Event_Takeover']}

Incident Visit: {row['Total_Incident_Visit']}
Event Visit: {row['Total_Event_Visit']}
"""

        doc = Document(
            page_content=content,
            metadata={
                "row": idx,
                "regional": row["Regional"],
                "area": row["Area"]
            }
        )

        documents.append(doc)

    return documents

# =========================================
# STORE DOCUMENTS
# =========================================
def store_documents(documents):

    vector_db.add_documents(documents)

# =========================================
# SEARCH DOCUMENTS
# =========================================
def search_documents(query, k=5):

    results = vector_db.similarity_search(
        query,
        k=k
    )

    return results