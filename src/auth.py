import base64
import requests
import streamlit as st

def exchange_code_for_tokens(auth_code):
    credentials = f"{st.secrets['default']['CLIENT_ID']}:{st.secrets['default']['CLIENT_SECRET']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    data = {
        "grant_type": "authorization_code",
        "client_id": st.secrets['default']['CLIENT_ID'],
        "code": auth_code,
        "redirect_uri": st.secrets['default']['REDIRECT_URI']
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }
    response = requests.post(f"{st.secrets['default']['COGNITO_DOMAIN']}/oauth2/token", data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to exchange code for tokens.")
        st.stop()

def clear_url():
    st.query_params.clear()
