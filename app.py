import streamlit as st
import pandas as pd

from utils.analytics import (
    get_basic_kpi,
    get_top_category,
    generate_data_summary
)

from utils.ai_engine import ask_ai

from utils.rag_engine import (
    store_document,
    search_documents
)

from utils.charts import create_bar_chart

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="TICKET-AI",
    layout="wide"
)

# =========================================
# SESSION MEMORY
# =========================================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================================
# TITLE
# =========================================
st.title("📊 TICKET-AI")

st.subheader(
    "Telecom Intelligent Chatbot for KPI Evaluation and Ticket Analytics"
)

# =========================================
# SIDEBAR
# =========================================
st.sidebar.title("About")

st.sidebar.info("""
TICKET-AI is an AI-powered telecom KPI analytics assistant
using Gemini API, RAG, and ChromaDB.
""")

# =========================================
# FILE UPLOADER
# =========================================
uploaded_file = st.file_uploader(
    "Upload KPI Excel File",
    type=["xlsx", "xls"]
)

# =========================================
# MAIN APP
# =========================================
if uploaded_file:

    # =====================================
    # READ EXCEL
    # =====================================
    df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # =====================================
    # DATA PREVIEW
    # =====================================
    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    # =====================================
    # KPI SUMMARY
    # =====================================
    st.subheader("KPI Summary")

    summary = get_basic_kpi(df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Records",
        summary["total_rows"]
    )

    col2.metric(
        "Total Numeric Value",
        f"{summary['total_numeric']:,.0f}"
    )

    col3.metric(
        "Total Columns",
        len(summary["columns"])
    )

    # =====================================
    # CHART SECTION
    # =====================================
    st.subheader("Top Category Analysis")

    chart_data = get_top_category(df)

    if chart_data is not None:

        fig = create_bar_chart(chart_data)

        st.pyplot(fig)

    # =====================================
    # CREATE RAG KNOWLEDGE
    # =====================================
    dataset_summary = generate_data_summary(df)

    store_document(dataset_summary)

    # =====================================
    # CHATBOT
    # =====================================
    st.subheader("💬 AI Chatbot")

    user_question = st.text_input(
        "Ask a question about your KPI data"
    )

    if st.button("Analyze"):

        # =================================
        # RAG SEARCH
        # =================================
        retrieved_docs = search_documents(
            user_question
        )

        rag_context = "\n".join(retrieved_docs)

        # =================================
        # AI RESPONSE
        # =================================
        answer = ask_ai(
            question=user_question,
            context=rag_context,
            history=st.session_state.history
        )

        # =================================
        # SAVE HISTORY
        # =================================
        st.session_state.history.append(
            f"User: {user_question}"
        )

        st.session_state.history.append(
            f"Assistant: {answer}"
        )

        # =================================
        # DISPLAY ANSWER
        # =================================
        st.markdown("### AI Analysis")

        st.write(answer)

    # =====================================
    # HISTORY
    # =====================================
    with st.expander("Conversation History"):

        for item in st.session_state.history:
            st.write(item)