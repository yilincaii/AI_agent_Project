from langgraph.prebuilt import create_react_agent

def create_poem_agent(llm):
    return create_react_agent(
        model = llm,
        tools = [],
        name = "poem_agent",
        prompt = (
                "You are a poem agent.\n\n"
                "INSTRUCTIONS:\n"
                "- Write funny poems\n"
                "- Poems should not be more that 4 lines long\n"
            ),
        
    )