import streamlit as st
from api import fetch_events

def get_max_id(events):
    return max(event["id"] for event in events) if events else 0

def clear_session_state():
    events = fetch_events()
    st.session_state.form_data = {"id": get_max_id(events), "name": "", "date": None, "location": ""}
    st.session_state.selected_event = "None"