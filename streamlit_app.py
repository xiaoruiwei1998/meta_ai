import streamlit as st
from openai import OpenAI
import subprocess
from streamlit_ace import st_ace
import pymongo
from pymongo import MongoClient
from states import state_1_initial_request, state_2_choose_stage, state_3_query_gpt, code_editor

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)


# Set the page layout
# st.set_page_config(layout="wide")

# # Connect to MongoDB
# client = MongoClient("mongodb+srv://Dev-Ruiwei:Xrw1998!!!@quickta.kwa5tjq.mongodb.net/")
# db = client["test"]
# collection = db["activity_logs"]

# if "display_mode" not in st.session_state:
#     st.session_state.display_mode = "state_1"

# if st.session_state.display_mode == "state_1":
#     col1, col2 = st.columns([1, 1])
# elif st.session_state.display_mode == "state_2":
#     col1, col2 = st.columns([2, 1])
# else: 
#     col1, col2 = st.columns([1, 1])

# with col1:
#     st.subheader("Description")
#     st.write("""
# In this lab, you will develop a program that allows two players to play Tic-Tac-Toe. Players alternate placing their marks, X's and O's, respectively in the cells of a 3×3 grid. The first player to place three of their marks in a vertical, horizontal, or diagonal line is the winner. If no lines are formed, the game ends in a tie.
# """)
#     if st.session_state.display_mode == "state_1":
#         state_1_initial_request.display()
#     elif st.session_state.display_mode == "state_2":
#         st.session_state.iterated_prompt = state_2_choose_stage.display()
#     else: 
#         state_3_query_gpt.display(st.session_state.iterated_prompt)
    
# with col2:
#     # Editor section
#     st.subheader("Code Editor")
#     code_editor.display()
    



    
