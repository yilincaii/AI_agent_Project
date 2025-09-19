import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATEHR_API_KEY = os.getenv("OPENWEATEHR_API_KEY")
TODOLIST_API_KEY = os.getenv("TODOLIST_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

FULL_AI_TRACE = False
