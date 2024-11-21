import streamlit as st
from openai import OpenAI
import pymongo
from pymongo import MongoClient
from annotated_text import annotated_text, annotation
from pages import stepper

criteria_list = {
    "Requests Elaboration or Explanation": True,
    "Relevance": True,
    "Clarity of Purpose": True,
    "Conciseness": True,
    "Background/Context": False
}

stage_criteria_list = {
    "Specify your current stage": True
}

strategy_criteria_list = {
    "Specify your current strategy": True,
    "Specify your current strategy example": False
}

code_criteria_list = {
    "Copy and paste your code here": False
}

problem_criteria_list = {
    "Copy and paste the problem description here": False
}

def display():
    
    st.subheader("Improve your prompt!")
        # Analyze code to determine the stage
    initial_prompt = st.session_state.messages[0]['content']
    code_content = st.session_state.get("content", "")[-1]
    output = st.session_state.get("output", "")[-1]
    print("code_content", code_content)
    print("output", output)
    current_stage = predict_stage(initial_prompt, "", code_content, output)

    st.write(f"Based on our analysis, you are in the {current_stage} stage. Here are some suggestions to improve your prompt before asking ChatGPT:")
    st.selectbox("", ["Code Planning", "Code Writing", "Code Explanation", "Debugging Error Message", "Debugging Wrong Output"], index=["Code Planning", "Code Writing", "Code Explanation", "Debugging Error Message", "Debugging Wrong Output"].index(current_stage))
    
    st.write(initial_prompt+"<br>", unsafe_allow_html=True)
    st.session_state.stage_input = display_edit_box("What's the type of your current problem?",stage_criteria_list)
    st.session_state.strategy_input = display_edit_box("How would you like the output to be organized?",strategy_criteria_list)
    st.session_state.problem_input = display_edit_box("Copy and paste the problem description here to help AI contextualize the response!",problem_criteria_list)
    st.session_state.code_input = display_edit_box("Copy and paste your current code here ", code_criteria_list)
    
    if st.button("Query ChatGPT with the new prompt!"):
        st.session_state.display_mode = "state_3"
        st.rerun()
    return st.session_state.stage_input + "\n" +  st.session_state.strategy_input + "\n" + st.session_state.problem_input + "\n" + st.session_state.code_input 

def display_edit_box(component, criteria_list):
    """
    Display a box for each stage with its criteria and a prompt input area.
    """
    # Stage header with numbered circle
    st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 10px;'>
        <div style="background-color: #1a73e8; color: white; width: 30px; height: 30px; 
                    border-radius: 50%; display: flex; justify-content: center; 
                    align-items: center; font-weight: bold; font-size: 16px;">
        </div>
        <div style="margin-left: 10px; font-size: 20px; font-weight: bold; color: #333;">
            {component}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Display criteria as a bullet list
    st.markdown("<div style=list-style-type: none; padding-left: 0;>", unsafe_allow_html=True)
    for criterion, is_met in criteria_list.items():
        color = "green" if is_met else "red"
        st.markdown(f"""
        <div style="padding-left: 40px; font-size: 16px; color: {color}; margin-bottom: 8px;">{'✔️' if is_met else '❌'} {criterion}</li>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Text input area for the stage prompt
    text_input = st.text_area(f"Please write your {component} Prompt here", key=f"{component}_prompt")
    return text_input


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