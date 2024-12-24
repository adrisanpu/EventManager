import base64
import requests
import streamlit as st
from config import TOKEN_ENDPOINT, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

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

def clear_url():
    st.query_params.clear()
