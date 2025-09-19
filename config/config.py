import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

FULL_AI_TRACE = False