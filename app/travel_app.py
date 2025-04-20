import streamlit as st
import datetime
from agent import create_travel_agent

st.set_page_config(page_title="Travel Buddy", page_icon="🧳")
st.title("🧳 Travel Buddy ✈️ - Your Personal Travel Agent")

with st.sidebar:
    destination = st.text_input("Where do you want to go? 🌍", "Tokyo")
    start_date = st.date_input(
        "Select your travel start date 📅", datetime.date.today()
    )
    end_date = st.date_input(
        "Select your travel end date 📅", start_date + datetime.timedelta(days=3)
    )

    if end_date < start_date:
        st.error(
            "End date cannot be earlier than the start date. Please select a valid range."
        )

    days = (end_date - start_date).days if end_date >= start_date else 0

    # Budget input
    st.subheader("💰 Set Your Budget (Optional)")

    budget_currency = st.selectbox(
        "Choose your budget currency 💸",
        ["USD", "EUR", "JPY", "GBP", "AUD", "TWD"],  # Removed CNY and added TWD
        index=0,
    )

    budget_amount = st.number_input(
        f"Enter your budget in {budget_currency}:", min_value=0, value=1000, step=10
    )

    # 💸 Preferences: Hotel & Flight Budget
    with st.expander("💸 Flight & Hotel Preferences (Optional)", expanded=False):
        flight_class = st.radio(
            "Select flight class:",
            ["Budget", "Economy", "Business", "First"],
            index=1,
            horizontal=True,
        )

        with_luggage = st.checkbox("Include checked luggage?", value=True)

        hotel_stars = st.select_slider(
            "Preferred hotel star rating:",
            options=["1★", "2★", "3★", "4★", "5★"],
            value="3★",
        )

    interests = st.multiselect(
        "What are your interests? 🧐",
        ["Food 🍣", "Shopping 🛍️", "History 🏰", "Nature 🌳"],
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
    days = (end_date - start_date).days + 1
    formatted_interests = ", ".join(interests)

    prompt = (
        f"I'm planning a trip to {destination} from {start_date} to {end_date}. With the budget of {budget_amount} in {budget_currency}\n"
        f"You have to use the tools to help me with the following (in language: {lang_code}):\n\n"
        f"📅 **get_weather** tool:\n"
        f"- Query: destination: {destination}, language: {lang_code}\n\n"
        f"🗺️ **generate_itinerary** tool:\n"
        f"- Query: destination: {destination}, days: {days}, interests: {formatted_interests}, language: {lang_code}\n\n"
        f"- 💡 Use the weather forecast (from get_weather) to avoid recommending places affected by bad weather (like rain or storms).\n\n"
        f"Please help answer the following based on these conditions:\n"
        f"- Destination: {destination} 🌏\n"
        f"- Start Date: {start_date} 📅\n"
        f"- End Date: {end_date} 📅\n"
        f"- Days: {days} 🌞\n"
        f"- Interests: {formatted_interests} 🏖️\n"
        f"- Language: {lang_code} 🈶\n"
        f"- Flight class: {flight_class}\n"
        f"- Include luggage: {'Yes' if with_luggage else 'No'}\n"
        f"- Hotel preference: {hotel_stars} hotel\n"
        f"- Budget: {budget_amount} {budget_currency}\n"
        f"- Question: {user_input} ❓\n\n"
    )

    agent = create_travel_agent()

    with st.spinner("Your travel buddy is thinking... 🧳💭"):
        output_box = st.empty()
        response_text = ""
        done_streaming = False  # Add a flag to indicate when streaming is done

        try:
            # Start streaming the agent's response
            for event in agent.stream(
                {"messages": [{"role": "user", "content": prompt}]}
            ):
                if "agent" in event:
                    for msg in event["agent"].get("messages", []):
                        content = getattr(msg, "content", None)

                        if content:
                            response_text += content
                            output_box.markdown(
                                response_text + "▌"
                            )  # Update with the cursor effect

                            done_streaming = True

                if done_streaming:
                    # Once the stream ends, update the output box to show the final result without cursor
                    output_box.markdown(response_text)
                    done_streaming = False  # Reset the flag

        except Exception as e:
            st.error(f"❌ Error while streaming: {str(e)}")
