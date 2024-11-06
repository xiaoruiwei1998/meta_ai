import streamlit as st

# Login Page
def login():
    st.title("Login")
    username = st.text_input("Username")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    login_button = st.button("Login")

    if login_button:
        if username and openai_api_key:
            st.session_state["username"] = username
            st.session_state["openai_api_key"] = openai_api_key
            st.session_state["logged_in"] = True
            st.rerun()  # Redirect to the main page
        else:
            st.error("Please enter both username and API key")
