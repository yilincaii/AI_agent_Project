# weather_tool.py
from typing import Dict, Any

def get_weather_placeholder() -> Dict[str, Any]:
    return {"event": "weather", "error": "weather provider not configured yet"}
