import streamlit as st
import ast
from openai import OpenAI


def component_extraction(component, source, target, prompt, criteria_list={}):
    client = OpenAI(api_key=st.session_state.openai_api_key)

    # component extraction
    stream = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": f"You need to extract if {component} is in {source}. Do not explain the reason. Just return the extracted part of text."},
            {"role": "user", "content": f"Identify if the following target is present in the given source:\n\nSource: {source}\n\nTarget: {target}. {prompt}"}
        ]
    )
    extracted_result = stream.choices[0].message.content

    # criteria update
    stream = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": f"If the extracted result is add the content here, then the criteria should be labeled as False. If you are sure the criteria is met, update it to True. Return the updated criteria_list ONLY."},
            {"role": "user", "content": f"You need to update the values in {criteria_list} ONLY if such criteria has met by the extracted result: {extracted_result}. "}
        ]
    )
    criteria_list = stream.choices[0].message.content

    return extracted_result, ast.literal_eval(criteria_list)


def display_edit_box(component, criteria_list, current_stage, init_prompt_component=""):
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
    if component == "What's the type of your current problem?":
        st.write(f"Based on our analysis, you are in the {current_stage} stage. Here are some suggestions to improve your prompt before asking ChatGPT:")
        st.selectbox("", ["Code Planning", "Code Writing", "Code Explanation", "Debugging Error Message", "Debugging Wrong Output"], index=["Code Planning", "Code Writing", "Code Explanation", "Debugging Error Message", "Debugging Wrong Output"].index(current_stage))
    
    # Text input area for the stage prompt
    text_input = st.text_area(f"Please write your {component} Prompt here", key=f"{component}_prompt", value=init_prompt_component)
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