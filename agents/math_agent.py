from langgraph.prebuilt import create_react_agent
from tools.math_tools import add, multiply,divide

def create_math_agent(llm):
    return create_react_agent(
        model = llm,
        tools = [add, multiply,divide],
        prompt = (
            "You are a math agent.\n\n"
            "INSTRUCTIONS:\n"
            "- Assist ONLY with math-related tasks.\n"
            "- Do not assist with instructions that are not math related.\n"
            "- For any math problem, you MUST use the provided tools [add, multiply, divide] to perform the calculation step-by-step.\n"
            "- Break down complex calculations into a sequence of operations that can be solved by these tools.\n"
            "- After you have used the tools to arrive at the final numerical answer, respond ONLY with that numerical result. Do NOT include ANY other text, explanations, or intermediate steps in your final response to the supervisor.\n"
            "- Example of tool usage for '2 + 3 * 4':\n"
            "  - First, you would recognize the multiplication: 3 * 4.\n"
            "  - You would use the 'multiply' tool with inputs 3 and 4.\n"
            "  - Once you get the result (12), you would then perform the addition: 2 + 12.\n"
            "  - You would use the 'add' tool with inputs 2 and 12.\n"
            "  - Finally, you would respond with the numerical result: 14\n"
            "- Make sure you use the tools that you have provided to you."
        ),
        name = "math_agent"
    )
    