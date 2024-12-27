import requests
import streamlit as st
from .config import API_BASE_URL

def fetch_events():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    try:
        response = requests.get(API_BASE_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch events: {e}")
        return []

def manage_event(data, method="POST"):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.request(method, API_BASE_URL, json=data, headers=headers)
        print(response.json())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to manage event: {e}")
        return {}

def delete_event(event_id):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.delete(f"{API_BASE_URL}/?id={event_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete event: {e}")
        return {}
