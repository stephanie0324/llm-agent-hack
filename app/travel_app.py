import streamlit as st
import datetime
from agent import create_travel_agent_graph

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

    interests = st.multiselect(
        "What are your interests? 🧐",
        ["Food 🍣", "Shopping 🛍️", "History 🏰", "Nature 🌳"],
        default=["Food 🍣"],
    )

user_input = st.text_input(
    "What do you want to ask? 💬 (e.g., Help me plan an itinerary!)"
)

if not user_input:
    st.warning("Please enter a question or request to proceed.")
else:
    days = (end_date - start_date).days + 1
    formatted_interests = ", ".join(interests)

    prompt = (
        f"I'm planning a trip to {destination} from {start_date} to {end_date}.\n"
        f"You have to use the tools to help me with the following:\n"
        f"📅 Use the get_weather tool to check the weather for each day. Pass the query as 'destination: {destination}'.\n"
        f"🗺️ Use the generate_itinerary tool to create a personalized itinerary based on the weather and interests: {formatted_interests}. Pass the query as 'destination: {destination}, days: {days}, interests: {formatted_interests}'.\n"
        f"📍 Use the search_places tool to recommend places in {destination} based on the interest '{formatted_interests}'. Pass the query as 'destination: {destination}, interest: {formatted_interests}'.\n"
        f"Please help answer the following based on these conditions:\n"
        f"- Destination: {destination} 🌏\n"
        f"- Start Date: {start_date} 📅\n"
        f"- End Date: {end_date} 📅\n"
        f"- Days: {days} 🌞\n"
        f"- Interests: {formatted_interests} 🏖️\n"
        f"- Question: {user_input} ❓\n"
        f"Weather Information Requests:\n"
        f"- Based on the given weather for each day, please plan the itinerary considering the weather conditions."
    )

    agent_graph = create_travel_agent_graph()

    with st.spinner("Your travel buddy is thinking... 🧳💭"):
        final_response = ""
        final_markdown = ""
        step_container = st.container()
        final_placeholder = st.empty()

        try:
            output_events = agent_graph.stream(
                {"messages": [{"role": "user", "content": prompt}]}
            )

            for event in output_events:
                st.write("📬 Event:", event)

                # Handle tool output
                tools = event.get("tools")
                if tools:
                    for message in tools.get("messages", []):
                        tool_content = getattr(message, "content", None)
                        if tool_content:
                            step_container.markdown(
                                f"📤 **Tool Output**:\n{tool_content}"
                            )
                            final_response += f"{tool_content}\n\n"

                # Handle final agent output
                if "agent" in event:
                    messages = event["agent"].get("messages", [])
                    if messages and hasattr(messages[-1], "content"):
                        final_markdown = messages[-1].content

            if final_markdown:
                final_placeholder.markdown("## ✅ Final Summary")
                final_placeholder.markdown(final_markdown)
            else:
                final_placeholder.warning(
                    "⚠️ No final response was received from the agent."
                )

        except Exception as e:
            st.error(f"An error occurred while getting the response: {str(e)}")
