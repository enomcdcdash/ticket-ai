import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# =========================================
# GEMINI MODEL
# =========================================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3,
    google_api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

# =========================================
# ASK AI
# =========================================
def ask_ai(question, context, history):

    history_text = ""

    for msg in history:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""
You are TICKET-AI,
an advanced telecom operational intelligence assistant.

You analyze:
- telecom ticket operations
- incidents
- events
- takeover metrics
- visit metrics
- regional telecom performance

Use ONLY the provided context.

If information is unavailable,
say clearly that the dataset context is insufficient.

Conversation History:
{history_text}

Dataset Context:
{context}

User Question:
{question}

Instructions:
- Give accurate operational insights
- Be concise
- Mention numbers if available
- Avoid hallucination
"""

    response = llm.invoke(prompt)

    return response.content