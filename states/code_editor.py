import streamlit as st
from openai import OpenAI
import subprocess
from streamlit_ace import st_ace
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import pymongo
from pymongo import MongoClient

def display():
    language = st.selectbox("Language mode", options=LANGUAGES, index=121)
    content = st_ace(language=language, theme='xcode', min_lines=20, show_print_margin=True, key="user_code")
    if "content" not in st.session_state:
        st.session_state.content = []
    if "output" not in st.session_state:
        st.session_state.output = []
    st.session_state.content.append(content)
    st.subheader("Output")
    if language == 'python':
        with open('temp_code.py', 'w') as f:
            f.write(content)
        try:
            # Execute the Python script
            result = subprocess.run(["python3", "temp_code.py"], capture_output=True, text=True, check=True)
            output = result.stdout if hasattr(result, 'stdout') else result
            st.write(output)
            st.session_state.output.append(output)
        except subprocess.CalledProcessError as e:
            # Handle execution errors
            st.error(f"Error running the code: {e.stderr}")
            st.session_state.output.append(e.stderr)
    