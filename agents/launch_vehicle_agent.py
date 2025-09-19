from langgraph.prebuilt import create_react_agent
from tools.launch_vehicle_tool import get_launches

def create_launch_vehicle_agent(llm):
    return create_react_agent(
        model =llm,
        tools = [get_launches],
        prompt = {
             "You are a launch vehicle agent.\n\n"
            "INSTRUCTIONS:\n"
            "- Assist only with space rocket launch vehicle related tasks.\n"
            "- Make sure you use the tools that you have provided to you.\n"
            "- Once you have the launch vehicle information, respond with the details and then indicate you are transferring back to the supervisor with the 'FINAL ANSWER'."
        }
        name = "launch_vehicle_agent",
    )