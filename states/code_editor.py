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
   
    st.subheader("Output")
    if language == 'python':
        with open('temp_code.py', 'w') as f:
            f.write(content)
        result = subprocess.run(["python3", "temp_code.py"], capture_output=True, text=True, check=True)
        st.write(result.stdout if hasattr(result, 'stdout') else result)
        
    # else:  # todo: add more languages
    