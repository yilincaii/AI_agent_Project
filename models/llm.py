import os
from lanchain_groq import CHatGroq
from config.config import GROQ_API_KEY

def get_llm():
    return CHatGroq(
        model = "llama-3.3-70b-versatile",
        groq_api_key = GROQ_API_KEY,
        temperature=0.7
    )