import datetime

import streamlit as st
from agent import create_travel_agent

st.set_page_config(page_title="Travel Buddy", page_icon="👛")
st.title("👛 Travel Buddy ✈️ - Your Personal Travel Agent")

with st.sidebar:
    destination = st.text_input("Where do you want to go? 🌍", "Tokyo")
    start_date = st.date_input("Select your travel start date 🗕️", datetime.date.today())
    end_date = st.date_input(
        "Select your travel end date 🗕️", start_date + datetime.timedelta(days=3)
    )

    if end_date < start_date:
        st.error(
            "End date cannot be earlier than the start date. Please select a valid range."
        )

    days = (end_date - start_date).days if end_date >= start_date else 0

    # 💰 Budget slider
    st.subheader("💰 Set Your Budget (Optional)")
    budget_currency = st.selectbox(
        "Choose your budget currency 💸",
        ["USD", "EUR", "JPY", "GBP", "AUD", "TWD"],
        index=0,
    )
    budget_amount = st.slider(
        "Select your budget range:",
        min_value=0,
        max_value=100000,
        value=20000,
        step=1000,
    )

    # 💸 Preferences: Flight & Hotel
    with st.expander("💸 Flight & Hotel Preferences (Optional)", expanded=False):
        flight_class = st.radio(
            "Select flight class:",
            ["Budget", "Economy", "Business", "First"],
            index=1,
            horizontal=True,
        )
        airline_preference = st.text_input("Preferred airline (optional):")
        flight_time_pref = st.selectbox(
            "Preferred flight time:",
            ["Any", "Morning", "Afternoon", "Evening", "Red-eye"],
        )
        with_luggage = st.checkbox("Include checked luggage?", value=True)
        hotel_stars = st.select_slider(
            "Preferred hotel star rating:",
            options=["1★", "2★", "3★", "4★", "5★"],
            value="3★",
        )
        hotel_type = st.multiselect(
            "Preferred hotel types:",
            ["Hotel", "Hostel", "Airbnb", "Ryokan", "Capsule", "Resort"],
        )
        hotel_features = st.multiselect(
            "Hotel preferences:",
            [
                "Non-smoking",
                "Bathtub",
                "Breakfast Included",
                "Near Station",
                "Late Checkout",
            ],
        )

    st.subheader("🚀 Customize Your Travel Experience")
    travel_companions = st.radio(
        "Who are you traveling with?",
        ["Solo", "Couple", "Family", "Friends", "Business"],
        index=0,
    )
    transportation = st.selectbox(
        "Preferred transportation within the destination:",
        ["Public Transport", "Taxi/Car-hailing", "Car Rental", "Walking Only"],
    )
    dietary = st.multiselect(
        "Do you have any dietary preferences or restrictions?",
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
    interests = st.multiselect(
        "What are your interests? 🧐",
        [
            "Food 🍣",
            "Shopping 🏍️",
            "History 🏰",
            "Nature 🌳",
            "Nightlife 🎉",
            "Art & Culture 🎨",
            "Photography 📸",
            "Theme Parks 🎡",
            "Hot Springs",
            "Museum",
            "Concert",
            "Hiking",
        ],
        default=["Food 🍣"],
    )

    language = st.selectbox(
        "Choose your preferred language 🌐",
        ["English", "日本語", "한국어", "繁體中文"],
        index=0,
    )
    lang_map = {"English": "en", "日本語": "ja", "한국어": "ko", "繁體中文": "zh-tw"}
    lang_code = lang_map[language]

user_input = st.text_input(
    "What do you want to ask? 💬 (e.g., Help me plan an itinerary!)"
)

if not user_input:
    st.warning("Please enter a question or request to proceed.")
else:
    st.subheader("🧃 Recommended Travel Plans")

    # mock API response with enriched detail
    mock_itineraries = [
        {
            "title": "Cultural Explorer",
            "highlights": ["Asakusa Temple", "Ueno Museum", "Tsukiji Food Tour"],
            "total_cost": 18000,
            "avg_per_day": 3600,
            "details": [
                {
                    "day": 1,
                    "schedule": [
                        ("08:00", "Arrive at Tokyo Haneda Airport"),
                        ("09:00", "Transfer to hotel (APA Hotel Asakusa)"),
                        ("10:30", "Check-in and unpack"),
                        ("12:00", "Lunch: Local sushi at Tsukiji"),
                        ("14:00", "Visit Ueno Park & Museum"),
                        ("17:30", "Return to hotel"),
                        ("19:00", "Dinner: Ramen at Ichiran"),
                        ("21:00", "Rest at hotel"),
                    ],
                },
                {
                    "day": 2,
                    "schedule": [
                        ("08:00", "Breakfast at hotel"),
                        ("09:30", "Visit Sensoji Temple"),
                        ("12:00", "Lunch: Tempura at Daikokuya"),
                        ("14:00", "Tokyo National Museum tour"),
                        ("18:00", "Dinner: Izakaya in Asakusa"),
                        ("20:00", "Stroll along Sumida River"),
                        ("22:00", "Return to hotel"),
                    ],
                },
                {
                    "day": 3,
                    "schedule": [
                        ("08:30", "Breakfast: Hotel buffet"),
                        ("10:00", "Day trip to Ginza for shopping"),
                        ("13:00", "Lunch: Michelin-star ramen"),
                        ("15:00", "Explore Shibuya and Harajuku"),
                        ("18:30", "Dinner: Shabu-shabu"),
                        ("21:00", "Back to hotel and rest"),
                    ],
                },
                {
                    "day": 4,
                    "schedule": [
                        ("08:00", "Breakfast and check out"),
                        ("09:30", "Airport transfer"),
                        ("11:30", "Flight departs"),
                    ],
                },
            ],
        },
        {
            "title": "Nature & Relaxation",
            "highlights": ["Hakone Hot Springs", "Lake Ashi", "Scenic Hike"],
            "total_cost": 19000,
            "avg_per_day": 3800,
            "details": [
                {
                    "day": 1,
                    "schedule": [
                        ("09:00", "Depart for Hakone"),
                        ("11:30", "Check-in at Yumoto Onsen Ryokan"),
                        ("12:30", "Lunch: Kaiseki at Ryokan"),
                        ("14:00", "Relax at hot springs"),
                        ("18:00", "Dinner at Ryokan"),
                        ("20:00", "Night stroll near lake"),
                    ],
                },
                {
                    "day": 2,
                    "schedule": [
                        ("08:00", "Breakfast at Ryokan"),
                        ("09:30", "Lake Ashi cruise"),
                        ("12:00", "Lunch: Lakeside cafe"),
                        ("14:00", "Ropeway to Owakudani"),
                        ("17:00", "Return to Ryokan for dinner"),
                    ],
                },
                {
                    "day": 3,
                    "schedule": [
                        ("09:00", "Check out and hike trail to Mt. Komagatake"),
                        ("12:00", "Picnic lunch on trail"),
                        ("15:00", "Return to Tokyo"),
                    ],
                },
            ],
        },
        {
            "title": "Urban Adventure",
            "highlights": ["Shibuya Crossing", "SkyTree Tower", "Tokyo Disneyland"],
            "total_cost": 20000,
            "avg_per_day": 4000,
            "details": [
                {
                    "day": 1,
                    "schedule": [
                        ("08:00", "Arrive in Tokyo"),
                        ("09:30", "Drop luggage at hotel"),
                        ("10:30", "SkyTree Observatory"),
                        ("13:00", "Lunch: Tonkatsu"),
                        ("15:00", "Asakusa street walk"),
                        ("19:00", "Dinner and drinks in Shinjuku"),
                    ],
                },
                {
                    "day": 2,
                    "schedule": [
                        ("08:00", "Breakfast at hotel"),
                        ("09:00", "Shopping in Harajuku"),
                        ("12:00", "Lunch: Omurice"),
                        ("14:00", "Ghibli Museum"),
                        ("18:00", "Dinner: Yakitori in Ebisu"),
                    ],
                },
                {
                    "day": 3,
                    "schedule": [
                        ("07:00", "Train to Disneyland"),
                        ("09:00", "Enter Disneyland"),
                        ("12:30", "Lunch: Park cafe"),
                        ("16:00", "Parade & shopping"),
                        ("19:00", "Return to Tokyo"),
                    ],
                },
            ],
        },
    ]

    selected_plan = st.session_state.get("selected_plan", None)

    if selected_plan is None:
        cols = st.columns(len(mock_itineraries))
        for idx, plan in enumerate(mock_itineraries):
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
        plan = mock_itineraries[selected_plan]
        st.markdown(f"## ✨ Detailed Itinerary: {plan['title']}")
        for day in plan["details"]:
            st.markdown(f"### Day {day['day']}")
            for time, item in day["schedule"]:
                if any(
                    keyword in item.lower()
                    for keyword in [
                        "breakfast",
                        "lunch",
                        "dinner",
                        "ramen",
                        "sushi",
                        "tempura",
                        "shabu",
                    ]
                ):
                    emoji = "🍽️"
                elif any(
                    keyword in item.lower()
                    for keyword in ["check-in", "check out", "hotel", "rest"]
                ):
                    emoji = "🛏️"
                elif any(
                    keyword in item.lower()
                    for keyword in ["airport", "flight", "arrive", "depart"]
                ):
                    emoji = "✈️"
                elif any(
                    keyword in item.lower()
                    for keyword in [
                        "museum",
                        "temple",
                        "park",
                        "walk",
                        "shopping",
                        "tour",
                        "hike",
                    ]
                ):
                    emoji = "📍"
                elif any(
                    keyword in item.lower()
                    for keyword in ["train", "taxi", "transfer", "ropeway"]
                ):
                    emoji = "🚆"
                else:
                    emoji = "⏰"
                st.markdown(f"- {emoji} {time} → {item}")
        st.markdown(f"\n**Total Cost:** NT$ {plan['total_cost']:,}")
        st.markdown(f"**Avg/Day:** NT$ {plan['avg_per_day']:,}")
        if st.button("🔙 Back to all plans"):
            del st.session_state.selected_plan
            st.rerun()
