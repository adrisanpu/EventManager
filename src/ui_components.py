import streamlit as st
from api import manage_event, delete_event
from utils import get_max_id, clear_session_state

def render_sidebar(logo_path, form_data):
    with st.sidebar:
        st.image(logo_path)
        st.text_input("Event ID", form_data.get("id", ""), disabled=True, key="event_id_form")
        st.text_input("Event Name", form_data.get("name", ""), key="event_name_form")
        st.date_input("Event Date", form_data.get("date"), key="event_date_form")
        st.text_input("Event Location", form_data.get("location", ""), key="event_location_form")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear"):
                clear_session_state()
                st.rerun()
        with col2:
            if st.button("Submit"):
                event_id = st.session_state.event_id_form
                event_name = st.session_state.event_name_form
                event_date = st.session_state.event_date_form
                event_location = st.session_state.event_location_form

                print(st.session_state.selected_event)

                event_data = {
                    "id": int(event_id),
                    "name": str(event_name),
                    "date": str(event_date),
                    "location": str(event_location)
                }
                method = "PUT" if st.session_state.selected_event != "None" else "POST"
                print(method)
                response = manage_event(event_data, method=method)
                print(response.json())
                st.success("Event submitted successfully!")
                clear_session_state()
                st.rerun()

def render_flashcards(events):
    cols = st.columns(3)
    for idx, event in enumerate(events):
        with cols[idx % 3]:
            st.markdown(
                f"""<div style='border: 1px solid #ddd; padding: 10px; border-radius: 8px; height: 200px; width: 200px; display: flex; flex-direction: column; justify-content: space-between;'>
                <h3>{event['name']}</h3>
                <p><b>Location:</b> {event['location']}</p>
                <p><b>Date:</b> {event['date']}</p>
                </div>""",
                unsafe_allow_html=True
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Modify", key=f"select_{event['id']}"):
                    st.session_state.selected_event = event
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"delete_{event['id']}"):
                    print(event['id'])
                    response = delete_event(event['id'])
                    print(response.json())
                    st.success("Event deleted successfully!")
                    clear_session_state()
                    st.rerun()