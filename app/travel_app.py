import json
import re
import datetime
import streamlit as st
from agent import create_travel_agent

st.set_page_config(page_title="Travel Buddy", page_icon="💼")
st.title("💼 Travel Buddy ✈️ - Your Personal Travel Agent")

# ======= set state ==========
if "itineraries" not in st.session_state:
    st.session_state.itineraries = None
if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = None

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
            destination = st.text_input("Destination", "Tokyo")
        with col2:
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
if st.button(button_text):
    # 呼叫 create_travel_agent 並執行後續邏輯
    agent = create_travel_agent()

    # 生成的 prompt 和處理流程
    prompt = f"""
    Please help plan a personalized itinerary with the following information:
    
    Total Days: {days}
    Destination: {destination}
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
    You need to use format_itinerary to return the result in json format and only the json format.
    """
    response = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    # 解析回應並儲存
    raw_content = response["messages"][-1].content
    cleaned = re.search(r"```json(.*?)```", raw_content, re.DOTALL)
    itineraries = (
        json.loads(cleaned.group(1).strip())
        if cleaned
        else json.loads(raw_content.strip())
    )

    # 儲存生成的計劃
    st.session_state.itineraries = itineraries
    st.session_state.selected_plan = None


if st.session_state.itineraries:
    # 顯示行程計劃的摘要，並可以查看詳情
    if st.session_state.selected_plan is None:
        cols = st.columns(len(st.session_state.itineraries))
        for idx, plan in enumerate(st.session_state.itineraries):
            with cols[idx]:
                st.markdown(f"### ✨ {plan['title']}")
                st.markdown("**Trip Highlights:**")
                for spot in plan["highlights"]:
                    st.markdown(f"- {spot}")
                st.markdown(f"**Estimated Total Cost:** NT$ {plan['total_cost']:,}")
                st.markdown(f"**Average Per Day:** NT$ {plan['avg_per_day']:,}")
                if st.button(f"View Details of {plan['title']}", key=f"view_{idx}"):
                    st.session_state.selected_plan = idx
                    st.rerun()
    else:
        # 顯示選定的行程詳細資料
        plan = st.session_state.itineraries[st.session_state.selected_plan]
        st.markdown(f"## ✨ Detailed Itinerary: {plan['title']}")
        for day in plan["details"]:
            st.markdown(f"### Day {day['day']}")
            for time, item in day["schedule"]:
                emoji = "⏰"  # Default emoji
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
                st.markdown(f"- {emoji} {time} → {item}")
        st.markdown(f"\n**Total Cost:** NT$ {plan['total_cost']:,}")
        st.markdown(f"**Avg/Day:** NT$ {plan['avg_per_day']:,}")
        if st.button("🔙 Back to all plans"):
            st.session_state.selected_plan = None
            st.rerun()
