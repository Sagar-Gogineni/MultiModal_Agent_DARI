import streamlit as st
from dataanalyst_agent.agent import agent_with_chat_history,config
from dataanalyst_agent.ingest import ingest_images


st.header("DARI: Data Analysis for Real-time Insights")
with st.sidebar:
    input_images=st.file_uploader('Upload screenshots or images files',type=['txt','jpg'],accept_multiple_files=True)
    if st.button("Upload"):
        ingest_images(input_images)

with st.chat_message("👩‍💻"):
    st.markdown("""I'm here to assist you.\n Upload data to get started""")

user_message=st.chat_input()

if user_message is not None:
    with st.chat_message("user"):
        st.markdown(user_message)
    with st.chat_message("👩‍💻"):
        # with st.spinner():
        response=agent_with_chat_history.invoke({"input":user_message},config)['output']
        st.markdown(response)