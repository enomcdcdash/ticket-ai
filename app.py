import streamlit as st
import pandas as pd

from utils.analytics import (
    get_basic_kpi,
    get_top_regional,
    get_incident_analysis,
    get_event_analysis,
    get_takeover_analysis,
    get_visit_analysis
)

from utils.ai_engine import ask_ai

from utils.rag_engine import (
    dataframe_to_documents,
    store_documents,
    search_documents
)

from utils.database import (
    save_dataframe,
    load_dataframe
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
# SESSION STATE
# =========================================
if "history" not in st.session_state:

    st.session_state.history = []

# =========================================
# TITLE
# =========================================
st.title("📊 TICKET-AI")

st.subheader(
    "AI-Powered Telecom KPI Analytics Assistant"
)

# =========================================
# SIDEBAR
# =========================================
st.sidebar.title("Dataset Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload KPI Dataset",
    type=["xlsx", "xls"]
)

# =========================================
# LOAD EXISTING DATASET
# =========================================
try:

    df = load_dataframe()

    data_loaded = True

except:

    data_loaded = False

# =========================================
# PROCESS NEW UPLOAD
# =========================================
if uploaded_file:

    df = pd.read_excel(uploaded_file)

    save_dataframe(df)

    data_loaded = True

    st.sidebar.success(
        "Dataset saved successfully"
    )

# =========================================
# MAIN APPLICATION
# =========================================
if data_loaded:

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

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Tickets",
        f"{summary['total_tickets']:,.0f}"
    )

    col2.metric(
        "Total Incident",
        f"{summary['total_incident']:,.0f}"
    )

    col3.metric(
        "Total Event",
        f"{summary['total_event']:,.0f}"
    )

    col4.metric(
        "Total Area",
        summary["total_area"]
    )

    col5.metric(
        "Total Regional",
        summary["total_regional"]
    )

    # =====================================
    # TOP REGIONAL ANALYSIS
    # =====================================
    st.subheader("Top Regional Ticket Volume")

    regional_chart = create_bar_chart(
        get_top_regional(df),
        "Top Regional Ticket Volume"
    )

    st.pyplot(regional_chart)

    # =====================================
    # INCIDENT ANALYSIS
    # =====================================
    st.subheader("Incident Analysis")

    incident_chart = create_bar_chart(
        get_incident_analysis(df),
        "Incident Analysis"
    )

    st.pyplot(incident_chart)

    # =====================================
    # EVENT ANALYSIS
    # =====================================
    st.subheader("Event Analysis")

    event_chart = create_bar_chart(
        get_event_analysis(df),
        "Event Analysis"
    )

    st.pyplot(event_chart)

    # =====================================
    # TAKEOVER ANALYSIS
    # =====================================
    st.subheader("Takeover Analysis")

    takeover_chart = create_bar_chart(
        get_takeover_analysis(df),
        "Takeover Analysis"
    )

    st.pyplot(takeover_chart)

    # =====================================
    # VISIT ANALYSIS
    # =====================================
    st.subheader("Visit Analysis")

    visit_chart = create_bar_chart(
        get_visit_analysis(df),
        "Visit Analysis"
    )

    st.pyplot(visit_chart)

    # =====================================
    # BUILD VECTOR DATABASE
    # =====================================
    if "rag_loaded" not in st.session_state:

        with st.spinner(
            "Building AI Knowledge Base..."
        ):

            documents = dataframe_to_documents(df)

            # limit for performance/quota
            store_documents(documents[:500])

        st.session_state.rag_loaded = True

        st.success(
            "AI Knowledge Base Ready"
        )

    # =====================================
    # CHATBOT
    # =====================================
    st.subheader("💬 TICKET-AI Assistant")

    # =====================================
    # DISPLAY CHAT HISTORY
    # =====================================
    for message in st.session_state.history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # =====================================
    # USER INPUT
    # =====================================
    user_question = st.chat_input(
        "Ask telecom operational questions..."
    )

    # =====================================
    # PROCESS QUESTION
    # =====================================
    if user_question:

        # =================================
        # SHOW USER MESSAGE
        # =================================
        with st.chat_message("user"):

            st.markdown(user_question)

        # =================================
        # SAVE USER MESSAGE
        # =================================
        st.session_state.history.append({
            "role": "user",
            "content": user_question
        })

        # =================================
        # VECTOR SEARCH
        # =================================
        results = search_documents(
            user_question,
            k=5
        )

        context = "\n\n".join([
            doc.page_content
            for doc in results
        ])

        # =================================
        # GENERATE AI RESPONSE
        # =================================
        with st.spinner(
            "Analyzing telecom operations..."
        ):

            answer = ask_ai(
                question=user_question,
                context=context,
                history=st.session_state.history[-6:]
            )

        # =================================
        # SHOW AI RESPONSE
        # =================================
        with st.chat_message("assistant"):

            st.markdown(answer)

        # =================================
        # SAVE AI RESPONSE
        # =================================
        st.session_state.history.append({
            "role": "assistant",
            "content": answer
        })

else:

    st.info(
        "Please upload KPI dataset to begin."
    )