import streamlit as st
import os
from PIL import Image
from dataanalyst_agent.retriever import data_ingestion
# Set up the upload directory
UPLOAD_DIR = "dataanalyst_agent/data_store/images_data"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@st.cache_resource
def ingest_images(uploaded_files):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Get the file name and create the full path
            file_name = uploaded_file.name
            file_path = os.path.join(UPLOAD_DIR, file_name)
            
            # Save the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Display a success message
            # st.success(f"Saved {file_name} to {UPLOAD_DIR}")
            data_ingestion()
            st.success(f"Loaded")
            # Display the uploaded image
            # image = Image.open(uploaded_file)
            # st.image(image, caption=file_name, use_column_width=True)
