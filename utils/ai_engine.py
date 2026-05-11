import google.generativeai as genai
import os

from dotenv import load_dotenv

# =========================================
# LOAD ENV
# =========================================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# =========================================
# GEMINI CONFIG
# =========================================
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# =========================================
# ASK AI
# =========================================
def ask_ai(question, context, history):

    prompt = f"""
    You are TICKET-AI,
    an AI telecom KPI and ticket analytics assistant.

    Responsibilities:
    - Analyze telecom ticket data
    - Explain KPI trends
    - Analyze SLA degradation
    - Provide operational recommendations
    - Answer professionally

    Conversation history:
    {history}

    Retrieved context:
    {context}

    User question:
    {question}
    """

    response = model.generate_content(prompt)

    return response.text