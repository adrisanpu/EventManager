import base64
import requests
import streamlit as st

def exchange_code_for_tokens(auth_code):
    credentials = f"{st.secrets['CLIENT_ID']}:{st.secrets['CLIENT_SECRET']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    data = {
        "grant_type": "authorization_code",
        "client_id": st.secrets['CLIENT_ID'],
        "code": auth_code,
        "redirect_uri": st.secrets['REDIRECT_URI']
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.post(st.secrets['TOKEN_ENDPOINT'], data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to exchange code for tokens.")
        st.stop()

def clear_url():
    st.query_params.clear()
