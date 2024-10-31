import streamlit as st
from openai import OpenAI
import pymongo
from pymongo import MongoClient
from annotated_text import annotated_text, annotation

def display():
    st.subheader("Strategies")
        # Analyze code to determine the stage
    code_content = st.session_state.get("content", "")
    if "def " in code_content or "class " in code_content:
        current_stage = "Code Writing"
    elif "print(" in code_content or "#" in code_content:
        current_stage = "Code Explanation"
    # elif "error" in response.lower():
    #     current_stage = "Debugging Error Message"
    # elif "unexpected output" in response.lower() or "wrong output" in response.lower():
    #     current_stage = "Debugging Wrong Output"
    else:
        current_stage = "Code Planning"

    st.write(f"You are in the {current_stage} stage. Here are some suggestions to improve your prompt before asking ChatGPT:")
    st.selectbox("", ["Code Planning", "Code Writing", "Code Explanation", "Debugging Error Message", "Debugging Wrong Output"], index=["Code Planning", "Code Writing", "Code Explanation", "Debugging Error Message", "Debugging Wrong Output"].index(current_stage))
    print(st.session_state.messages)
    
    with st.chat_message("user"):
        st.write(st.session_state.messages[0]['content']+"<br>", unsafe_allow_html=True)
        display_edit_box("stage_input", "[specify stage here]", "[STAGE]")
        display_edit_box("strategy_input", "[specify strategy here]", "[STRATEGY]")
        display_edit_box("problem_input", "[paste the problem description here]", "[PROBLEM]")
        display_edit_box("code_input", "[paste your current code here]", "[CODE]")
    
    if st.button("Query ChatGPT with the new prompt!"):
        st.session_state.display_mode = "state_3"
        st.rerun()
    return st.session_state.stage_input + "\n" +  st.session_state.strategy_input + "\n" + st.session_state.problem_input + "\n" + st.session_state.code_input 

def display_edit_box(suggestion_title, placeholder, label):
    strategy_annotated_text = annotated_text(annotation(st.session_state.get(suggestion_title, placeholder), label, font_family="Comic Sans MS", background="#FFCCCB"))
    annotation_text = st.text_input(
        label="",
        value=placeholder,
        key=suggestion_title
    )
