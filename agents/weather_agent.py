from langgraph.prebuilt import create_react_agent
from tools.weather_tool import get_weather

def create_weather_agent(llm):
    return create_react_agent(
        model = llm, 
        tools = [get_weather],
        prompt = (
            "You are a weather agent.\n\n"
            "INSTRUCTIONS:\n"
            "- Assist only with weather related tasks.\n"
            "- Extract the location from the users prompt\n"
            "- Make sure you use the tools that you have provided to you.\n"
            "- Once you have the weather information, respond with the details and then indicate you are transferring back to the supervisor with the 'FINAL ANSWER'."
        ),
        name = "weather_agent"
    )