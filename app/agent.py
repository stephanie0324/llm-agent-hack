from langgraph.prebuilt import create_react_agent
from tools import (
    get_weather,
    search_and_generate_itinerary,
    format_itinerary,
    search_flight,
)
from config import settings

# Set LLM Model
model_config = settings.MODEL_CONFIG.root


def create_travel_agent():
    tools = [get_weather, search_and_generate_itinerary, format_itinerary]

    # Create the LLM instance
    llm = model_config["AOAI"].as_instance()

    # Bind the tools to the LLM
    llm_with_tools = llm.bind_tools(tools)

    # Create the agent with both model and tools
    agent = create_react_agent(model=llm_with_tools, tools=tools, debug=settings.DEBUG)

    return agent
