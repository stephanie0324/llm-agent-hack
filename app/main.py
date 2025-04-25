import datetime
import json
import re
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

import streamlit as st
from agent import create_modify_itinerary_agent, create_travel_agent
from mock_api import get_mock_itineraries, get_mock_modified_itinerary

# Tool emoji mapping
emoji_map = {
    "search_web": "🔍",
    "search_flights": "✈️",
    "search_hotels": "🏨",
    "search_activities": "🎯",
    "search_restaurants": "🍽️",
    "get_weather": "🌤️",
    "get_exchange_rate": "💱",
    "format_itinerary": "📅",
}


@dataclass
class TravelPreferences:
    language: str
    travel_style: List[str]
    interests: List[str]
    transportation: str
    dietary: List[str]


@dataclass
class FlightPreferences:
    budget: float
    flight_class: str
    time_preference: str
    airline: Optional[str]
    with_luggage: bool
    non_stop: bool


@dataclass
class HotelPreferences:
    budget: float
    stars: str
    features: List[str]
    types: List[str]


@dataclass
class TravelConfig:
    departure: str
    destination: str
    start_date: datetime.date
    end_date: datetime.date
    total_budget: float
    currency: str
    flight_prefs: FlightPreferences
    hotel_prefs: HotelPreferences
    travel_prefs: TravelPreferences

    @property
    def days(self) -> int:
        return (self.end_date - self.start_date).days


@dataclass
class ItineraryModification:
    timestamp: datetime.datetime
    original_activities: List[Dict]
    modified_activities: List[Dict]
    instruction: str


@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: datetime.datetime


class ChatHistory:
    def __init__(self):
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

    def add_message(self, role: str, content: str):
        """Add a new message to the chat history"""
        message = ChatMessage(
            role=role, content=content, timestamp=datetime.datetime.now()
        )
        st.session_state.chat_messages.append(message)

    def get_messages(self) -> List[ChatMessage]:
        """Get all messages in the chat history"""
        return st.session_state.chat_messages

    def clear(self):
        """Clear the chat history"""
        st.session_state.chat_messages = []


class ItineraryHistory:
    def __init__(self):
        self.modifications = []
        if "modification_thoughts" not in st.session_state:
            st.session_state.modification_thoughts = []

    def add_modification(self, mod: ItineraryModification):
        self.modifications.append(mod)

    def add_modification_thoughts(self, thoughts: List[Dict]):
        if "modification_thoughts" not in st.session_state:
            st.session_state.modification_thoughts = []
        st.session_state.modification_thoughts.append(thoughts)

    def get_latest_modification(self) -> Optional[ItineraryModification]:
        return self.modifications[-1] if self.modifications else None

    def get_all_thoughts(self) -> List[List[Dict]]:
        return st.session_state.modification_thoughts

    def clear(self):
        self.modifications = []
        if "modification_thoughts" in st.session_state:
            st.session_state.modification_thoughts = []


class ItineraryPlanner:
    def __init__(self, config: TravelConfig):
        self.config = config
        self.agent = create_travel_agent()
        self.emoji_map = {
            "search_flight": "✈️",
            "search_hotel": "🏨",
            "get_weather": "⛅️",
            "search_and_generate_itinerary": "🗺️",
            "format_itinerary": "📋",
        }

    def generate_prompt(self) -> str:
        # From session state, get all necessary variables
        departure = st.session_state.get("departure", "Taipei")
        destination = st.session_state.get("destination", "Tokyo")
        start_date = st.session_state.get("start_date", datetime.date.today())
        end_date = st.session_state.get(
            "end_date", datetime.date.today() + datetime.timedelta(days=3)
        )
        days = (end_date - start_date).days

        # Budget related
        total_budget = st.session_state.get("total_budget", 30000)
        budget_currency = st.session_state.get("budget_currency", "TWD")
        flight_budget = st.session_state.get("flight_budget", 10000)
        hotel_budget = st.session_state.get("hotel_budget", 15000)

        # Flight preferences
        flight_class = st.session_state.get("flight_class", "Economy")
        flight_time_pref = st.session_state.get("flight_time_pref", "Any")
        airline_preference = st.session_state.get("airline_preference", None)
        with_luggage = st.session_state.get("with_luggage", True)
        non_stop = st.session_state.get("non_stop", True)

        # Accommodation preferences
        hotel_stars = st.session_state.get("hotel_stars", "3★")
        hotel_features = st.session_state.get("hotel_features", [])
        hotel_type = st.session_state.get("hotel_type", [])

        # Travel preferences
        travel_companions = st.session_state.get("travel_companions", "Solo")
        transportation = st.session_state.get("transportation", "Public Transport")
        travel_style = st.session_state.get("travel_style", [])
        dietary = st.session_state.get("dietary", ["None"])
        interests = st.session_state.get("interests", [])

        # Language settings
        lang_code = st.session_state.get("language", "English")

        return f"""
        Please help plan 3 personalized itinerary for the user to choose with the following information:
        Consider the below details, budget and weather.

        Departure: {departure}
        Destination: {destination}
        Total Days: {days}
        Start Date: {start_date}
        End Date: {end_date}
        Budget: {total_budget} {budget_currency}

        Flight Preferences:
        - Flight Budget: {flight_budget}
        - Class: {flight_class}
        - Preferred Time: {flight_time_pref}
        - Preferred Airline: {airline_preference or "None"}
        - Checked Luggage: {'Yes' if with_luggage else 'No'}
        - Non-Stop Flight: {'Yes' if non_stop else 'No'}

        Hotel Preferences:
        - Hotel Budget: {hotel_budget}
        - Stars: {hotel_stars}
        - Features: {', '.join(hotel_features) if hotel_features else 'None'}
        - Type: {', '.join(hotel_type) if hotel_type else 'None'}

        Companions: {travel_companions}
        Transportation Preference: {transportation}
        Travel Style: {', '.join(travel_style) if travel_style else 'None'}
        Dietary Requirements: {', '.join(dietary) if dietary else 'None'}
        Interests: {', '.join(interests) if interests else 'None'}
        Remaining Budget: {total_budget - (flight_budget + hotel_budget)}

        Language: {lang_code}
        You need to use `format_itinerary` to return the result in json format and only the json format.
        """

    def generate_itineraries(self):
        # Use mock data for development
        # return get_mock_itineraries()
        prompt = self.generate_prompt()

        with st.spinner("🧠 Agent is reasoning..."):
            progress_bar = st.progress(0)
            progress_text = st.empty()
            thought_block = st.expander("", expanded=True)

            try:
                # Initialize counter and list for tool names
                tool_call_count = 0
                function_names = []  # List to store all function names

                # Dynamically collect tool calls and display detailed output
                with thought_block:
                    raw_content = None
                    for event in self.agent.stream(
                        {"messages": [{"role": "user", "content": prompt}]}
                    ):
                        if "agent" in event:
                            for message in event["agent"]["messages"]:
                                # Check if message contains tool calls
                                if hasattr(message, "additional_kwargs"):
                                    tool_calls = getattr(
                                        message, "additional_kwargs", {}
                                    ).get("tool_calls", [])

                                    for tool_call in tool_calls:
                                        tool_name = tool_call["function"]["name"]
                                        tool_args = tool_call["function"]["arguments"]
                                        emoji = self.emoji_map.get(tool_name, "🔧")

                                        with st.chat_message("assistant"):
                                            st.markdown(
                                                f"{emoji} **Calling `{tool_name}`**"
                                            )
                                            st.code(tool_args, language="json")

                                        # Update progress bar dynamically
                                        tool_call_count += 1
                                        progress = min(
                                            tool_call_count / (tool_call_count + 1), 1.0
                                        )
                                        progress_bar.progress(progress)

                                # If it is the final result, display the final output
                                if hasattr(message, "content") and message.content:
                                    raw_content = message.content
                                    progress_bar.progress(1.0)  # Complete
                                    progress_text.text("✅ Process complete! 🎉")
                                    break  # Break the loop after getting the final result

                    if raw_content:
                        # Extract JSON from the raw content
                        cleaned = re.search(r"```json(.*?)```", raw_content, re.DOTALL)
                        itineraries = (
                            json.loads(cleaned.group(1).strip())
                            if cleaned
                            else json.loads(raw_content.strip())
                        )
                        return itineraries
                    else:
                        raise Exception("No content received from agent")

            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
                # If an error occurs, return mock data
                return get_mock_itineraries()
            finally:
                # Ensure progress bar is completed
                progress_bar.progress(1.0)


class ModifyItineraryAgent:
    def __init__(self, config: TravelConfig):
        self.config = config
        self.agent = create_modify_itinerary_agent()
        self.emoji_map = {
            "search_activities": "🎯",
            "get_travel_time": "🚗",
            "check_opening_hours": "⏰",
            "get_weather": "🌤️",
            "format_itinerary": "📋",
        }

    def _generate_modification_prompt(
        self,
        original_plan: dict,
        selected_activities: List[dict],
        modification_instruction: str,
    ) -> str:
        # Format selected activities
        selected_activities_formatted = "\n".join(
            [
                f"- Date: {act['date']}, Time: {act['time']}~{act['end_time']}, "
                f"Activity: {act['activity']}"
                for act in selected_activities
            ]
        )

        # Get user preferences from config
        travel_style = ", ".join(self.config.travel_prefs.travel_style)
        transportation = self.config.travel_prefs.transportation
        interests = ", ".join(self.config.travel_prefs.interests)
        dietary = ", ".join(self.config.travel_prefs.dietary)

        # Budget information
        total_budget = self.config.total_budget
        remaining_budget = total_budget - (
            self.config.flight_prefs.budget + self.config.hotel_prefs.budget
        )
        currency = self.config.currency

        # Hotel preferences
        hotel_stars = self.config.hotel_prefs.stars
        hotel_features = ", ".join(self.config.hotel_prefs.features)
        hotel_types = ", ".join(self.config.hotel_prefs.types)

        return f"""
        Please help modify the itinerary based on the following requirements:

        Original Activities to Modify:
        {selected_activities_formatted}

        Modification Request:
        {modification_instruction}

        Current Itinerary:
        {json.dumps(original_plan, indent=2)}

        User Preferences and Constraints:
        1. Budget Constraints:
           - Total Budget: {total_budget} {currency}
           - Remaining Budget: {remaining_budget} {currency}
           
        2. Travel Style and Preferences:
           - Travel Style: {travel_style}
           - Transportation: {transportation}
           - Interests: {interests}
           - Dietary Requirements: {dietary}
           
        3. Hotel Preferences:
           - Star Rating: {hotel_stars}
           - Required Amenities: {hotel_features}
           - Accommodation Types: {hotel_types}

        Modification Requirements:
        1. Maintain the original JSON format
        2. Only modify selected activities while keeping others unchanged
        3. Ensure modifications comply with:
           - Budget constraints
           - Time constraints (no overlapping)
           - Geographic feasibility (consider travel time)
           - Operating hours
           - Weather conditions (for outdoor activities)
        4. New activities must align with user preferences:
           - Match travel style
           - Consider transportation preferences
           - Align with interests
           - Respect dietary requirements
        5. For restaurant modifications:
           - Ensure dietary compliance
           - Consider appropriate meal times
        6. For attraction modifications:
           - Verify operating hours
           - Consider weather impact (outdoor activities)
           - Assess transportation feasibility

        Please use the following tools to assist with modifications:
        - search_activities: Find suitable new activities
        - get_travel_time: Verify travel time between locations
        - check_opening_hours: Confirm operating hours
        - get_weather: Check weather conditions (outdoor activities)
        - format_itinerary: Format the final itinerary

        Please return the complete modified itinerary in JSON format.
        """

    def modify_itinerary(
        self,
        original_plan: dict,
        selected_activities: List[dict],
        modification_instruction: str,
        history: ItineraryHistory,
    ) -> dict:
        # for development
        # return get_mock_modified_itinerary(
        #     original_plan, selected_activities, modification_instruction
        # )
        # Prepare prompt
        prompt = self._generate_modification_prompt(
            original_plan, selected_activities, modification_instruction
        )

        # Create progress indicators
        progress_bar = st.progress(0)
        progress_text = st.empty()

        # Create an expander for agent's thought process
        thought_block = st.expander("🤔 Agent's Thought Process", expanded=True)

        try:
            # Initialize tool call counter and thoughts list
            tool_call_count = 0
            thoughts = []

            # Process agent's response
            with thought_block:
                st.markdown("### 🔄 Modification Process")
                raw_content = None

                for event in self.agent.stream(
                    {"messages": [{"role": "user", "content": prompt}]}
                ):
                    if "agent" in event:
                        for message in event["agent"]["messages"]:
                            # Handle tool calls
                            if hasattr(message, "additional_kwargs"):
                                tool_calls = getattr(
                                    message, "additional_kwargs", {}
                                ).get("tool_calls", [])

                                for tool_call in tool_calls:
                                    tool_name = tool_call["function"]["name"]
                                    tool_args = tool_call["function"]["arguments"]
                                    emoji = self.emoji_map.get(tool_name, "🔧")

                                    # Add thought process
                                    thought = {
                                        "type": "tool_call",
                                        "tool": tool_name,
                                        "args": tool_args,
                                        "emoji": emoji,
                                    }
                                    thoughts.append(thought)

                                    st.markdown(f"#### {emoji} Using {tool_name}")
                                    st.code(tool_args, language="json")

                                    # Update progress
                                    tool_call_count += 1
                                    progress = min(
                                        tool_call_count / (tool_call_count + 1), 1.0
                                    )
                                    progress_bar.progress(progress)

                            # Handle agent's reasoning
                            if hasattr(message, "content") and message.content:
                                if (
                                    "I need to" in message.content
                                    or "I should" in message.content
                                ):
                                    st.markdown(f"💭 **Agent's Reasoning:**")
                                    st.markdown(message.content)
                                    thoughts.append(
                                        {
                                            "type": "reasoning",
                                            "content": message.content,
                                        }
                                    )

                            # Handle final result
                            if hasattr(message, "content") and message.content:
                                raw_content = message.content
                                progress_bar.progress(1.0)
                                progress_text.text("✅ Modification complete! 🎉")

                # Display summary of modifications
                if raw_content:
                    st.markdown("### 📝 Modification Summary")
                    st.markdown("The agent followed these steps:")

                    for i, thought in enumerate(thoughts, 1):
                        if thought["type"] == "tool_call":
                            st.markdown(
                                f"{i}. {thought['emoji']} Used `{thought['tool']}` to find suitable options"
                            )
                        elif thought["type"] == "reasoning":
                            st.markdown(f"{i}. 💭 Reasoning: {thought['content']}")

                    # Save thoughts to history
                    history.add_modification_thoughts(thoughts)

                    # Extract JSON from the raw content
                    cleaned = re.search(r"```json(.*?)```", raw_content, re.DOTALL)
                    modified_plan = (
                        json.loads(cleaned.group(1).strip())
                        if cleaned
                        else json.loads(raw_content.strip())
                    )
                    return modified_plan
                else:
                    raise Exception("No content received from agent")

        except Exception as e:
            st.error(f"Error modifying itinerary: {str(e)}")
            return original_plan
        finally:
            # Ensure progress bar is completed
            progress_bar.progress(1.0)


class TravelUI:
    def __init__(self):
        self.config = None
        self.planner = None
        self._language = "English"
        self.history = ItineraryHistory()
        self.chat_history = ChatHistory()

    def update_config(self):
        """Update the current configuration from UI inputs"""
        self.config = self.get_current_config()

    def setup_page(self):
        st.set_page_config(page_title="Travel Buddy", page_icon="✈️", layout="wide")
        self._setup_styles()
        # Initialize or update config
        self.update_config()

    def _setup_styles(self):
        background_image_url = "https://c1.wallpaperflare.com/preview/447/58/538/cloudscape-texture-cloud-sky-thumbnail.jpg"
        st.markdown(
            f"""
            <style>
            .header-container {{
                text-align: center;
                        background: url({background_image_url}) no-repeat center center fixed;
                        background-size: cover;
                padding: 40px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                font-size: 60px;
                color: #ffffff;
                font-family: 'Times New Roman', serif;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: 10px;
            }}
            .subheader {{
                font-size: 24px;
                color: #ffffff;
                font-family: 'Arial', sans-serif;
                font-weight: 400;
                letter-spacing: 1px;
                font-style: italic;
            }}
            .footer {{
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                text-align: center;
                padding: 20px;
                background-color: white;
                box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.1);
                z-index: 1000;
            }}
            .footer .divider {{
                border: 0;
                border-top: 3px solid #00BFFF;
                width: 60%;
                margin: 0 auto 15px auto;
                opacity: 0.6;
            }}
            .footer-text {{
                font-size: 18px;
                font-family: 'Arial', sans-serif;
                letter-spacing: 1px;
            }}
            .footer a.streamlit {{
                color: #FF4500;  /* Orange Red for Streamlit */
                text-decoration: none;
                font-weight: bold;
            }}
            .footer a.azure {{
                color: #1E90FF;  /* Dodger Blue for Azure */
                text-decoration: none;
                font-weight: bold;
            }}
            </style>
            <div class="header-container">
                <div class="header">
                    ✈️ Travel Buddy
                </div>
                <div class="subheader">
                    Your go-to travel assistant for the perfect vacation 🏖️
                </div>
            </div>
            <div class="footer">
                <div class="divider"></div>
                <div class="footer-text">
                    Powered by <a href="https://www.streamlit.io" target="_blank" class="streamlit">Streamlit</a> & <a href="https://azure.microsoft.com" target="_blank" class="azure">Azure</a> ✨
                </div>
            </div>
    """,
            unsafe_allow_html=True,
        )

    def get_selected_language(self) -> str:
        """Get the currently selected language"""
        return self._language

    def get_current_config(self) -> TravelConfig:
        """Get the current configuration from UI inputs"""
        # Get values from sidebar inputs
        departure = st.session_state.get("departure", "Taipei")
        destination = st.session_state.get("destination", "Tokyo")
        start_date = st.session_state.get("start_date", datetime.date.today())
        end_date = st.session_state.get(
            "end_date", datetime.date.today() + datetime.timedelta(days=3)
        )

        # Create flight preferences
        flight_prefs = FlightPreferences(
            budget=st.session_state.get("flight_budget", 10000),
            flight_class=st.session_state.get("flight_class", "Economy"),
            time_preference=st.session_state.get("flight_time_pref", "Any"),
            airline=st.session_state.get("airline_preference", None),
            with_luggage=st.session_state.get("with_luggage", True),
            non_stop=st.session_state.get("non_stop", True),
        )

        # Create hotel preferences
        hotel_prefs = HotelPreferences(
            budget=st.session_state.get("hotel_budget", 15000),
            stars=st.session_state.get("hotel_stars", "3★"),
            features=st.session_state.get("hotel_features", []),
            types=st.session_state.get("hotel_type", []),
        )

        # Create travel preferences
        travel_prefs = TravelPreferences(
            language=self._language,
            travel_style=st.session_state.get("travel_style", []),
            interests=st.session_state.get("interests", []),
            transportation=st.session_state.get("transportation", "Public Transport"),
            dietary=st.session_state.get("dietary", ["None"]),
        )

        # Create and return config
        return TravelConfig(
            departure=departure,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            total_budget=st.session_state.get("total_budget", 30000),
            currency=st.session_state.get("budget_currency", "TWD"),
            flight_prefs=flight_prefs,
            hotel_prefs=hotel_prefs,
            travel_prefs=travel_prefs,
        )

    def render_sidebar(self):
        with st.sidebar:
            self._render_settings_section()
            self._render_destination_section()
            self._render_budget_section()
            self._render_preferences_section()

    def _render_settings_section(self):
        with st.container(border=True):
            st.header("⚙️ Settings")
            self._language = st.selectbox(
                "Language", ["English", "日本語", "한국어", "繁體中文"], key="language"
            )

    def _render_destination_section(self):
        with st.container(border=True):
            st.header("📍 Destination & Dates")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Departure", "Taipei", key="departure")
            with col2:
                st.text_input("Destination", "Tokyo", key="destination")

            date_range = st.date_input(
                "🗓️ Travel Dates (Start - End)",
                [
                    datetime.date.today(),
                    datetime.date.today() + datetime.timedelta(days=3),
                ],
                key="date_range",
            )

            if len(date_range) == 2:
                st.session_state.start_date = date_range[0]
                st.session_state.end_date = date_range[1]

    def _render_budget_section(self):
        with st.container(border=True):
            st.header("💰 Budget")

            st.markdown("#### 🔢 Allocate Your Budget")

            col1, col2 = st.columns(2)
            with col1:
                st.number_input(
                    "Flight Budget",
                    min_value=0,
                    value=10000,
                    step=500,
                    key="flight_budget",
                )
            with col2:
                st.number_input(
                    "Hotel Budget",
                    min_value=0,
                    value=15000,
                    step=500,
                    key="hotel_budget",
                )

            col1, col2 = st.columns([2, 1])
            with col1:
                min_total_budget = st.session_state.get(
                    "flight_budget", 10000
                ) + st.session_state.get("hotel_budget", 15000)

                st.slider(
                    "Total Budget",
                    min_value=min_total_budget,
                    max_value=100000,
                    value=max(min_total_budget, 30000),
                    step=1000,
                    key="total_budget",
                )
            with col2:
                st.selectbox(
                    "Currency",
                    ["USD", "EUR", "JPY", "GBP", "AUD", "TWD"],
                    key="budget_currency",
                )

            remaining_budget = st.session_state.get("total_budget", 30000) - (
                st.session_state.get("flight_budget", 10000)
                + st.session_state.get("hotel_budget", 15000)
            )
            st.success(f"✅ Remaining Budget: {remaining_budget}")

    def _render_preferences_section(self):
        with st.container(border=True):
            st.header("✨ Personalization")

            col1, col2 = st.columns(2)
            with col1:
                st.radio(
                    "Traveling With",
                    ["Solo", "Couple", "Family", "Friends", "Business"],
                    horizontal=True,
                    key="travel_companions",
                )
            with col2:
                st.selectbox(
                    "Preferred Transportation",
                    [
                        "Public Transport",
                        "Taxi/Car-hailing",
                        "Car Rental",
                        "Walking Only",
                    ],
                    key="transportation",
                )

            st.multiselect(
                "Travel Style",
                [
                    "Relaxed & Chill 😌",
                    "Adventurous 🧷",
                    "Cultural & Historical 🏛️",
                    "Luxury 💎",
                    "Backpacking 🎒",
                    "Family-Friendly 👨‍👩‍👧‍👦",
                    "Romantic 💖",
                    "Party & Nightlife 🎉",
                    "Eco & Nature 🌿",
                ],
                default=["Relaxed & Chill 😌", "Luxury 💎"],
                key="travel_style",
            )

            col3, col4 = st.columns(2)
            with col3:
                st.multiselect(
                    "Dietary Needs",
                    [
                        "None",
                        "Vegetarian",
                        "Vegan",
                        "Halal",
                        "Kosher",
                        "Gluten-Free",
                        "Seafood Allergy",
                    ],
                    default=["None"],
                    key="dietary",
                )
            with col4:
                st.multiselect(
                    "Interests",
                    [
                        "Food 🍣",
                        "Shopping 💼",
                        "History 🌰",
                        "Nature 🌳",
                        "Nightlife 🎉",
                        "Art & Culture 🎨",
                        "Photography 📸",
                        "Theme Parks 🎡",
                        "Hot Springs ♨️",
                        "Museum 🖼️",
                        "Concert 🎶",
                        "Hiking 🦼",
                    ],
                    default=["Food 🍣"],
                    key="interests",
                )

            with st.expander("Advanced Settings"):
                st.markdown("### ✈️ Flight Preferences")
                st.radio(
                    "Flight Class",
                    ["Budget", "Economy", "Business", "First"],
                    horizontal=True,
                    key="flight_class",
                )

                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox(
                        "Flight Time",
                        ["Any", "Morning", "Afternoon", "Evening", "Red-eye"],
                        key="flight_time_pref",
                    )
                with col2:
                    st.text_input("Preferred Airline", key="airline_preference")

            col1, col2 = st.columns(2)
            with col1:
                st.checkbox("Checked Luggage", value=True, key="with_luggage")
            with col2:
                st.checkbox("Non Stop Flight", value=True, key="non_stop")

            st.markdown("### 🏨 Hotel Preferences")
            col3, col4 = st.columns(2)
            with col3:
                st.select_slider(
                    "Hotel Rating",
                    ["1★", "2★", "3★", "4★", "5★"],
                    value="3★",
                    key="hotel_stars",
                )
                st.multiselect(
                    "Hotel Features",
                    [
                        "Non-smoking",
                        "Bathtub",
                        "Breakfast Included",
                        "Near Station",
                        "Late Checkout",
                    ],
                    default=["Non-smoking", "Breakfast Included", "Near Station"],
                    key="hotel_features",
                )
            with col4:
                st.multiselect(
                    "Hotel Type",
                    ["Hotel", "Hostel", "Airbnb", "Ryokan", "Capsule", "Resort"],
                    key="hotel_type",
                )

    def render_itinerary_card(self, plan):
        # Format average per day to remove trailing zeros while keeping the thousands separator
        avg_per_day = f"{plan['avg_per_day']:,.3f}".rstrip("0").rstrip(".")

        return f"""
        <div style="
            border: 2px solid #1E90FF;
            border-radius: 30px;
            padding: 30px 25px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin: 10px auto;
            width: 100%;
            min-height: 250px;
            box-sizing: border-box;
            background-color: #ffffff;
            text-align: left;
        ">
            <h3 style="color: #1E90FF; font-size: 22px; margin-bottom: 20px; text-align: center;">
                ✨ {plan['title']}
            </h3>
            <p style="text-align: left; font-size: 16px; font-weight: bold; margin-bottom: 10px;">
                Trip Highlights:
            </p>
            <ul style="text-align: left; font-size: 14px; list-style-type: disc; margin-left: 25px; line-height: 1.6;">
                {"".join([f"<li>{spot}</li>" for spot in plan['highlights']])}
            </ul>
            <p style="text-align: left; font-size: 16px; margin-top: 20px;">
                <strong>Estimated Total Cost:</strong> NT$ {plan['total_cost']:,}
            </p>
            <p style="text-align: left; font-size: 16px;">
                <strong>Average Per Day:</strong> NT$ {avg_per_day}
            </p>
        </div>
        """

    def display_itineraries(self):
        if st.session_state.itineraries:
            # Display itinerary summaries and details
            if st.session_state.selected_plan is None:
                cols = st.columns(len(st.session_state.itineraries))
                for idx, plan in enumerate(st.session_state.itineraries):
                    with cols[idx]:
                        st.markdown(
                            self.render_itinerary_card(plan), unsafe_allow_html=True
                        )
                        if st.button(
                            f"View Details of {plan['title']}",
                            key=f"view_{idx}",
                            use_container_width=True,
                        ):
                            st.session_state.selected_plan = idx
                            # Initialize chat history with the selected plan
                            self.chat_history.clear()
                            self.chat_history.add_message(
                                "assistant", self.display_chat_itinerary(plan)
                            )
                            st.rerun()
            else:
                # Get current plan
                current_plan = st.session_state.itineraries[
                    st.session_state.selected_plan
                ]

                # Display all messages in chat history
                messages = self.chat_history.get_messages()
                for i, msg in enumerate(messages):
                    # Display the message
                    with st.chat_message(msg.role):
                        st.markdown(msg.content, unsafe_allow_html=True)

                    # If this is an assistant message and there are thoughts for this modification
                    if msg.role == "assistant" and i // 2 < len(
                        self.history.get_all_thoughts()
                    ):
                        thoughts = self.history.get_all_thoughts()[i // 2]
                        # Display the modification thoughts
                        with st.expander("🤔 Agent's Thought Process", expanded=True):
                            st.markdown("### 📝 Modification Steps")
                            for j, thought in enumerate(thoughts, 1):
                                if thought["type"] == "tool_call":
                                    st.markdown(
                                        f"{j}. {thought['emoji']} Used `{thought['tool']}` to find suitable options"
                                    )
                                    st.code(thought["args"], language="json")
                                elif thought["type"] == "reasoning":
                                    st.markdown(
                                        f"{j}. 💭 Reasoning: {thought['content']}"
                                    )

                # Display current modification UI
                st.markdown("### 🔄 Want to modify this itinerary?")
                selected_activities, modification_instruction = (
                    self.display_modification_ui(current_plan, current_date=None)
                )

                # Handle modification if user submitted
                if selected_activities and modification_instruction:
                    modified_plan = self.handle_modification_result(
                        current_plan,
                        selected_activities,
                        modification_instruction,
                    )
                    st.rerun()

    def display_modification_ui(self, plan, current_date):
        """Display the modification UI for the itinerary"""
        # Use a consistent key prefix for the session
        if "current_mod_key_prefix" not in st.session_state:
            st.session_state.current_mod_key_prefix = f"mod_{int(time.time())}"
        key_prefix = st.session_state.current_mod_key_prefix

        # Display the complete itinerary and get selected activities
        selected_activities = self.display_itinerary(plan, key_prefix=key_prefix)

        # Get modification instruction
        modification_instruction = st.text_area(
            "Describe your modification:",
            placeholder="e.g., I want to add more cultural activities or replace shopping with a museum visit.",
            key=f"{key_prefix}_custom_mod",
        )

        # Add budget consideration warning if needed
        if modification_instruction and "luxury" in modification_instruction.lower():
            current_budget = st.session_state.get("total_budget", 0)
            st.warning(
                f"⚠️ This modification might increase the total cost beyond your budget of {current_budget} {st.session_state.get('budget_currency', 'TWD')}"
            )

        # Create two columns for buttons
        col1, col2 = st.columns(2)

        # Modify button on the left
        with col1:
            modify_clicked = st.button(
                "💡 Modify Itinerary",
                key=f"{key_prefix}_modify",
                use_container_width=True,
            )

        # Back button on the right
        with col2:
            back_clicked = st.button(
                "🔙 Back to all plans",
                key=f"{key_prefix}_back",
                use_container_width=True,
            )

        if back_clicked:
            st.session_state.selected_plan = None
            self.chat_history.clear()
            st.rerun()

        if modify_clicked:
            if not selected_activities:
                st.warning("Please select at least one activity to modify.")
                return None, None
            elif not modification_instruction.strip():
                st.warning("Please provide some direction for modification.")
                return None, None
            else:
                # Generate new key prefix for next modification
                st.session_state.current_mod_key_prefix = f"mod_{int(time.time())}"
                return selected_activities, modification_instruction

        return None, None

    def display_chat_itinerary(self, plan):
        """Display itinerary in chat format with table schedule"""
        message = f"""
<div style="padding: 25px; border-radius: 12px; border: 2px solid #1E90FF; margin: 15px 0; background-color: #ffffff; box-shadow: 0 2px 8px rgba(30, 144, 255, 0.1);">
<head>
    <style type="text/css">
        .schedule-table td {{
            transition: all 0.3s ease;
            position: relative;
        }}

        .schedule-table td[data-activity]:hover {{
            background-color: #2196F3 !important;
            color: white !important;
            /* Remove the scale transform to prevent color from showing through header gaps */
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            cursor: pointer;
            z-index: 1;
        }}

        .schedule-table thead {{
            position: sticky;
            top: 0;
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
            color: white;
            z-index: 2;
        }}

        #activity-details {{
            display: none;
            position: fixed;
            background: white;
            border: 2px solid #1E90FF;
            border-radius: 8px;
            padding: 15px;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
        }}
    </style>
</head>

<div id="activity-details"></div>

<script type="text/javascript">
    document.addEventListener('DOMContentLoaded', function() {{
        const setupEventListeners = function() {{
            document.querySelectorAll('.schedule-table td[data-activity]').forEach(cell => {{
                cell.addEventListener('click', function(e) {{
                    const details = document.getElementById('activity-details');
                    if (details) {{
                        details.innerHTML = 
                            <h4 style="margin: 0 0 10px 0; color: #1E90FF;">🎯 活動詳情</h4>
                            <p style="margin: 5px 0;"><strong>活動：</strong>${{this.dataset.activity}}</p>
                            <p style="margin: 5px 0;"><strong>開始時間：</strong>${{this.dataset.startTime}}</p>
                            <p style="margin: 5px 0;"><strong>結束時間：</strong>${{this.dataset.endTime}}</p>
                            <p style="margin: 5px 0;"><strong>描述：</strong>${{this.dataset.description}}</p>
                        ;
                        
                        const rect = this.getBoundingClientRect();
                        details.style.left = rect.left + window.scrollX + 'px';
                        details.style.top = rect.bottom + window.scrollY + 10 + 'px';
                        details.style.display = 'block';
                        
                        e.stopPropagation();
                    }}
                }});
            }});
            
            document.addEventListener('click', function(e) {{
                const details = document.getElementById('activity-details');
                if (details && !details.contains(e.target)) {{
                    details.style.display = 'none';
                }}
            }});
        }};

        // 初始設置
        setupEventListeners();

        // 監聽可能的動態內容更新
        const observer = new MutationObserver(function(mutations) {{
            setupEventListeners();
        }});

        observer.observe(document.body, {{
            childList: true,
            subtree: true
        }});
    }});
</script>

<h1 style="font-size: 32px; color: #1E90FF; text-align: center; margin-bottom: 30px;">✨ {plan['title']}</h1>

💰 **Cost Summary**:
- Total Cost: NT$ {plan['total_cost']:,}
- Average Per Day: NT$ {plan['avg_per_day']:,.3f}

🌟 **Highlights**:
{chr(10).join([f"- {highlight}" for highlight in plan['highlights']])}

📅 **Daily Schedule**:

<div style="max-height: 500px; overflow-y: auto; overflow-x: auto; margin: 10px 0;">
<div style="min-width: 800px;">
<table class="schedule-table" style="width: 100%; border-collapse: collapse; text-align: center; position: relative; font-family: Arial, sans-serif;">
<thead style="position: sticky; top: 0; background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%); color: white; z-index: 2;">
<tr>
<th style="border: 1px solid #ddd; padding: 12px; min-width: 80px; width: 80px; font-size: 15px; text-transform: uppercase; letter-spacing: 1px;">Time</th>
"""
        # Get all dates and format them as MM/DD
        dates = []
        formatted_dates = []
        for day in plan["details"]:
            date = day["date"]
            dates.append(date)
            # Parse the date string (assuming format YYYY-MM-DD)
            month, day = date.split("-")[1:]
            formatted_date = f"{int(month)}/{int(day)}"
            # Add day of week
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            day_of_week = date_obj.strftime("%a")
            formatted_dates.append(
                f"{formatted_date}<br><span style='font-size: 13px; opacity: 0.9;'>{day_of_week}</span>"
            )
            message += f'<th style="border: 1px solid #ddd; padding: 12px; min-width: 200px; width: 200px; font-size: 15px; text-transform: uppercase; letter-spacing: 1px;">{formatted_dates[-1]}</th>'

        message += """
</tr>
</thead>
<tbody>
"""

        # Calculate the earliest and latest activity times
        earliest_time = "23:59"
        latest_time = "00:00"
        for day in plan["details"]:
            for activity in day["schedule"]:
                start_time = self.standardize_time_format(activity["start_time"])
                end_time = self.standardize_time_format(activity["end_time"])
                if start_time < earliest_time:
                    earliest_time = start_time
                if end_time > latest_time:
                    latest_time = end_time

        # Adjust the earliest and latest times
        earliest_hour, earliest_minute = map(int, earliest_time.split(":"))
        latest_hour, latest_minute = map(int, latest_time.split(":"))
        earliest_hour = max(0, earliest_hour - 1)
        # Remove the extra hour addition to latest_hour
        # latest_hour = min(23, latest_hour + 1)
        latest_hour = min(23, latest_hour)

        # Create time slots based on the adjusted earliest and latest times
        time_slots = []
        for hour in range(earliest_hour, latest_hour + 1):
            for minute in [0, 30]:
                time_slots.append(f"{hour:02d}:{minute:02d}")

        # Create a dictionary to store activities by date and time
        activities_by_date = {date: {} for date in dates}
        for day in plan["details"]:
            date = day["date"]
            schedule = day["schedule"]
            for activity in schedule:
                start_time = self.standardize_time_format(activity["start_time"])
                end_time = self.standardize_time_format(activity["end_time"])
                activities_by_date[date][start_time] = {
                    "activity": activity["activity"],
                    "end_time": end_time,
                    "description": activity.get("description", ""),
                }

        # Calculate rowspans
        rowspans = {date: {} for date in dates}
        for date in dates:
            for start_time, activity_info in activities_by_date[date].items():
                start_idx = time_slots.index(start_time)
                end_idx = time_slots.index(activity_info["end_time"])
                rowspan = end_idx - start_idx
                if rowspan > 0:
                    rowspans[date][start_time] = rowspan

        # Track cells that should be skipped due to rowspan
        skip_cells = {date: set() for date in dates}

        # Fill the table
        for time_slot in time_slots:
            # Format time for better readability
            hour, minute = time_slot.split(":")
            hour_int = int(hour)
            period = "AM" if hour_int < 12 else "PM"
            if hour_int == 0:
                hour_int = 12
            elif hour_int > 12:
                hour_int -= 12

            formatted_time = f"{hour_int}:{minute} {period}"

            message += "<tr>"
            # Add gradient background to time column based on time of day
            time_bg_color = self._get_time_background_color(int(hour))
            message += f"""<td style="border: 1px solid #ddd; padding: 12px; font-weight: 500; color: #2c3e50; 
                          background: {time_bg_color}; font-size: 14px;">{formatted_time}</td>"""

            for date in dates:
                if time_slot in skip_cells[date]:
                    continue

                current_activity = None
                rowspan = 1
                description = ""

                # Check if there's an activity starting at this time
                if time_slot in activities_by_date[date]:
                    activity_info = activities_by_date[date][time_slot]
                    current_activity = activity_info["activity"]
                    description = activity_info["description"]
                    if time_slot in rowspans[date]:
                        rowspan = rowspans[date][time_slot]
                        # Mark cells to skip
                        start_idx = time_slots.index(time_slot)
                        for i in range(start_idx + 1, start_idx + rowspan):
                            if i < len(time_slots):
                                skip_cells[date].add(time_slots[i])

                cell_style = "border: 1px solid #ddd; padding: 12px; font-size: 14px;"
                if current_activity:
                    cell_style += (
                        " background-color: #ebf5ff; color: #2c3e50; font-weight: 500;"
                    )
                    # Format time for display
                    display_time = f"{self.format_time_range(time_slot)} ~ {self.format_time_range(activity_info['end_time'])}"

                    # Add data attributes for the popup
                    data_attrs = f'data-activity="{current_activity}" data-start-time="{display_time}" data-end-time="{activity_info["end_time"]}" data-description="{description}"'
                else:
                    data_attrs = ""

                if rowspan > 1:
                    message += f'<td {data_attrs} style="{cell_style}" rowspan="{rowspan}">{current_activity or ""}</td>'
                else:
                    message += f'<td {data_attrs} style="{cell_style}">{current_activity or ""}</td>'

            message += "</tr>"

        message += """
</tbody>
</table>
</div>
</div>
</div>
"""
        return message

    def _get_time_background_color(self, hour: int) -> str:
        """Get background color gradient based on time of day"""
        if 6 <= hour < 12:  # Morning
            return "linear-gradient(90deg, #fff4e6 0%, #fff8f0 100%)"
        elif 12 <= hour < 18:  # Afternoon
            return "linear-gradient(90deg, #e6f3ff 0%, #f0f8ff 100%)"
        elif 18 <= hour < 22:  # Evening
            return "linear-gradient(90deg, #fff0f5 0%, #fff5fa 100%)"
        else:  # Night
            return "linear-gradient(90deg, #f5f5f5 0%, #fafafa 100%)"

    def handle_modification_result(
        self, plan, selected_activities, modification_instruction
    ):
        with st.spinner("🤔 Thinking about your modification request..."):
            try:
                # Add user's request to chat history
                user_message = (
                    "I would like to modify these activities:\n"
                    + "\n".join(
                        [
                            f"- {act['date']} {self.format_time_range(act['time'])}~{self.format_time_range(act['end_time'])} {act['activity']}"
                            for act in selected_activities
                        ]
                    )
                    + f"\n\nModification request: {modification_instruction}"
                )

                self.chat_history.add_message("user", user_message)

                # Create modification agent and modify itinerary
                modifier = ModifyItineraryAgent(self.config)
                modified_plan = modifier.modify_itinerary(
                    plan, selected_activities, modification_instruction, self.history
                )

                # Add modified itinerary to chat history
                self.chat_history.add_message(
                    "assistant", self.display_chat_itinerary(modified_plan)
                )

                # Update the current plan in session state
                if st.session_state.selected_plan is not None:
                    st.session_state.itineraries[st.session_state.selected_plan] = (
                        modified_plan
                    )

                # Clear modification form by generating a new key prefix
                st.session_state.current_mod_key_prefix = f"mod_{int(time.time())}"

                # Clear any selected checkboxes
                for key in list(st.session_state.keys()):
                    if key.startswith("mod_") and key.endswith("_custom_mod"):
                        del st.session_state[key]

                return modified_plan

            except Exception as e:
                error_message = f"❌ Error modifying itinerary: {str(e)}"
                st.error(error_message)
                self.chat_history.add_message("assistant", error_message)
                return plan

    def _generate_modification_summary(self, old_plan, new_plan, modified_activities):
        """Generate a summary of the modifications made to the plan"""
        summary = []

        # Track modified dates
        modified_dates = {act["date"] for act in modified_activities}

        for date in modified_dates:
            old_activities = [act["activity"] for act in old_plan.get(date, [])]
            new_activities = [act["activity"] for act in new_plan.get(date, [])]

            # Find differences
            removed = set(old_activities) - set(new_activities)
            added = set(new_activities) - set(old_activities)

            if removed or added:
                summary.append(f"\n📅 {date}:")
                if removed:
                    summary.append("Removed:")
                    for activity in removed:
                        summary.append(f"- ❌ {activity}")
                if added:
                    summary.append("Added:")
                    for activity in added:
                        summary.append(f"- ✨ {activity}")

        return (
            "\n".join(summary) if summary else "No changes were made to the itinerary."
        )

    def display_itinerary(self, plan, show_checkboxes=True, key_prefix=""):
        """Display the complete itinerary in a consistent format

        Args:
            plan: The itinerary plan to display
            show_checkboxes: Whether to show modification checkboxes
            key_prefix: Prefix for checkbox keys to ensure uniqueness

        Returns:
            list: List of selected activities if show_checkboxes is True, else empty list
        """
        selected_activities = []

        # Format average per day to remove trailing zeros while keeping the thousands separator
        avg_per_day = f"{plan['avg_per_day']:,.3f}".rstrip("0").rstrip(".")

        # Display plan title and cost summary
        st.markdown(f"### ✨ {plan['title']}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Total Cost:** NT$ {plan['total_cost']:,}")
        with col2:
            st.markdown(f"**Average Per Day:** NT$ {avg_per_day}")

        st.markdown("---")

        # Display schedule for each day
        for day_schedule in plan["details"]:
            with st.expander(f"📅 Date {day_schedule['date']}", expanded=True):
                # Create activities list
                activities = []
                for activity in day_schedule["schedule"]:
                    # Match emoji based on activity type
                    if any(
                        keyword in activity["activity"].lower()
                        for keyword in ["breakfast", "lunch", "dinner"]
                    ):
                        emoji = "🍽️"
                    elif any(
                        keyword in activity["activity"].lower()
                        for keyword in ["check-in", "check out"]
                    ):
                        emoji = "🛏️"
                    elif any(
                        keyword in activity["activity"].lower()
                        for keyword in ["airport", "flight"]
                    ):
                        emoji = "✈️"
                    elif any(
                        keyword in activity["activity"].lower()
                        for keyword in ["museum", "temple", "shrine", "art", "tour"]
                    ):
                        emoji = "🏛️"
                    elif any(
                        keyword in activity["activity"].lower()
                        for keyword in ["shopping", "market"]
                    ):
                        emoji = "💼️"
                    elif any(
                        keyword in activity["activity"].lower()
                        for keyword in ["onsen", "relax", "spa"]
                    ):
                        emoji = "♨️"
                    else:
                        emoji = "⏰"

                    time_range = f"{self.format_time_range(activity['start_time'])} ~ {self.format_time_range(activity['end_time'])}"

                    activities.append(
                        {
                            "time_range": time_range,
                            "activity": f"{emoji} {activity['activity']}",
                            "raw_activity": activity["activity"],
                            "time": activity["start_time"],
                            "end_time": activity["end_time"],
                            "description": activity.get("description", ""),
                        }
                    )

                # Display activities using columns layout
                for activity in activities:
                    if show_checkboxes:
                        cols = st.columns([7, 1])
                        with cols[0]:
                            st.markdown(
                                f"**{activity['time_range']}**: {activity['activity']}"
                            )
                            if activity["description"]:
                                st.markdown(f"*{activity['description']}*")
                        with cols[1]:
                            checkbox_key = f"{key_prefix}_mod_{day_schedule['date']}_{activity['raw_activity']}"

                            # Initialize the session state for this checkbox if not exists
                            if checkbox_key not in st.session_state:
                                st.session_state[checkbox_key] = False

                            # Create checkbox with the session state value
                            if st.checkbox(
                                "Modify",
                                key=checkbox_key,
                                value=st.session_state[checkbox_key],
                            ):
                                selected_activities.append(
                                    {
                                        "date": day_schedule["date"],
                                        "time": activity["time"],
                                        "end_time": activity["end_time"],
                                        "activity": activity["raw_activity"],
                                    }
                                )
                    else:
                        st.markdown(
                            f"**{activity['time_range']}**: {activity['activity']}"
                        )
                        if activity["description"]:
                            st.markdown(f"*{activity['description']}*")

        return selected_activities

    def standardize_time_format(self, time_str):
        """Standardize time string to 24-hour format (HH:MM)

        Args:
            time_str (str): Time string in various formats (e.g. "5:00 PM", "5 PM", "17:00", "08:00")

        Returns:
            str: Standardized time string in HH:MM format
        """
        try:
            # Remove extra spaces and handle special cases
            time_str = time_str.strip()
            if time_str == "(End)":
                return "23:59"

            # If already in 24-hour format (HH:MM), return as is
            if re.match(r"^([01][0-9]|2[0-3]):[0-5][0-9]$", time_str):
                return time_str

            # Remove all spaces from the string
            time_str = "".join(time_str.split())

            # Convert to uppercase for consistency
            time_str = time_str.upper()

            # Handle cases with colon
            if ":" in time_str:
                # Split time into hours and minutes with AM/PM
                match = re.match(r"(\d+):(\d+)(AM|PM)?", time_str)
                if match:
                    hours = int(match.group(1))
                    minutes = int(match.group(2))
                    meridiem = match.group(3)
                else:
                    raise ValueError(f"Invalid time format: {time_str}")
            else:
                # Handle cases without colon (e.g. "5PM")
                match = re.match(r"(\d+)(AM|PM)?", time_str)
                if match:
                    hours = int(match.group(1))
                    minutes = 0
                    meridiem = match.group(2)
                else:
                    raise ValueError(f"Invalid time format: {time_str}")

            # Convert to 24-hour format if AM/PM is present
            if meridiem:
                if meridiem == "PM" and hours < 12:
                    hours += 12
                elif meridiem == "AM" and hours == 12:
                    hours = 0

            # Ensure hours and minutes are within valid ranges
            hours = hours % 24
            minutes = minutes % 60

            # Format the time
            return f"{hours:02d}:{minutes:02d}"
        except Exception as e:
            print(f"Error formatting time {time_str}: {str(e)}")
            return time_str

    def format_time_range(self, time_str):
        """Format time range for display in 12-hour format with AM/PM

        Args:
            time_str (str): Time string in HH:MM format (24-hour)

        Returns:
            str: Formatted time string in HH:MM format (24-hour)
        """
        try:
            if time_str == "(End)":
                return time_str

            if ":" not in time_str:
                return time_str

            # Return the time string as is since we're using 24-hour format
            return time_str

        except Exception as e:
            print(f"Error formatting time {time_str}: {str(e)}")
            return time_str


class TravelApp:
    def __init__(self):
        self.ui = TravelUI()
        self.config = None
        self.planner = None

    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if "itineraries" not in st.session_state:
            st.session_state.itineraries = None
        if "selected_plan" not in st.session_state:
            st.session_state.selected_plan = None
        if "booking_done" not in st.session_state:
            st.session_state.booking_done = False
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    def setup(self):
        """Setup the application"""
        self.ui.setup_page()
        self.initialize_session_state()

    def run(self):
        """Run the application"""
        self.setup()

        # Render sidebar and get configuration
        self.ui.render_sidebar()

        # Get button text based on language
        button_text = self._get_generate_button_text()

        st.markdown(
            """
            <style>
                .stButton>button {
                    background-color: #87CEEB;
                    color: white;
                    width: 75%;  
                    padding: 20px 40px; 
                    font-size: 20px;
                    font-family: 'Arial', sans-serif;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    border-radius: 12px;
                    border: none;
                    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
                    transition: all 0.3s ease;
                    margin-top: auto;
                }

                .stButton>button:hover {
                    background-color: #5D8AA8;
                    transform: translateY(-3px);
                    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.3);
                }

                .stButton>button:focus {
                    outline: none;
                }
            </style>
        """,
            unsafe_allow_html=True,
        )
        # Handle generate button click
        # Handle button click event
        if st.button(button_text, use_container_width=True):
            # Operation when button is clicked
            self._handle_generate_click()

        # Display itineraries if available
        self.ui.display_itineraries()

    def _get_generate_button_text(self):
        """Get the generate button text based on selected language"""
        language = self.ui.get_selected_language()
        return {
            "English": "Generate Itinerary",
            "繁體中文": "生成行程",
            "日本語": "行程を生成",
            "한국어": "여행 일정 생성",
        }.get(language, "Generate Itinerary")

    def _handle_generate_click(self):
        """Handle generate button click event"""
        # Create config from UI inputs
        self.config = self.ui.get_current_config()

        # Create planner with config
        self.planner = ItineraryPlanner(self.config)

        # Generate itineraries
        itineraries = self.planner.generate_itineraries()

        # Save to session state
        st.session_state.itineraries = itineraries
        st.session_state.selected_plan = None


if __name__ == "__main__":
    app = TravelApp()
    app.run()
