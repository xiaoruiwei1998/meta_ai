import streamlit as st

def display_stepper(current_step):
    # Define steps
    steps = ["Select campaign settings", "Create an ad group", "Create an ad"]

    # Create the stepper UI using HTML and CSS
    stepper_html = """
    <div style="display: flex; justify-content: space-between; margin: 20px 0;">
    """

    for i, step in enumerate(steps):
        if i == current_step:
            stepper_html += f"""
            <div style="text-align: center;">
                <div style="background-color: #4285F4; color: white; width: 30px; height: 30px; border-radius: 50%; display: inline-flex; justify-content: center; align-items: center;">
                    {i + 1}
                </div>
                <p style="margin-top: 5px; color: #4285F4; font-weight: bold;">{step}</p>
            </div>
            """
        elif i < current_step:
            stepper_html += f"""
            <div style="text-align: center;">
                <div style="background-color: #34A853; color: white; width: 30px; height: 30px; border-radius: 50%; display: inline-flex; justify-content: center; align-items: center;">
                    {i + 1}
                </div>
                <p style="margin-top: 5px; color: #34A853;">{step}</p>
            </div>
            """
        else:
            stepper_html += f"""
            <div style="text-align: center;">
                <div style="background-color: #DADCE0; color: #9AA0A6; width: 30px; height: 30px; border-radius: 50%; display: inline-flex; justify-content: center; align-items: center;">
                    {i + 1}
                </div>
                <p style="margin-top: 5px; color: #9AA0A6;">{step}</p>
            </div>
            """

    stepper_html += "</div>"

    # Display the stepper
    st.markdown(stepper_html, unsafe_allow_html=True)

