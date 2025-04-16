from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from tools import search_places, get_weather, calculate_budget, generate_itinerary
from llm_config import get_gpt_4o_llm


def create_travel_agent_graph():
    tools = [
        search_places,
        get_weather,
        calculate_budget,
        generate_itinerary,
    ]

    llm = get_gpt_4o_llm()
    llm_with_tools = llm.bind_tools(tools)
    agent = create_react_agent(llm_with_tools, tools=tools, debug=True)

    return agent
