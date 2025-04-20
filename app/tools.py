from langchain.tools import tool
from typing import TypedDict
from datetime import datetime, timedelta
import requests
import urllib3
from config import settings

# Suppress SSL warnings if needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set LLM Model
model_config = settings.MODEL_CONFIG.root


class FormatInput(TypedDict):
    itinerary: str
    language: str


# ==========================================================
# TOOLS
# ==========================================================


@tool
def get_weather(city: str, days: int) -> str:
    """
    🌦️ Get the weather forecast for a specific city and date range.

    Args:
        city (str): City name (e.g., "Tokyo").
        days (int): Number of days to fetch the forecast.

    Returns:
        str: Weather information for the specified date range.
    """
    base_url = "https://api.weatherbit.io/v2.0/forecast/daily"
    params = {
        "city": city,
        "days": days,
        "lang": "en",
        "units": "M",
        "key": settings.WEATHER_API_KEY,
    }

    try:
        response = requests.get(base_url, params=params, verify=False)
        response.raise_for_status()
        weather_data = response.json()

        forecast = []
        for day in weather_data["data"]:
            date = datetime.strptime(day["datetime"], "%Y-%m-%d").date()
            temp = day["temp"]
            description = day["weather"]["description"]
            forecast.append(f"📅 {date} — 🌡️ {temp}°C, 🌤️ {description}")

        return f"🌍 Weather Forecast for {city}:\n" + "\n".join(forecast)

    except requests.exceptions.RequestException as e:
        return f"❌ Error: Unable to retrieve weather data for {city}. {str(e)}"


from langchain.agents import tool


@tool
def generate_itinerary(
    destination: str, days: int, interests: str, weather: str, budget: float
) -> str:
    """
    🗺️ Generate a personalized itinerary with meals, transportation, and sightseeing based on destination, weather, and user preferences.

    Instructions:
    1. Generate a {days}-day itinerary for {destination} based on the following:
    2. Consider the user's interests: {interests}
    3. Weather conditions: {weather}
    4. Budget available: {budget} USD
    5. Each day should include:
       - 🍽️ Breakfast, lunch, and dinner (dish names or restaurant suggestions)
       - 🌟 Two activities (places to visit or things to do)
       - 🚇 Suggested transport (public, taxi, rental, etc.)
       - 🌧️ A weather-based tip (e.g., "Bring an umbrella")
    """

    try:
        # The docstring now contains all the instructions for the tool logic.
        # This is the part where the actual LLM model will be expected to understand and execute the prompt
        # based on the information provided by the tool's inputs.

        # Generate itinerary based on the description and return the output.
        # For now, we just return a placeholder response (you can customize it based on your needs).
        itinerary = f"Here's your {days}-day itinerary for {destination}: \n"
        itinerary += f"Interests: {interests} \n"
        itinerary += f"Weather: {weather} \n"
        itinerary += f"Budget: {budget} USD \n"
        itinerary += "\nEach day includes:\n"

        # Example day structure (this can be extended or modified to match your exact needs)
        for i in range(1, days + 1):
            itinerary += f"Day {i}: \n"
            itinerary += "🍽️ Breakfast: [Dish/Restaurant suggestion] \n"
            itinerary += "🌟 Activity 1: [Place/Activity suggestion] \n"
            itinerary += "🌟 Activity 2: [Place/Activity suggestion] \n"
            itinerary += (
                "🚇 Suggested transport: [Public transport/Taxi/Rental suggestion] \n"
            )
            itinerary += "🌧️ Weather tip: [Tip based on the weather] \n"

        return itinerary

    except Exception as e:
        return f"❌ Error: {str(e)}"


@tool
def format_itinerary(itinerary: dict, language: str) -> str:
    """
    Formats the given itinerary into a markdown-styled table with days as columns and adds a title based on the language.

    Args:
        itinerary (dict): A dictionary containing details for each day (meals, activities, transport, weather tips).
        language (str): The language for the itinerary title.

    Returns:
        str: A markdown-formatted table with the itinerary and a title.
    """
    # Language-based title map
    title_map = {
        "en": "🧳 Here is your travel itinerary!",
        "ja": "🧳 あなたの旅行プランはこちら！",
        "ko": "🧳 여행 일정이 준비되었습니다!",
        "zh-tw": "🧳 您的旅遊行程如下！",
    }
    title = title_map.get(language, title_map["en"])

    # Create the table header with days as columns
    days = len(itinerary)
    header = "| Meal | " + " | ".join([f"Day {i+1}" for i in range(days)]) + " |"
    separator = "|------|" + "|---------|" * days

    # Add data rows
    meals = (
        "| Breakfast, Lunch, Dinner | "
        + " | ".join([itinerary[f"Day {i+1}"]["meal"] for i in range(days)])
        + " |"
    )
    activities1 = (
        "| Activity 1 | "
        + " | ".join([itinerary[f"Day {i+1}"]["activity1"] for i in range(days)])
        + " |"
    )
    activities2 = (
        "| Activity 2 | "
        + " | ".join([itinerary[f"Day {i+1}"]["activity2"] for i in range(days)])
        + " |"
    )
    transport = (
        "| Transport | "
        + " | ".join([itinerary[f"Day {i+1}"]["transport"] for i in range(days)])
        + " |"
    )
    weather = (
        "| Weather Tip | "
        + " | ".join([itinerary[f"Day {i+1}"]["weather_tip"] for i in range(days)])
        + " |"
    )

    # Constructing the full markdown output
    table = f"""
    # {title}

    ```markdown
    {header}
    {separator}
    {meals}
    {activities1}
    {activities2}
    {transport}
    {weather}
    ✈️ Safe travels and have fun!
    ```
    """

    return table
