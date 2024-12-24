import streamlit as st
from auth import exchange_code_for_tokens, clear_url
from api import fetch_events, manage_event, delete_event
from ui_components import render_sidebar, render_flashcards
from utils import get_max_id
from config import COGNITO_DOMAIN, CLIENT_ID, REDIRECT_URI

# Authentication
try:
    auth_code = st.query_params.get("code")

    if "access_token" not in st.session_state or not st.session_state.access_token:
        if auth_code:
            tokens = exchange_code_for_tokens(auth_code)
            st.session_state.access_token = tokens.get("access_token")
            st.session_state.id_token = tokens.get("id_token")
            clear_url()
            st.rerun()
        else:
            sign_in_url = (
                f"{COGNITO_DOMAIN}/login?"
                f"client_id={CLIENT_ID}&response_type=code&scope=openid&redirect_uri={REDIRECT_URI}"
            )
            st.write(f"""<meta http-equiv="refresh" content="0; url={sign_in_url}" />""", unsafe_allow_html=True)
            st.stop()
except Exception as e:
    pass

# Fetch Events
events = fetch_events()

# Sidebar
if 'selected_event' not in st.session_state:
    st.session_state.selected_event = "None"

selected_event = st.session_state.selected_event

if selected_event != "None":
    event_data = next(event for event in events if event["id"] == selected_event['id'])
    form_data = {"id": event_data["id"], "name": event_data["name"], "date": event_data["date"], "location": event_data["location"]}
else:
    form_data = {"id": get_max_id(events) + 1, "name": "", "date": None, "location": ""}

render_sidebar("static/event_manager_logo.png", form_data)

# Main UI
selected_nav = st.selectbox("Filter Events", ["All Events", "Upcoming Events", "Past Events"])
filtered_events = [event for event in events if selected_nav == "All Events" or (
    selected_nav == "Upcoming Events" and event["date"] > "2024-01-01") or (
    selected_nav == "Past Events" and event["date"] <= "2024-01-01"
)]
render_flashcards(filtered_events)
