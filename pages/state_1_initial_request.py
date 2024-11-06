import streamlit as st
from openai import OpenAI
import pymongo
from pymongo import MongoClient

def display():
    # Set sessions states
    print("apikey", st.session_state.openai_api_key)
    client = OpenAI(api_key=st.session_state.openai_api_key)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.display_mode = "state_2"
        st.rerun()
        