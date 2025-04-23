import datetime
import json
import re
import time

import streamlit as st
from agent import create_travel_agent
from mock_api import get_mock_itineraries

st.set_page_config(page_title="Travel Buddy", page_icon="✈️", layout="wide")
background_image_url = "https://c1.wallpaperflare.com/preview/447/58/538/cloudscape-texture-cloud-sky-thumbnail.jpg"
st.markdown(
    f"""
    <style>
    .header-container {{
        text-align: center;
        background: url({background_image_url}) no-repeat center center fixed; /* Background image */
        background-size: cover; /* Make the background cover the entire container */
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
    .divider {{
        border: 0;
        border-top: 3px solid #00BFFF;
        width: 60%;
        margin: 30px auto;
        opacity: 0.6;
    }}
    .footer {{
        text-align: center;
        font-size: 18px;
        font-family: 'Arial', sans-serif;
        margin-top: 40px;
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
    <div class="divider"></div>
    <div class="footer">
        Powered by <a href="https://www.streamlit.io" target="_blank" class="streamlit">Streamlit</a> & <a href="https://azure.microsoft.com" target="_blank" class="azure">Azure</a> ✨
    </div>
""",
    unsafe_allow_html=True,
)


# st.title("✈️ Travel Buddy")

# ======= set state ==========
if "itineraries" not in st.session_state:
    st.session_state.itineraries = None
if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = None
if "booking_done" not in st.session_state:
    st.session_state.booking_done = False

# Sidebar Inputs
with st.sidebar:
    with st.container(border=True):
        st.header("⚙️ Settings")
        language = st.selectbox("Language", ["English", "日本語", "한국어", "繁體中文"])
        lang_code = {
            "English": "en",
            "日本語": "ja",
            "한국어": "ko",
            "繁體中文": "zh-tw",
        }[language]

    with st.container(border=True):
        st.header("📍 Destination & Dates")
        col1, col2 = st.columns(2)
        with col1:
            departure = st.text_input("Departure", "Taipei")
        with col2:
            destination = st.text_input("Destination", "Tokyo")
        date_range = st.date_input(
            "🗓️ Travel Dates (Start - End)",
            [
                datetime.date.today(),
                datetime.date.today() + datetime.timedelta(days=3),
            ],
        )
        if len(date_range) != 2:
            st.error("Please select both a start and an end date.")
        else:
            start_date, end_date = date_range
            if end_date < start_date:
                st.error("End date cannot be earlier than the start date.")
                days = 0
            else:
                days = (end_date - start_date).days

    with st.container(border=True):
        st.header("💰 Budget")

        st.markdown("#### 🔢 Allocate Your Budget")

        col1, col2 = st.columns(2)
        with col1:
            flight_budget = st.number_input(
                "Flight Budget", min_value=0, value=10000, step=500
            )
        with col2:
            hotel_budget = st.number_input(
                "Hotel Budget", min_value=0, value=15000, step=500
            )

        # 計算最小總預算
        col1, col2 = st.columns([2, 1])
        with col1:
            min_total_budget = flight_budget + hotel_budget

            total_budget = st.slider(
                "Total Budget",
                min_value=min_total_budget,
                max_value=100000,
                value=max(min_total_budget, 30000),  # 預設值不能比 min 小
                step=1000,
            )
        with col2:
            budget_currency = st.selectbox(
                "Currency", ["USD", "EUR", "JPY", "GBP", "AUD", "TWD"]
            )

        st.success(
            f"✅ Remaining Budget: {total_budget - (flight_budget + hotel_budget)}"
        )
        with st.expander("Advanced Settings"):
            st.markdown("### ✈️ Flight Preferences")
            flight_class = st.radio(
                "Flight Class",
                ["Budget", "Economy", "Business", "First"],
                horizontal=True,
            )
            col1, col2 = st.columns(2)
            with col1:
                flight_time_pref = st.selectbox(
                    "Flight Time", ["Any", "Morning", "Afternoon", "Evening", "Red-eye"]
                )
            with col2:
                airline_preference = st.text_input("Preferred Airline")
            col1, col2 = st.columns(2)
            with col1:
                with_luggage = st.checkbox("Checked Luggage", value=True)
            with col2:
                non_stop = st.checkbox("Non Stop Flight", value=True)

            st.markdown("### 🏨 Hotel Preferences")
            col3, col4 = st.columns(2)
            with col3:
                hotel_stars = st.select_slider(
                    "Hotel Rating", ["1★", "2★", "3★", "4★", "5★"], value="3★"
                )
                hotel_features = st.multiselect(
                    "Hotel Features",
                    [
                        "Non-smoking",
                        "Bathtub",
                        "Breakfast Included",
                        "Near Station",
                        "Late Checkout",
                    ],
                    default=["Non-smoking", "Breakfast Included", "Near Station"],
                )
            with col4:
                hotel_type = st.multiselect(
                    "Hotel Type",
                    ["Hotel", "Hostel", "Airbnb", "Ryokan", "Capsule", "Resort"],
                )

    with st.container(border=True):
        st.header("✨ Personalization")

        col1, col2 = st.columns(2)
        with col1:
            travel_companions = st.radio(
                "Traveling With",
                ["Solo", "Couple", "Family", "Friends", "Business"],
                horizontal=True,
            )
        with col2:
            transportation = st.selectbox(
                "Preferred Transportation",
                ["Public Transport", "Taxi/Car-hailing", "Car Rental", "Walking Only"],
            )

        travel_style = st.multiselect(
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
        )

        col3, col4 = st.columns(2)
        with col3:
            dietary = st.multiselect(
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
            )
        with col4:
            interests = st.multiselect(
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
            )

# 根據語言設置按鈕文字
button_text = "Generate Itinerary"
if language == "繁體中文":
    button_text = "生成行程"
elif language == "日本語":
    button_text = "行程を生成"
elif language == "한국어":
    button_text = "여행 일정 생성"

# 如果按下按鈕，觸發行程生成
if st.button(button_text, use_container_width=True):
    # 呼叫 create_travel_agent 並執行後續邏輯
    agent = create_travel_agent()

    # 生成的 prompt 和處理流程
    prompt = f"""
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

    emoji_map = {
        "search_flight": "✈️",
        "search_hotel": "🏨",
        "get_weather": "⛅️",
        "search_and_generate_itinerary": "🗺️",
        "format_itinerary": "📋",
    }

    with st.spinner("🧠 Agent is reasoning..."):
        thought_block = st.expander("", expanded=True)
        progress_bar = st.progress(0)
        progress_text = thought_block.empty()

        # Initialize counter and list for tool names
        tool_call_count = 0
        function_names = []  # List to store all function names

        # Dynamically collect tool calls and display detailed output
        with thought_block:
            for event in agent.stream(
                {"messages": [{"role": "user", "content": prompt}]}
            ):
                if "agent" in event:
                    for message in event["agent"]["messages"]:
                        # Check if message contains tool calls
                        if hasattr(message, "additional_kwargs"):
                            tool_calls = getattr(message, "additional_kwargs", {}).get(
                                "tool_calls", []
                            )

                            for tool_call in tool_calls:
                                tool_name = tool_call["function"]["name"]
                                tool_args = tool_call["function"]["arguments"]
                                emoji = emoji_map.get(tool_name, "🔧")

                                with st.chat_message("assistant"):
                                    st.markdown(f"{emoji} **Calling `{tool_name}`**")
                                    st.code(tool_args, language="json")

                                # Update progress bar dynamically
                                tool_call_count += 1
                                progress = min(
                                    tool_call_count / (tool_call_count + 1), 1.0
                                )  # Dynamic counting for progress bar
                                progress_bar.progress(progress)

                        # If it is the final result, display the final output
                        if hasattr(message, "content") and message.content:
                            raw_content = message.content
                            progress_bar.progress(1.0)  # Complete
                            progress_text.text("✅ Process complete! 🎉")
                            break  # Break the loop after getting the final result

    cleaned = re.search(r"```json(.*?)```", raw_content, re.DOTALL)
    itineraries = (
        json.loads(cleaned.group(1).strip())
        if cleaned
        else json.loads(raw_content.strip())
    )

    # # 顯示結果
    # st.subheader("📝 Final Itinerary")
    # st.json(itineraries)
    # st.write(itineraries)

    # # 儲存生成的計劃
    st.session_state.itineraries = itineraries
    st.session_state.selected_plan = None

    # with st.spinner("🧠 Agent is reasoning..."):
    #     thought_block = st.expander("🧠 Agent Thought Process", expanded=True)

    #     with thought_block:
    #         st.write("🤖 Agent: Calling `get_weather` for your destination...")
    #         time.sleep(2)
    #         st.info("🌤️ Weather in Tokyo: Mostly sunny, 24°C")

    #         st.write(
    #             "🤖 Agent: Calling `search_and_generate_itinerary` with your preferences..."
    #         )
    #         progress_text = st.empty()
    #         for i in range(1, 4):
    #             time.sleep(1)
    #             progress_text.info(
    #                 f"🔍 Found {i} candidate itinerary{'...' if i < 3 else '!'}"
    #             )
    #         st.success("🗺️ All 3 itineraries generated successfully.")

    #         st.write("🤖 Agent: Calling `format_itinerary` to organize plan details...")
    #         time.sleep(1)
    #         st.success("✅ Itinerary formatting complete.")

    # # 完成後才儲存到 session_state
    # st.session_state.itineraries = get_mock_itineraries()
    # st.session_state.selected_plan = None
    # st.rerun()


if st.session_state.itineraries:
    # 顯示行程計劃的摘要，並可以查看詳情
    if st.session_state.selected_plan is None:
        cols = st.columns(len(st.session_state.itineraries))
        for idx, plan in enumerate(st.session_state.itineraries):
            with cols[idx]:
                st.markdown(
                    f"""
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
                            <strong>Average Per Day:</strong> NT$ {plan['avg_per_day']:,}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # st.markdown(f"### ✨ {plan['title']}")
                # st.markdown("**Trip Highlights:**")
                # for spot in plan["highlights"]:
                #     st.markdown(f"- {spot}")
                # st.markdown(f"**Estimated Total Cost:** NT$ {plan['total_cost']:,}")
                # st.markdown(f"**Average Per Day:** NT$ {plan['avg_per_day']:,}")
                if st.button(f"View Details of {plan['title']}", key=f"view_{idx}"):
                    st.session_state.selected_plan = idx
                    st.rerun()
    else:
        # 顯示選定的行程詳細資料
        plan = st.session_state.itineraries[st.session_state.selected_plan]
        st.markdown(f"## ✨ Detailed Itinerary: {plan['title']}")
        for day in plan["details"]:
            st.markdown(f"### 📅 Date {day['date']}")
            schedule_table = {"Time Range": [], "Activity": []}

            schedule = day["schedule"]
            for i, (start_time, item) in enumerate(schedule):
                # 決定結束時間（除最後一筆外）
                if i + 1 < len(schedule):
                    end_time = schedule[i + 1][0]
                    time_range = f"{start_time} ~ {end_time}"
                else:
                    time_range = f"{start_time} ~ (End)"

                # 配對 emoji
                if any(
                    keyword in item.lower()
                    for keyword in ["breakfast", "lunch", "dinner"]
                ):
                    emoji = "🍽️"
                elif any(
                    keyword in item.lower() for keyword in ["check-in", "check out"]
                ):
                    emoji = "🛏️"
                elif any(keyword in item.lower() for keyword in ["airport", "flight"]):
                    emoji = "✈️"
                elif any(
                    keyword in item.lower()
                    for keyword in ["museum", "temple", "shrine", "art", "tour"]
                ):
                    emoji = "🏛️"
                elif any(keyword in item.lower() for keyword in ["shopping", "market"]):
                    emoji = "💼️"
                elif any(
                    keyword in item.lower() for keyword in ["onsen", "relax", "spa"]
                ):
                    emoji = "♨️"
                else:
                    emoji = "⏰"

                schedule_table["Time Range"].append(time_range)
                schedule_table["Activity"].append(f"{emoji} {item}")

            st.table(schedule_table)

        st.markdown(f"\n**Total Cost:** NT$ {plan['total_cost']:,}")
        st.markdown(f"**Avg/Day:** NT$ {plan['avg_per_day']:,}")
        st.markdown("---")

        st.markdown(
            "🔽 Click the button below to automatically book the following items:"
        )
        st.markdown(
            """
        - 🛫 Flights (based on your preferred time and airline)
        - 🏨 Hotels (with breakfast / near train stations)
        - 🚖 Airport transfers and local transportation passes
        - 🎟️ Attraction tickets (if included in the itinerary)
        """
        )

        if not st.session_state.booking_done:
            if st.button("✅ Book All (Flights, Hotels, Transport)"):
                with st.spinner("⏳ Booking in progress... Please wait a moment."):
                    time.sleep(5)  # 模擬API請求等待時間
                st.success(
                    "🎉 Booking confirmed! All items have been successfully arranged."
                )
                st.session_state.booking_done = True
                st.rerun()
        else:
            if st.button("💳 Proceed to Payment"):
                # Simulated payment flow
                st.markdown("Please click the link below to complete your payment:")
                st.markdown(
                    "[🔗 Go to Payment Page](https://mockpayment.example.com/pay?plan_id=1234)",
                    unsafe_allow_html=True,
                )
                st.info(
                    "💡 You will receive an email confirmation once payment is complete."
                )

        if st.button("🔙 Back to all plans"):
            st.session_state.selected_plan = None
            st.rerun()
