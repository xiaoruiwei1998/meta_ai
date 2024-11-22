import streamlit as st
from openai import OpenAI
import pymongo
from pymongo import MongoClient
from annotated_text import annotated_text, annotation
from pages import utils

def display():
    
    st.subheader("Improve your prompt!")
        # Analyze code to determine the stage
    initial_prompt = st.session_state.messages[0]['content']
    code_content = st.session_state.get("content", "")[-1]
    output = st.session_state.get("output", "")[-1]
    print("code_content", code_content)
    print("output", output)
    current_stage = utils.predict_stage(initial_prompt, "", code_content, output)

    # component extraction

    stage_criteria_list = {
        "Specify your current stage": False
    }

    strategy_criteria_list = {
        "Specify your current strategy": False,
        "Specify your current strategy example": False
    }

    code_criteria_list = {
        "Copy and paste your code here": False
    }

    problem_criteria_list = {
        "Copy and paste the problem description here": False
    }
    init_prompt_stage, stage_criteria_list = utils.component_extraction("problem-solving stage", initial_prompt, "", "return the sentence that this student talked about where they are or the question in the response if student included. Otherwise return the text that is not code, problem description, or related to output format. Otherwise return add the content here",stage_criteria_list)
    init_prompt_strategy, strategy_criteria_list = utils.component_extraction("output format", initial_prompt, "", "return the student's description on how the output should be like (e.g. scratic question) if student included. Otherwise return \"add the content here\"",strategy_criteria_list)
    init_prompt_problem, problem_criteria_list = utils.component_extraction("problem description", initial_prompt, "", "return the programming task description in the response if student included. Otherwise return \"add the content here\"",problem_criteria_list)
    init_prompt_code, code_criteria_list = utils.component_extraction("code", initial_prompt, code_content, "return the student's code only in the response. Otherwise return \"add the content here\"",code_criteria_list)
    print(strategy_criteria_list)

    # st.write(initial_prompt+"<br>", unsafe_allow_html=True)

    st.session_state.stage_input = utils.display_edit_box("What's the type of your current problem?",stage_criteria_list, current_stage, init_prompt_stage)
    st.session_state.strategy_input = utils.display_edit_box("How would you like the output to be organized?",strategy_criteria_list, current_stage, init_prompt_strategy)
    st.session_state.problem_input = utils.display_edit_box("Copy and paste the problem description here to help AI contextualize the response!", problem_criteria_list, current_stage, init_prompt_problem)
    st.session_state.code_input = utils.display_edit_box("Copy and paste your current code here ", code_criteria_list, current_stage, init_prompt_code)
    
    if st.button("Query ChatGPT with the new prompt!"):
        st.session_state.display_mode = "state_3"
        st.rerun()
    return st.session_state.stage_input + "\n" +  st.session_state.strategy_input + "\n" + st.session_state.problem_input + "\n" + st.session_state.code_input 
