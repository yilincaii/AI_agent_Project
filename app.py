import os
from typing import List

from flask import Flask, request, Response
from flask_cors import CORS
from langgraph.prebuilt import create_react_agent  
import json

# 尝试这些可能的导入路径
#from langgraph.prebuilt import create_supervisor
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from agents.math_agent import create_math_agent
from agents.poem_agent import create_poem_agent
from agents.weather_agent import create_weather_agent
from agents.launch_vehicle_agent import create_launch_vehicle_agent
from agents.todolist_agent import create_todoist_agent
from models.llm import get_llm


from tools.launch_vehicle_tool import get_launches
from tools.todolist_tools import add_task, get_task  
from tools.weather_tool import get_weather
from tools.math_tools import add, multiply, divide

app = Flask(__name__)
CORS(app)

llm_model = get_llm()

math_agent = create_math_agent(llm_model)
weather_agent = create_weather_agent(llm_model)
poem_agent = create_poem_agent(llm_model)
launch_vehicle_agent = create_launch_vehicle_agent(llm_model)
todoist_agent = create_todoist_agent(llm_model)

supervisor_prompt = (
    "You are a supervisor managing multiple agents:\n"
    "- a poem agent. Assign tasks that explicitly ask for a poem or creative writing to this agent.\n"
    "- a math agent. Assign tasks that involve calculations, numbers, or mathematical operations to this agent.\n"
    "- a weather agent. Assign tasks that involve getting weather, temperature, humidity or anything else weather related to a location\n"
    "- a launch vehicle agent. Assign tasks that involve getting details of space rocket launch vehicle events. Such as when a certain rocket is due to lift off.\n"
    "- a todoist agent. Assign tasks related to todo lists. It could be anything from adding, editing, deleting, or just reading whats on a todo list.\n"
    "Assign work to one agent at a time, do not call agents in parallel.\n"
    "When the user provides a request, determine the most suitable agent to handle it and transfer the request to that agent.\n"
    "I may make requests that require you to use multiple agents, in this case, please break down the activities appropriately and transfer key information from one agent output into another agent input.\n"
    "Once an agent has completed its task and indicates it is transferring back to you with a 'FINAL ANSWER', you MUST take that final answer and present it directly to the user. You can remove any reference to 'final answer' to clean up the response and add your own quirky style to the final response.\n"
    "If any information is missing for the agent to complete its task, re-prompt the user for the missing details\n"
    "If the request is not suitable for any of the specialized agents, feel free to answer it as you would if I was having a normal conversation with you as a standalone language model."
)

# 然后使用监督器
supervisor = create_supervisor(
    model=llm_model,
    agents=[poem_agent, math_agent, weather_agent, launch_vehicle_agent, todoist_agent],
    prompt=supervisor_prompt,
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()

current_message = 0
request_process = []

@app.route("/prompt", methods = ["POST"])
def handle_prompt():
    prompt = request.json["prompt"]
    return Response(generate_stream(prompt), mimetype="text/event-stream")


def generate_stream(prompt):
    for data in submit_prompt_to_llm(prompt):
        json_data = json.dumps(data)
        yield f"data: {json_data}\n\n"


def submit_prompt_to_llm(prompt):
    request_process = []
    current_message = 0
    for chunk in supervisor.stream({"messages": prompt}):
        for agent_name, agent_data in chunk.items():
            if agent_data and "messages" in agent_data and isinstance(agent_data["messages"], list):
                messages = agent_data["messages"]
                for i in range(current_message, len(messages)):
                    message = messages[i]
                    message.pretty_print()
                    response_dict = {agent_name: message.model_dump()}
                    request_process.append(response_dict)

                    yield{
                        "response": response_dict, 
                        "step": request_process,
                        "done": False,
                    }

                    current_message +=1
    
    final_message = chunk.get("supervisor", {}).get("messages", [])[-1] if chunk.get("supervisor", {}).get("messages") else None

    if final_message:
        print(f"J.A.R.V.I.S : {final_message.content}")
        yield{
                        "response": {"supervisor": {"content":final_message.content}}, 
                        "step": request_process,
                        "done": True,
        }
    else:
        yield{
                "response": "No Final Response", 
                        "step": request_process,
                        "done": True,
            }
    

if __name__ == "__main__":
    app.run(port = 5000)