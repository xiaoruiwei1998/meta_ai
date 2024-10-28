import streamlit as st
from openai import OpenAI
import pymongo
from pymongo import MongoClient

def display():
    print(st.session_state.messages)
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        for message in st.session_state.messages[1:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Generate a response using the OpenAI API.
        client = OpenAI(api_key=st.session_state.openai_api_key)
        stream = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using st.write_stream, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
