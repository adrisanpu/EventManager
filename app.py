import streamlit as st
import requests
import re
from urllib.parse import urlparse, parse_qs

# App configuration
API_BASE_URL = "https://d74rfmvj5f.execute-api.us-east-1.amazonaws.com"
COGNITO_SIGN_IN_URL = "https://us-east-1fr69d5yr4.auth.us-east-1.amazoncognito.com/login?client_id=794g205l7hst4la4k1tf97hunq&response_type=token&scope=openid&redirect_uri=https://eventmanager-prtylabs.streamlit.app/"

# Function to extract token from URL fragment
def extract_token_from_url():
    query_params = st.experimental_get_query_params()
    if "access_token" in query_params:
        return query_params["access_token"][0]
    return None

# Function to clean the URL fragment and reload
def reload_without_token():
    st.experimental_set_query_params()

# --- Authentication Section ---
st.sidebar.image("static/event_manager_logo.png", width=150)
st.sidebar.title("Event Manager")
st.sidebar.info("Please sign in via Cognito to continue.")

# Check for token in session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Check URL for access token and save to session state
if not st.session_state.access_token:
    access_token = extract_token_from_url()
    if access_token:
        st.session_state.access_token = access_token
        reload_without_token()
        st.experimental_rerun()
    else:
        st.sidebar.markdown(f"[Sign In]( {COGNITO_SIGN_IN_URL} )")
        st.stop()

# --- Event Management Section ---
st.title("Event Management System")
st.subheader("Manage your events seamlessly!")

# Layout with 2 columns
col1, col2 = st.columns([2, 1])

# Function to fetch all events
def fetch_events():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{API_BASE_URL}/events", headers=headers)
    return response.json() if response.status_code == 200 else []

# Function to create/update/delete events
def post_event(data, method="POST"):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }
    return requests.request(method, f"{API_BASE_URL}/events", headers=headers, json=data)

# --- Display Events ---
with col1:
    st.header("Events")
    events = fetch_events()

    if not events:
        st.write("No events available.")
    else:
        selected_event = None
        for event in events:
            with st.expander(f"{event['name']} - {event['date']}"):
                st.write(f"**Location**: {event['location']}")
                st.write(f"**ID**: {event['id']}")
                if st.button("Edit", key=f"edit_{event['id']}"):
                    selected_event = event
                if st.button("Delete", key=f"delete_{event['id']}"):
                    post_event({"id": event["id"]}, method="DELETE")
                    st.experimental_rerun()

# --- Event Form (Create/Edit) ---
with col2:
    st.header("Event Form")
    form_data = {"id": "", "name": "", "date": "", "location": ""}

    if selected_event:
        form_data = selected_event

    with st.form("event_form", clear_on_submit=True):
        form_data["id"] = st.text_input("Event ID", value=form_data["id"])
        form_data["name"] = st.text_input("Event Name", value=form_data["name"])
        form_data["date"] = st.date_input("Event Date", value=form_data["date"])
        form_data["location"] = st.text_input("Event Location", value=form_data["location"])
        
        submitted = st.form_submit_button("Submit Event")
        if submitted:
            if form_data["id"]:
                post_event(form_data, method="PUT")
            else:
                post_event(form_data, method="POST")
            st.success("Event submitted successfully!")
            st.experimental_rerun()
