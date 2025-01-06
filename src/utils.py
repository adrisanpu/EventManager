import streamlit as st
import boto3
import uuid
import tempfile
import os
from PIL import Image
from .config import S3_BUCKET_NAME, S3_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY
from .api import fetch_events

def initialize_session_state():
    if "selected_event" not in st.session_state:
        st.session_state.selected_event = None
    if "form_data" not in st.session_state:
        st.session_state.form_data = {"id": "", "name": "", "date": None, "location": ""}

def get_max_id(events):
    return max(event["id"] for event in events) if events else 0

def clear_session_state():
    events = fetch_events()
    st.session_state.form_data = {"id": get_max_id(events), "name": "", "date": None, "location": ""}
    st.session_state.selected_event = None

def process_image(image_path, output_width=200, output_height=120):
    """
    Process the image by scaling and then cropping it to the desired dimensions.
    """
    with Image.open(image_path) as img:
        # Scale the image while maintaining the aspect ratio
        img.thumbnail((output_width, output_height), Image.LANCZOS)

        # Get the dimensions of the scaled image
        width, height = img.size

        # Calculate the cropping box to crop from the center
        left = (width - output_width) / 2
        top = (height - output_height) / 2
        right = (width + output_width) / 2
        bottom = (height + output_height) / 2

        # Perform the cropping
        cropped_img = img.crop((left, top, right, bottom))

        # Use tempfile to create a secure temporary file path
        temp_dir = tempfile.gettempdir()
        #create thumbnails directory if it doesn't exist
        if not os.path.exists(os.path.join(temp_dir, "thumbnails")):
            os.makedirs(os.path.join(temp_dir, "thumbnails"))
        temp_file_path = os.path.join(temp_dir, f"thumbnails\{uuid.uuid4()}.png")
        print(temp_file_path)
        cropped_img.save(temp_file_path, format="PNG")

    return temp_file_path

def upload_thumbnail(file):
    """
    Upload an image to S3 and return the public URL.
    """
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=S3_REGION
    )

    # Generate a unique filename
    file_name = uuid.uuid4()
    s3_key = f"{file_name}.png"
    temp_file_path = process_image(file)

    print(f"Uploading {temp_file_path} to {s3_key}")

    with open(temp_file_path, "rb") as data:
        s3.upload_fileobj(
            data,
            S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": "image/png"}
        )

    # Clean up the temporary file
    os.remove(temp_file_path)

    # Return the public URL
    return file_name