import streamlit as st
import pandas as pd
import time
from survey_generator import generate_survey_json 
from survey_generator import update_survey

# ----------------------------------------
# Simulated Functions for Dashboard Actions
# ----------------------------------------
def generate_new_questions():
    """
    Simulate the generation of new generic survey questions using AI.
    In production, this would call your LLM function (e.g., generate_survey_json)
    that accepts a list of low-confidence questions and returns new question JSON.
    """
    # Simulate processing time
    time.sleep(2)
    # Example new questions (replace with actual API calls/results)
    new_questions = [
        {
            "question": "How would you rate the efficiency of local government services?",
            "options": ["Excellent", "Good", "Average", "Poor", "Very Poor"]
        },
        {
            "question": "How satisfied are you with public transport reliability?",
            "options": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
        }
    ]
    return new_questions

def re_evaluate_new_questions():
    """
    Simulate re-evaluating the matching analysis after new questions are incorporated.
    In production, this might involve computing updated similarity or coverage metrics.
    """
    # Simulate processing time
    time.sleep(2)
    # Example evaluation results (replace with actual calculations)
    evaluation_results = pd.DataFrame({
        "Metric": ["Coverage Improvement", "Average Similarity Score"],
        "Value": [0.85, 0.92]
    })
    return evaluation_results

def get_generic_survey_template():
    """
    Simulate retrieving the current generic survey template.
    In production, this might be stored in a database, CSV file, or retrieved via an API.
    """
    template = pd.DataFrame({
        "Question": [
            "How satisfied are you with city services?",
            "How do you rate public transport quality?",
            "How safe do you feel in your neighborhood?"
        ],
        "Option 1": ["Very Satisfied", "Excellent", "Very Safe"],
        "Option 2": ["Satisfied", "Good", "Safe"],
        "Option 3": ["Neutral", "Average", "Neutral"],
        "Option 4": ["Dissatisfied", "Poor", "Unsafe"],
        "Option 5": ["Very Dissatisfied", "Very Poor", "Very Unsafe"]
    })
    return template

# ----------------------------------------
# Streamlit Page Setup
# ----------------------------------------
st.set_page_config(
    page_title="Enhanced Survey Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Enhanced Survey Dashboard")
st.markdown("""
This dashboard enables you to:
- **Generate new generic survey questions** from low-confidence items using AI.
- **Re-evaluate the matching analysis** to assess how the new questions affect coverage.
- **View the current Generic Survey Template.**
""")

# ----------------------------------------
# Layout: Add Buttons for Actions
# ----------------------------------------
col_gen, col_eval = st.columns(2)

with col_gen:
    if st.button("Generate New Questions"):
        with st.spinner("Generating new questions using AI..."):
            new_questions = generate_new_questions()
            st.success("New questions generated successfully!")
            st.markdown("### New Generic Survey Questions")
            new_questions_df = pd.DataFrame(new_questions)
            st.dataframe(new_questions_df, use_container_width=True)
    # Create a button to trigger generation of new generic questions.
    if st.button("Generate New Generic Survey Questions"):
        with st.spinner("Generating new questions..."):
            new_questions = generate_survey_json()
        
        if new_questions is not None:
            st.success("New questions generated!")
            # Display the generated questions in a table.
            new_questions_df = pd.DataFrame(new_questions)
            st.dataframe(new_questions_df, use_container_width=True)
        else:
            st.error("Failed to generate new questions. Please check the logs for errors.")

with col_eval:
    if st.button("Re-Evaluate Matching Analysis"):
        with st.spinner("Re-evaluating matching analysis..."):
            eval_results = re_evaluate_new_questions()
            st.success("Re-evaluation completed!")
            st.markdown("### Matching Analysis Evaluation")
            st.dataframe(eval_results, use_container_width=True)

# ----------------------------------------
# Display Generic Survey Template
# ----------------------------------------
st.markdown("### Generic Survey Template")
template_df = get_generic_survey_template()
st.dataframe(template_df, use_container_width=True)



import os
import pandas as pd
import streamlit as st

# def update_survey(row):
#     output_dir = "./output"
#     os.makedirs(output_dir, exist_ok=True)
#     survey_path = os.path.join(output_dir, "GenericSurvey.csv")
    
#     # Load the current template if it exists; otherwise, initialize an empty template.
#     if os.path.exists(survey_path):
#         generic_template = pd.read_csv(survey_path)
#     else:
#         generic_template = pd.DataFrame(columns=["generic_question", "option_1", "option_2", "option_3", "option_4", "option_5", "option_6", "option_7"])
    
#     new_questions_df = pd.DataFrame([row])
#     updated_survey_df = pd.concat([generic_template, new_questions_df], ignore_index=True)
#     updated_survey_df.to_csv(survey_path, index=False)
#     return True

# Example row (as a pandas Series)
example_row = pd.Series({
    "generic_question": "How satisfied are you with Surbab?",
    "option_1": "Very Satisfied",
    "option_2": "Satisfied",
    "option_3": "Neutral",
    "option_4": "Dissatisfied",
    "option_5": "Very Dissatisfied",
    "option_6": None,
    "option_7": None,
})

if st.button("Test Update"):
    update_success = update_survey(example_row)
    if update_success:
        st.success("Template updated!")
        st.write("Updated CSV content:")
        st.write(pd.read_csv("./output/GenericSurvey.csv"))
