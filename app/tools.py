import time
import python_weather
from langchain.tools import tool


@tool
def search_places(destination: str, interest: str) -> str:
    """
    🔍 Simulate a place search by generating LLM-friendly output.
    """
    try:
        return (
            f"Please recommend popular places in {destination} for someone interested in {interest}.\n"
            f"Include famous attractions, food spots, or cultural sites if relevant. Add emojis!"
        )
    except Exception as e:
        return f"❌ Error: Could not simulate search. {str(e)}"


@tool
def get_weather(destination: str) -> str:
    """
    🌦️ Get the current weather for a given travel destination.

    Args:
        destination (str): The location you'd like the weather for (e.g., "Osaka").

    Returns:
        str: Current temperature and weather description.
    """
    try:
        client = python_weather.Client(unit=python_weather.IMPERIAL)
        weather = client.get(destination)

        temp = weather.temperature
        description = getattr(weather, "description", "No description available")

        return (
            f"🌍 Weather in {destination}:\n"
            f"🌡️ Temperature: {temp}°F\n"
            f"🌤️ Description: {description}"
        )

    except Exception as e:
        return f"❌ Error: Unable to retrieve weather data for {destination}. {str(e)}"


@tool
def calculate_budget(destination: str, days: int) -> str:
    """
    💰 Estimate your travel budget based on destination and length of stay.

    Args:
        destination (str): Where you're going (e.g., "Seoul").
        days (int): Number of days you'll stay.

    Returns:
        str: Estimated total cost (based on 1500 units/day).
    """
    try:
        cost = days * 1500
        return (
            f"💸 Estimated budget for {days} days in {destination}: {cost} 💰 "
            f"(based on 1500 per day). ✈️🧳"
        )
    except Exception as e:
        return f"❌ Error: Unable to calculate budget. {str(e)}"


@tool
def generate_itinerary(destination: str, days: int, interests: str) -> str:
    """
    🗺️ Create a personalized travel itinerary.

    Args:
        destination (str): Where you're headed (e.g., "Bangkok").
        days (int): Number of days you'll spend there.
        interests (str): Comma-separated list of interests (e.g., "food, temples, shopping").

    Returns:
        str: A simple 3-day travel itinerary.
    """
    try:
        interest_list = interests.split(", ")
        plan = " 🎯 ".join(interest_list)

        return (
            f"🗺️ Suggested {days}-day itinerary in {destination}:\n"
            f"📅 Day 1: Arrival & explore nearby 🛬\n"
            f"📅 Day 2: Activities around {plan} 🏖️🍜🎨\n"
            f"📅 Day 3: Chill, shop, and head home 🧘‍♂️🛍️✈️"
        )
    except Exception as e:
        return f"❌ Error: Unable to generate itinerary. {str(e)}"
