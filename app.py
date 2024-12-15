import base64
import requests
import streamlit as st

# Cognito App Client Information
COGNITO_DOMAIN = "https://us-east-1fr69d5yr4.auth.us-east-1.amazoncognito.com"
CLIENT_ID = "794g205l7hst4la4k1tf97hunq"
CLIENT_SECRET = "1vasb7atj21bgbh3eoueua8f07oeces2o4isvap8lmlgj2krf6qu"
REDIRECT_URI = "http://localhost:8501/"
TOKEN_ENDPOINT = f"{COGNITO_DOMAIN}/oauth2/token"

API_BASE_URL = "https://d74rfmvj5f.execute-api.us-east-1.amazonaws.com"

# Function to exchange authorization code for tokens
def exchange_code_for_tokens(auth_code):
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.post(TOKEN_ENDPOINT, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to exchange code for tokens.")
        st.stop()

# Function to get query parameters
def get_query_param(key):
    query_params = st.query_params
    return query_params.get(key)

# Layout - Centered Logo
st.markdown("<h1 style='text-align: center; margin-bottom: -30px;'>Event Manager</h1>", unsafe_allow_html=True)
st.image("static/event_manager_logo.png", width=200)

# Authentication
auth_code = get_query_param("code")
if "access_token" not in st.session_state or not st.session_state.access_token:
    if auth_code:
        tokens = exchange_code_for_tokens(auth_code)
        st.session_state.access_token = tokens.get("access_token")
        st.session_state.id_token = tokens.get("id_token")
        st.rerun()
    else:
        sign_in_url = (
            f"{COGNITO_DOMAIN}/login?"
            f"client_id={CLIENT_ID}&response_type=code&scope=openid&redirect_uri={REDIRECT_URI}"
        )
        st.markdown(f"<div style='text-align: center;'><a href='{sign_in_url}'><button style='padding: 10px 20px; font-size: 16px;'>Sign In</button></a></div>", unsafe_allow_html=True)
        st.stop()

# Functions to fetch and manage events
def fetch_events():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(API_BASE_URL, headers=headers)
    return response.json() if response.status_code == 200 else []

def manage_event(data, method="POST"):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }
    return requests.request(method, API_BASE_URL, json=data, headers=headers)

def get_next_id(events):
    if not events:
        return 1
    return max(event['id'] for event in events) + 1

# Initialize selected event
if "selected_event" not in st.session_state:
    st.session_state.selected_event = None

# Fetch events
events = fetch_events()

# Layout - 2/3 for Events, 1/3 for Form
col_events, col_form = st.columns([2, 1])

# Display Events as Flashcards
with col_events:
    st.header("Events")
    if not events:
        st.write("No events available.")
    else:
        for index, event in enumerate(events):
            st.markdown(
                f"""
                <div style='padding: 10px; margin: 10px; height: 250px; border: 1px solid #ddd; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); display: flex; flex-direction: column; justify-content: space-between;'>
                    <div>
                        <h4 style='margin: 5px 0;'>{event['name']}</h4>
                        <p style='margin: 5px 0;'>📅 Date: {event['date']}</p>
                        <p style='margin: 5px 0;'>📍 Location: {event['location']}</p>
                    </div>
                    <div style='text-align: center;'>
                        <form action="" method="post">
                            <button style='background-color: #007BFF; color: white; border: none; padding: 5px 10px; margin-right: 10px; border-radius: 5px;' 
                            onclick="document.getElementById('modify_{event['id']}').click()">Modify</button>
                            <button style='background-color: #DC3545; color: white; border: none; padding: 5px 10px; border-radius: 5px;' 
                            onclick="document.getElementById('delete_{event['id']}').click()">Delete</button>
                        </form>
                    </div>
                </div>
                """, unsafe_allow_html=True
            )
            if st.button(f"Modify {event['id']}", key=f"modify_{event['id']}"):
                st.session_state.selected_event = event
                st.rerun()
            if st.button(f"Delete {event['id']}", key=f"delete_{event['id']}"):
                manage_event({"id": event["id"]}, method="DELETE")
                st.rerun()

# Event Form for Creating/Modifying Events
with col_form:
    st.header("Create or Modify Event")
    default_event = st.session_state.selected_event or {}
    next_id = get_next_id(events) if not default_event.get("id") else default_event.get("id")

    with st.form("event_form"):
        event_id = st.text_input("Event ID (auto-generated)", value=next_id, disabled=True)
        event_name = st.text_input("Event Name", value=default_event.get("name", ""))
        event_date = st.date_input("Event Date", value=default_event.get("date", None))
        event_location = st.text_input("Event Location", value=default_event.get("location", ""))

        submitted = st.form_submit_button("Submit")
        if submitted:
            if not event_name or not event_date or not event_location:
                st.error("All fields are required!")
            else:
                event_data = {
                    "id": next_id,
                    "name": event_name,
                    "date": str(event_date),
                    "location": event_location
                }
                method = "PUT" if st.session_state.selected_event else "POST"
                manage_event(event_data, method=method)
                st.success("Event submitted successfully!")
                st.session_state.selected_event = None
                st.rerun()
