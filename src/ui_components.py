import streamlit as st
from .api import manage_event, delete_event, fetch_events
from .utils import clear_session_state, upload_thumbnail

def render_sidebar(logo_path, form_data):
    with st.sidebar:
        st.image(logo_path)
        st.text_input("Event Name", form_data.get("name", ""), key="event_name_form")
        st.date_input("Event Date", form_data.get("date"), key="event_date_form")
        st.text_input("Event Location", form_data.get("location", ""), key="event_location_form")
        
        # File uploader for thumbnail
        uploaded_file = st.file_uploader("Upload Thumbnail", type=["png", "jpg", "jpeg"])
        thumbnail_url = None

        # Submit and Clear buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear"):
                clear_session_state()
                st.rerun()
        with col2:
            if st.button("Submit"):
                event_id = st.session_state.selected_event['id']
                event_name = st.session_state.event_name_form
                event_date = st.session_state.event_date_form
                event_location = st.session_state.event_location_form
                thumbnail_url = st.session_state.selected_event['thumbnail_url']

                if uploaded_file:
                    thumbnail_url = upload_thumbnail(uploaded_file)

                event_data = {
                    "id": int(event_id),
                    "name": str(event_name),
                    "date": str(event_date),
                    "location": str(event_location),
                    "thumbnail_url": str(thumbnail_url)
                }
                method = "PUT" if st.session_state.selected_event != None else "POST"
                response = manage_event(event_data, method=method)
                if response:
                    st.success("Event submitted successfully!")
                    clear_session_state()
                    st.rerun()

def render_flashcards(events):
    cols = st.columns(3)
    for idx, event in enumerate(events):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div style='border: 1px solid #ddd; padding: 5px; border-radius: 8px; height: 240px; width: 200px; display: flex; flex-direction: column; justify-content: space-between;'>
                    <img src="https://event-api-thumbnails.s3.us-east-1.amazonaws.com/{event['thumbnail_url']}.png" alt="Event Thumbnail" style="width: 100%; height: 120px; object-fit: cover; border-radius: 5px;" />
                    <div style="text-align: center; margin: 5px 0;">
                        <h4 style='font-size: 14px; margin: 2px 0;'>{event['name']}</h4>
                        <p style='font-size: 12px; margin: 2px 0;'>{event['location']}</p>
                        <p style='font-size: 12px; margin: 2px 0;'>{event['date']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            render_buttons(event)

def render_buttons(event):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Modify", key=f"select_{event['id']}"):
            st.session_state.selected_event = event
            st.rerun()
    with col2:
        if st.button("Delete", key=f"delete_{event['id']}"):
            response = delete_event(event['id'])
            if response:
                st.success("Event deleted successfully!")
                st.rerun()