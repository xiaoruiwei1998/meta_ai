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
        initial_prompt = annotated_text(st.session_state.messages[0]['content'], " ", 
                                    annotation("[specify stage here]","[STAGE]",font_family="Comic Sans MS", background="#FFCCCB"), 
                                    annotation("[specify strategy here]","[STRATEGY]",font_family="Comic Sans MS", background="#D9EAD3"), 
                                    annotation("[paste the problem description here]","[PROBLEM]",font_family="Comic Sans MS", background="#FFCCCB"), 
                                    annotation("[paste your current code here]","[CODE]",font_family="Comic Sans MS", background="#FFCCCB"))
    
    # suggestions on improving the prompt
    display_suggestion(suggestion_title="Which stage you are in?", suggestion_detail="Specify the stage you are in right now (e.g. debugging, planning, etc.): ", key="stage_suggestion", isExpanded=False, prompt=initial_prompt)
    display_suggestion(suggestion_title="Specify the strategy", suggestion_detail="Provide a detailed strategy for solving the problem.", key="strategy_suggestion", isExpanded=False, prompt=initial_prompt)
    display_suggestion(suggestion_title="Add problem description", suggestion_detail="Copy and paste the problem description here: ", key="problem_context_suggestion", isExpanded=False, prompt=initial_prompt)
    display_suggestion(suggestion_title="Add current code", suggestion_detail="Copy and paste your current code here: ", key="code_context_suggestion", isExpanded=False, prompt=initial_prompt)
    
    if st.button("Query ChatGPT with the new prompt!"):
        st.session_state.display_mode = "state_3"
        st.rerun()

def display_suggestion(suggestion_title, suggestion_detail, key, isExpanded, prompt):
    with st.expander(suggestion_title, expanded=isExpanded):
        comment = st.text_area(suggestion_detail, key=key)
        if comment and st.button("Submit"):
            print(prompt+suggestion_title)