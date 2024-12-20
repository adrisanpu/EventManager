import base64
import requests
import streamlit as st
from PIL import Image

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
        print("Failed to exchange code for tokens:", response.json())
        st.error("Failed to exchange code for tokens.")
        st.stop()

# Function to clear the 'code' parameter from the URL
def clear_url():
    st.query_params.clear()
    st.experimental_set_query_params()

# Function to fetch events with the access token
def fetch_events():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(API_BASE_URL, headers=headers)
    return response.json() if response.status_code == 200 else []

# Function to manage events (create/update/delete)
def manage_event(data, method="POST"):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }
    return requests.request(method, API_BASE_URL, json=data, headers=headers)

# --- Authentication Block ---
try:
    auth_code = st.query_params.get("code")

    if "access_token" not in st.session_state or not st.session_state.access_token:
        if auth_code:
            tokens = exchange_code_for_tokens(auth_code)
            st.session_state.access_token = tokens.get("access_token")
            st.session_state.id_token = tokens.get("id_token")
            print("Access Token:", st.session_state.access_token)
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

# --- UI Components ---
# Sidebar with logo
with st.sidebar:
    logo = Image.open("static/event_manager_logo.png")
    st.image(logo, use_container_width=True)

    if "form_data" not in st.session_state:
        st.session_state.form_data = {"id": "", "name": "", "date": None, "location": ""}

    event_id = st.text_input("Event ID", st.session_state.form_data.get("id", ""))
    event_name = st.text_input("Event Name", st.session_state.form_data.get("name", ""))
    event_date = st.date_input("Event Date", st.session_state.form_data.get("date"))
    event_location = st.text_input("Event Location", st.session_state.form_data.get("location", ""))

    if st.button("Submit"):
        event_data = {
            "id": event_id,
            "name": event_name,
            "date": str(event_date),
            "location": event_location
        }
        method = "PUT" if event_id else "POST"
        manage_event(event_data, method=method)
        st.success("Event submitted successfully!")
        st.session_state.form_data = {"id": "", "name": "", "date": None, "location": ""}
        st.experimental_rerun()

# Horizontal navigation bar
nav_options = ["All Events", "Upcoming Events", "Past Events"]
selected_nav = st.selectbox("Filter Events", nav_options)

# Fetch events
events = fetch_events()

# Filter events based on navigation bar
if selected_nav == "Upcoming Events":
    events = [event for event in events if event["date"] > "2024-01-01"]  # Example filter logic
elif selected_nav == "Past Events":
    events = [event for event in events if event["date"] <= "2024-01-01"]

# Flashcard display
if not events:
    st.write("No events found.")
else:
    cols = st.columns(3)
    for idx, event in enumerate(events):
        col = cols[idx % 3]
        with col:
            st.markdown(
                f"""<div style='border: 1px solid #ddd; padding: 10px; border-radius: 8px; margin-bottom: 10px; height: 250px; width: 200px; display: flex; flex-direction: column; justify-content: space-between;'>
                <h3>{event['name']}</h3>
                <p><b>Location:</b> {event['location']}</p>
                <p><b>Date:</b> {event['date']}</p>
                <div style='display: flex; justify-content: space-between;'>
                    <button style='padding: 5px 10px; background-color: #007BFF; color: white; border: none; border-radius: 4px;' onclick="modify_event('{event['id']}')">Modify</button>
                    <button style='padding: 5px 10px; background-color: #FF0000; color: white; border: none; border-radius: 4px;'>Delete</button>
                </div>
                </div>""",
                unsafe_allow_html=True
            )

# Add JavaScript to handle Modify button functionality
st.markdown(
    """<script>
    function modify_event(event_id) {
        // Populate the form data in the sidebar
        const eventData = events.find(event => event.id === event_id);
        window.parent.postMessage({ type: 'MODIFY_EVENT', data: eventData }, '*');
    }
    </script>""",
    unsafe_allow_html=True
)
