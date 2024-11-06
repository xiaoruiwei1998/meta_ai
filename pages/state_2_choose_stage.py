import streamlit as st
from openai import OpenAI
import pymongo
from pymongo import MongoClient
from annotated_text import annotated_text, annotation

def display():
    st.subheader("Strategies")
        # Analyze code to determine the stage
    initial_prompt = st.session_state.messages[0]['content']
    code_content = st.session_state.get("content", "")[-1]
    output = st.session_state.get("output", "")[-1]
    print("code_content", code_content)
    print("output", output)
    current_stage = predict_stage(initial_prompt, "", code_content, output)

    st.write(f"You are in the {current_stage} stage. Here are some suggestions to improve your prompt before asking ChatGPT:")
    st.selectbox("", ["Code Planning", "Code Writing", "Code Explanation", "Debugging Error Message", "Debugging Wrong Output"], index=["Code Planning", "Code Writing", "Code Explanation", "Debugging Error Message", "Debugging Wrong Output"].index(current_stage))
    
    with st.chat_message("user"):
        st.write(initial_prompt+"<br>", unsafe_allow_html=True)
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


def predict_stage(initial_prompt, problem_description, code, output, client=None, approach="rule-based"):
    """
    use rule-based algorithm to predict which one of code planning, code writing, code explanation, debugging
    is the learners' help-seeking scenario
    """
    stage = "Code Planning"
    if approach == "rule-based":
        if len(code) == 0:
            stage = "Code Planning"
        elif "error" in output.lower() or "traceback" in output.lower():
            stage = "Debugging Error Message"
        elif problem_description and not code and ("explain" in problem_description.lower() or "explain" in initial_prompt.lower()):
            stage = "Code Explanation"
        else:
            stage = "Code Writing"

    # if approach == "llm-based":
    #     # Generate a response using the OpenAI API.
    #     response = client.chat.completions.create(
    #         model="gpt-4-turbo",
    #         messages=[
    #             {"role": "system", "content": "Predict which scenario the student is in from one of the following"},
    #             {"role": "user", "content": ""}
    #         ],
    #         stream=False,
    #     )
    return stage