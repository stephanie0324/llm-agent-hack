from config import settings
from langgraph.prebuilt import create_react_agent
from tools import (
    check_opening_hours,
    format_itinerary,
    get_travel_time,
    get_weather,
    search_activities,
    search_and_generate_itinerary,
    search_flight,
    search_hotel,
)

# Set LLM Model
model_config = settings.MODEL_CONFIG.root

# Create the LLM instance
llm = model_config["AOAI"].as_instance()


def create_travel_agent():
    tools = [
        get_weather,
        search_flight,
        search_hotel,
        search_and_generate_itinerary,
        format_itinerary,
    ]

    # Bind the tools to the LLM
    llm_with_tools = llm.bind_tools(tools)

    # Create the agent with both model and tools
    agent = create_react_agent(model=llm_with_tools, tools=tools, debug=settings.DEBUG)

    return agent


def create_modify_itinerary_agent():
    """Create an agent specifically for modifying existing itineraries.

    Returns:
        Agent: A ReAct agent with tools for modifying itineraries
    """
    tools = [
        get_weather,
        search_flight,
        search_hotel,
        search_and_generate_itinerary,
        format_itinerary,
        # search_activities,
        # get_travel_time,
        # check_opening_hours,
    ]

    # Bind the tools to the LLM
    llm_with_tools = llm.bind_tools(tools)

    # Create the agent with both model and tools
    agent = create_react_agent(model=llm_with_tools, tools=tools, debug=settings.DEBUG)

    return agent
