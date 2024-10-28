import streamlit as st
from openai import OpenAI
import pymongo
from pymongo import MongoClient

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
        st.markdown(st.session_state.messages[0]['content']
                    + "<br>[specify stage here]"
                    + "<br>[specify strategy here]"
                    + "<br>[paste the problem description here]"
                    + "<br>[paste your current code here]", unsafe_allow_html=True)
    
    # suggestions on improving the prompt
    with st.expander("Which stage you are in?", expanded=False):
        st.write("Specify the stage (e.g. code planning, debugging) that you are currently in.")
        comment = st.text_area("Add your comment here:", "", key="stage_comment")
        if comment:
            st.success("Comment added")
            # todo: set default bg color; change color when completed

    with st.expander("Specify the strategy", expanded=False):
        st.write("Provide a detailed strategy for solving the problem.")
        comment = st.text_area("Add your comment here:", "", key="strategy_comment")
        if comment:
            st.success("Comment added")
            # todo: set default bg color; change color when completed

    with st.expander("Add problem description", expanded=False):
        st.write("Copy and paste the problem description here: ")
        comment = st.text_area("Add your comment here:", "", key="description_comment")
        if comment:
            st.success("Comment added")

    with st.expander("Add current code", expanded=False):
        st.write("Copy and paste your current code here: ")
        comment = st.text_area("Add your comment here:", "", key="code_comment")
        if comment:
            st.success("Comment added")
    
    if st.button("Query ChatGPT with the new prompt!"):
        st.session_state.display_mode = "state_3"
        st.rerun()