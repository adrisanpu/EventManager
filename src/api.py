import requests
import streamlit as st
from config import API_BASE_URL

def fetch_events():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(API_BASE_URL, headers=headers)
    try:
        return response.json() if response.status_code == 200 else []
    except ValueError:
        st.error("Invalid API response.")
        return []

def manage_event(data, method="POST"):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }
    response = requests.request(method, API_BASE_URL, json=data, headers=headers)
    return response

def delete_event(event_id):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }
    response = requests.delete(f"{API_BASE_URL}/?id={event_id}", headers=headers)
    return response
