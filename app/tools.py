from datetime import datetime
from typing import Dict, List

import requests
import urllib3
from config import settings
from langchain.tools import tool
from schemas.schema import ItineraryPlan
from utils import get_response_from_ai_service

# Suppress SSL warnings if needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set LLM Model
model_config = settings.MODEL_CONFIG.root


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
def search_hotel(
    destination: str,
    check_in_date: str,
    check_out_date: str,
    hotel_budget: float,
    hotel_rating: float,
    hotel_type: str,
    amenities: str,
):
    """
    🏨 Search for hotels based on user preferences, ensuring at least 10 hotel options within the budget.

    Args:
        destination (str): Destination city.
        check_in_date (str): Check-in date in YYYY-MM-DD format.
        check_out_date (str): Check-out date in YYYY-MM-DD format.
        hotel_budget (float): Maximum budget for the hotel stay.
        hotel_rating (float): Minimum star rating for the hotel.
        hotel_type (str): Type of hotel (e.g., luxury, budget, boutique).
        amenities (str): Desired amenities (e.g., pool, gym, breakfast).

    Returns:
        str: Hotel search results with at least 10 options within budget.
    """
    try:
        query = f"""
        Search for hotels in {destination} from {check_in_date} to {check_out_date}.
        The user has a budget of ${hotel_budget}. 
        Minimum star rating: {hotel_rating}.
        Hotel type preference: {hotel_type}.
        Desired amenities: {amenities}.
        Please return at least 10 hotel options that fall within the budget, including details such as pricing, 
        location, and amenities.
        """
        return get_response_from_ai_service(query)

    except requests.exceptions.RequestException as e:
        return f"❌ Error: Unable to retrieve hotel data for {destination}. {str(e)}"


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
    Converts the raw travel summary text into three formatted itinerary suggestions (List[ItineraryPlan]),
    including daily activities, time, and cost. The output structure must strictly follow the ItineraryPlan format.
    """
    output_structure = """
    [
    {
        "title": str,
        "highlights": [str, str, ...],
        "total_cost": int,
        "avg_per_day": float,
        "hotels": [
            {
                "name": str,
                "price": int,
                "rating": float,
                "start_date": str,
                "end_date": str
            },
            ...
        ],
        "flights": [
            {
                "start_date": str,
                "from": str,
                "to": str,
                "airline": str,
                "class": str,
                "check-in luggage": bool,
                "price": int
            },
            ...
        ],
        "details": [
            {
                "date": str,
                "schedule": [
                    {
                        "start_time": str,
                        "end_time": str,
                        "activity": str,
                        "description": str
                    },
                    ...
                ],
                "hotel": {
                    "name": str
                }
            },
            ...
        ]
    },
    ...
    ]
    """

    query = f"""
    The content must be in {language}.
    Based on the following travel summary, generate three formatted itinerary suggestions. Each itinerary must follow the `ItineraryPlan` structure.
    The output should be in a JSON array format (List[ItineraryPlan]) and must include the following fields:
    When you generate title, please make it short and catchy.

    Location: {destination}
    Trip duration: {trip_days} days
    Summary text as follows:
    ---
    {raw_text}
    ---
    Please ensure the output structure is as follows:
    {output_structure}
    """

    try:
        # Make the call to the AI service (get_response_from_ai_service should be implemented as per your setup)
        return get_response_from_ai_service(query)

    except Exception as e:
        return f"❌ Error: {str(e)}"


@tool
def modify_itinerary(
    current_itinerary: Dict,
    modification_request: str,
    preferences: Dict,
) -> Dict:
    """
    🔄 修改現有行程根據用戶的要求和偏好。

    Args:
        current_itinerary (Dict): 當前需要修改的行程
        modification_request (str): 用戶的具體修改要求
        preferences (Dict): 用戶偏好，包括預算、興趣等

    Returns:
        Dict: 修改後的行程
    """
    try:
        query = f"""
        Please modify the following itinerary according to the user's request and preferences:
        
        Current Itinerary:
        {current_itinerary}
        
        Modification Request:
        {modification_request}
        
        User Preferences:
        {preferences}
        
        Please maintain the same time structure but modify the selected activities according to the request.
        Consider the user's preferences while making modifications.
        Ensure the modifications are realistic and maintain the flow of the itinerary.
        """

        return get_response_from_ai_service(query)

    except Exception as e:
        return f"❌ Error: {str(e)}"


@tool
def search_activities(
    location: str,
    interests: List[str],
    budget: float,
    time_slot: str,
    weather: str = None,
    indoor_only: bool = False,
) -> List[Dict]:
    """
    🎯 Search for activities in a specific location based on user preferences.

    Args:
        location (str): The location to search for activities
        interests (List[str]): List of user interests
        budget (float): Available budget for the activity
        time_slot (str): Preferred time slot (morning/afternoon/evening)
        weather (str, optional): Weather condition to consider
        indoor_only (bool, optional): Whether to only show indoor activities

    Returns:
        List[Dict]: List of activity suggestions with details
    """
    try:
        query = f"""
        Find activities in {location} that match:
        - Interests: {', '.join(interests)}
        - Budget: {budget}
        - Time: {time_slot}
        - Weather: {weather if weather else 'Any'}
        - {'Indoor activities only' if indoor_only else 'Both indoor and outdoor activities'}
        """

        return get_response_from_ai_service(query)
    except Exception as e:
        return f"❌ Error: {str(e)}"


@tool
def get_travel_time(
    origin: str,
    destination: str,
    mode: str = "transit",
    departure_time: str = None,
) -> Dict:
    """
    🚗 Get estimated travel time between two locations.

    Args:
        origin (str): Starting location
        destination (str): Ending location
        mode (str): Transportation mode (transit/walking/driving)
        departure_time (str, optional): Departure time in HH:MM format

    Returns:
        Dict: Travel time details including duration and route options
    """
    try:
        query = f"""
        Calculate travel time from {origin} to {destination}:
        - Mode: {mode}
        - Departure: {departure_time if departure_time else 'Now'}
        """

        return get_response_from_ai_service(query)
    except Exception as e:
        return f"❌ Error: {str(e)}"


@tool
def check_opening_hours(
    place_name: str,
    date: str,
    location: str = None,
) -> Dict:
    """
    ⏰ Check the opening hours for a specific place.

    Args:
        place_name (str): Name of the place
        date (str): Date to check in YYYY-MM-DD format
        location (str, optional): Location details for disambiguation

    Returns:
        Dict: Opening hours information including special holiday schedules
    """
    try:
        query = f"""
        Check opening hours for {place_name}:
        - Date: {date}
        {f'- Location: {location}' if location else ''}
        """

        return get_response_from_ai_service(query)
    except Exception as e:
        return f"❌ Error: {str(e)}"
