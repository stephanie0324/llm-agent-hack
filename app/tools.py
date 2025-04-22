from langchain.tools import tool
from typing import TypedDict, Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import requests
import urllib3

from config import settings
from utils import get_response_from_ai_service

# Suppress SSL warnings if needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set LLM Model
model_config = settings.MODEL_CONFIG.root


# === Schemas ===
class FormatInput(TypedDict):
    itinerary: str
    language: str


class ScheduleItem(BaseModel):
    time: str = Field(..., description="活動開始的時間，例如 '08:00'")
    activity: str = Field(..., description="活動內容，例如 'Visit Asakusa Temple'")
    cost: int = Field(..., description="此活動的花費（單位：日幣）")


class DaySchedule(BaseModel):
    day: int = Field(..., description="第幾天的行程")
    schedule: List[ScheduleItem] = Field(..., description="此天的詳細行程表")


class ItineraryPlan(BaseModel):
    title: str = Field(..., description="行程標題，簡短描述此行程主題")
    highlights: List[str] = Field(..., description="從整個行程中擷取出來的三個亮點活動")
    total_cost: int = Field(..., description="整趟行程的總費用（日幣）")
    avg_per_day: float = Field(..., description="平均每日費用（日幣）")
    details: List[DaySchedule] = Field(..., description="完整的每日行程安排")


# ==========================================================
# TOOLS
# ==========================================================


@tool
def get_weather(city: str, start_date: str, end_date: str) -> str:
    """
    🌦️ Get the weather forecast for a specific city and date range.

    Args:
        city (str): City name (e.g., "Tokyo").
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.

    Returns:
        str: Weather information within the specified date range.
    """
    base_url = "https://api.weatherbit.io/v2.0/forecast/daily"
    params = {
        "city": city,
        "days": 16,
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


@tool
def search_flight(
    departure_city: str,
    destination_city: str,
    start_date: str,
    end_date: str,
    flight_budget: float,
    flight_class: str,
    flight_time_pref: str,
    airline_preference: str,
    with_luggage: bool,
    non_stop: bool,
):
    """
    ✈️ Search for return flights based on user preferences, ensuring at least 10 flight options within the budget.

    Args:
        departure_city (str): City of departure.
        destination_city (str): City of destination.
        start_date (str): Departure date in YYYY-MM-DD format.
        end_date (str): Return date in YYYY-MM-DD format.
        flight_budget (float): Maximum budget for the round-trip flight.
        flight_class (str): Flight class preference (Budget, Economy, Business, First).
        flight_time_pref (str): Preferred flight time (Any, Morning, Afternoon, Evening, Red-eye).
        airline_preference (str): Preferred airline name.
        with_luggage (bool): Whether the user wants checked luggage.
        non_stop (bool): Whether the user prefers a non-stop flight.

    Returns:
        str: Flight search results with at least 10 options within budget.
    """
    try:
        query = f"""
        Search for return flights from {departure_city} to {destination_city} between {start_date} and {end_date}.
        The user has a budget of ${flight_budget}. 
        Flight class preference: {flight_class}.
        Preferred flight time: {flight_time_pref}.
        Preferred airline: {airline_preference}.
        Include checked luggage: {'Yes' if with_luggage else 'No'}.
        Non-stop flight: {'Yes' if non_stop else 'No'}.
        Please return at least 10 flight options that fall within the budget, including round-trip flights with details 
        such as flight times, layovers, and pricing.
        """
        return get_response_from_ai_service(query)

    except requests.exceptions.RequestException as e:
        return f"❌ Error: Unable to retrieve flight data for {departure_city} to {destination_city}. {str(e)}"


@tool
def search_and_generate_itinerary(
    destination: str,
    days: str,
    start_date: str,
    end_date: str,
    interests: str,
    weather: str,
    remain_budget: float,
    travel_companions: str,
    transportation: str,
    travel_style: str,
    dietary: str,
    budget_currency: str,
) -> str:
    """
    🗺️ Search and generate a personalized itinerary using AI based on user preferences and trip details.

    Args:
        destination (str): Destination city.
        days (str): Total days spent
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        interests (str): User's travel interests (e.g., adventure, culture, food).
        weather (str): Expected weather conditions.
        remain_budget (float): Remaining budget for the trip.
        travel_companions (str): Type of travel companions (Solo, Family, Friends, etc.).
        transportation (str): Preferred transportation method.
        travel_style (str): Travel style (e.g., luxury, budget, adventure).
        dietary (str): Dietary preferences (e.g., vegetarian, gluten-free, etc.).
        budget_currency (str): Currency for the budget (e.g., USD, EUR).

    Returns:
        str: A detailed, personalized itinerary generated by the AI response.
    """
    try:
        # Construct the query for generating the itinerary based on inputs
        query = f"""
        Generate a {days}-day itinerary for the destination {destination} from {start_date} to {end_date}.
        Please generate 3 itinerary options for the user to choose from.
        The user has the following preferences:
        - Interests: {interests}
        - Weather: {weather}
        - Budget: {remain_budget} {budget_currency}
        - Travel Companions: {travel_companions}
        - Transportation: {transportation}
        - Travel Style: {travel_style}
        - Dietary Preferences: {dietary}
        
        For each day, include:
        1. 🍽️ Breakfast, lunch, and dinner suggestions (dish names or restaurant recommendations)
        2. 🌟 Two activities (places to visit or things to do)
        3. 🚇 Suggested transport (e.g., public transport, taxi, rental car)
        4. 🌧️ Weather tip (e.g., "Bring an umbrella")

        Please ensure the itinerary is well balanced and fits the user's budget and interests.
        """

        # Make the call to the AI service (get_response_from_ai_service should be implemented as per your setup)
        return get_response_from_ai_service(query)

    except Exception as e:
        return f"❌ Error: {str(e)}"


@tool
def format_itinerary(
    raw_text: str, destination: str, trip_days: int, language: str
) -> List[ItineraryPlan]:
    """
    將旅遊摘要文字轉換成三個格式化的行程建議（List[ItineraryPlan]），
    包含每日活動、時間與花費，輸出結構需完全符合 ItineraryPlan。
    """
    query = f"""
    內容必須是 {language}
    請你根據以下旅遊摘要內容，生成三組格式化的行程建議，每組行程需符合 `ItineraryPlan` 結構。
    請以 JSON 陣列的形式回傳（List[ItineraryPlan]），並務必符合下列欄位要求：

    地點：{destination}
    行程天數：{trip_days}
    摘要文字如下：
    ---
    {raw_text}
    ---
    請確保輸出結構為：
    [
    {{
        "title": str,
        "highlights": [str, str, ...],
        "total_cost": int,
        "avg_per_day": int,
        "details": [
        {{
            "day": int,
            "schedule": [
            [str (time), str (activity name)]
            ]
        }}
        ]
    }},
    ...
    ]
    """

    try:
        # Make the call to the AI service (get_response_from_ai_service should be implemented as per your setup)
        return get_response_from_ai_service(query)

    except Exception as e:
        return f"❌ Error: {str(e)}"
