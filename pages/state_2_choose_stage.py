import streamlit as st
from openai import OpenAI
# import pymongo
# from pymongo import MongoClient
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
    
    # st.write(initial_prompt+"<br>", unsafe_allow_html=True)
    display_edit_box("stage_input", "[specify stage here]", "[STAGE]",stage_criteria_list)
    display_edit_box("strategy_input", "[specify strategy here]", "[STRATEGY]",strategy_criteria_list)
    display_edit_box("problem_input", "[paste the problem description here]", "[PROBLEM]",problem_criteria_list,True)
    display_edit_box("code_input", "[paste your current code here]", "[CODE]", code_criteria_list)
    
    if st.button("Query ChatGPT with the new prompt!"):
        st.session_state.display_mode = "state_3"
        st.rerun()
    return st.session_state.stage_input + "\n" +  st.session_state.strategy_input + "\n" + st.session_state.problem_input + "\n" + st.session_state.code_input 

def display_edit_box(suggestion_title, placeholder, label, criteria_list=criteria_list, is_selected=False):
    background_color = "#E8F0FE" if is_selected else "transparent"
    isCompleted = False if False in criteria_list.values() else True
    dot_color = "#4285F4" if isCompleted else "#D3D3D3"
    step_html = f"""
    <div style='display: flex; align-items: flex-start; margin-bottom: 20px; background-color: {background_color}; padding: 10px; border-radius: 8px;'>
        <div style="background-color: {dot_color}; color: white; width: 30px; height: 30px; 
                    border-radius: 50%; display: flex; justify-content: center; 
                    align-items: center; font-weight: bold; font-size: 18px;">
        </div>
        <div style="margin-left: 10px;">
            <strong style="color: #1a73e8; font-size: 16px;">{suggestion_title}</strong>
        </div>
    </div>
    """

    # Display the highlighted text in Streamlit
    st.markdown(step_html, unsafe_allow_html=True)


    html_content = "<ul style='list-style-type: none; padding-left: 0;'>"
    for criteria, isCorrect in criteria_list.items():
        # Set the color and icon based on isCorrect
        color = "green" if isCorrect else "orange"
        icon = "✔️" if isCorrect else "⚠️"
        # Create the HTML for each criteria
        html_criteria = f"""<li style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="color: {color}; font-size: 20px;">{icon}</span>
                <span style="margin-left: 8px; color: {color};">{criteria}</span>
            </li>
        """
        html_content += html_criteria
    html_content += "</ul>"

    # Display the criteria list as HTML
    st.markdown(html_content, unsafe_allow_html=True)

    annotation_text = st.text_area(
        label="",
        value="",
        key=suggestion_title,
        height=90
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