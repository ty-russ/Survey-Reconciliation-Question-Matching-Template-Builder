import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np
from sklearn.manifold import TSNE
import ast
import seaborn as sns
from survey_generator import generate_new_questions
from survey_generator import update_survey
import os

def update_callback(idx, row_dict):
    try:
        update_success = update_survey(row_dict)
        if update_success:
            st.session_state[f"updated_{idx}"] = True
            st.success(f"Question updated in template")
            del st.session_state["new_questions_df"]
            load_generic_template.clear()
        else:
            st.error(f"Failed to update question")
    except Exception as e:
        st.error(f"An error occurred during update: {e}")
# ----------------------------------------
# Page Configuration
# ----------------------------------------


st.set_page_config(
    page_title="ETC Generic Survey Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
logo_path = "logo.webp"  # Replace with your logo file path or URL.
st.image(logo_path, width=200)

# ----------------------------------------
# Data Loading Functions 
# ----------------------------------------
@st.cache_data
def load_matched_questions():  
    matched_df = pd.read_csv("./output/matched_questions.csv")
    return pd.DataFrame(matched_df)
    

@st.cache_data
def load_similarity_matrix():
    similarity_scoresdf = pd.read_csv("./output/similarity_scores.csv")
    return similarity_scoresdf

@st.cache_data
def load_ranking_data():
    rankingdf = pd.read_csv("./output/ranking.csv")
    rankingdf.sort_values("Similarity_Score", ascending=False, inplace=True)
    return rankingdf

    return pd.DataFrame(rankingdf)

@st.cache_data
def load_cluster_questions():    
    clusters_df = pd.read_csv("./output/clustered_questions.csv")
    return pd.DataFrame(clusters_df)


@st.cache_data
def load_generic_template():    
    template_df = pd.read_csv("./output/GenericSurvey.csv")
    return pd.DataFrame(template_df)

@st.cache_data
def load_low_matched_questions():    
    low_df = pd.read_csv("./output/low_matched_survey_questions.csv")
    return pd.DataFrame(low_df)

@st.cache_data
def load_updated_generic_template():    
    updated_df = pd.read_csv("./output/GenericSurvey.csv")
    return pd.DataFrame(updated_df)


# ----------------------------------------
# Load Data
# ----------------------------------------
matched_questions_df = load_matched_questions()
similarity_matrix_df = load_similarity_matrix()
ranking_df = load_ranking_data()
clusters_df = load_cluster_questions()
template_df = load_generic_template()
updated_template_df = load_updated_generic_template()
low_df = load_low_matched_questions()
new_questions_df = None
filtered_generic_question = template_df

# ----------------------------------------
# Sidebar Filters
# ----------------------------------------

selected_section = st.sidebar.radio(
    "Select Filter Section", 
    options=["Rank Table", "Generic Survey Template",]
)
filtered_df=ranking_df
if selected_section == "Rank Table":
    st.sidebar.header("Filters")
    selected_confidence = st.sidebar.multiselect(
        "Select Confidence Level",
        options=ranking_df["Confidence_Level"].unique(),
        default=ranking_df["Confidence_Level"].unique()
    )
    # historical_question_filter = st.sidebar.text_input("Filter by Historical Question")

    # # Filter Historical Questions
    # filtered_historical = ranking_df[ranking_df["Confidence_Level"].isin(selected_confidence)]
    # if historical_question_filter:
    #     filtered_historical = filtered_historical[
    #         filtered_historical["Historical_Question"].str.contains(historical_question_filter, case=False)
    #     ]


      # Get a sorted list of unique generic questions from your ranking DataFrame.
    historical_question_options = sorted(ranking_df["Historical_Question"].unique().tolist())

    # Use st.multiselect (or st.selectbox) to create a searchable dropdown in the sidebar.
    selected_historical_questions = st.sidebar.multiselect(
        "Filter by Historical Question", 
        options=historical_question_options,
        help="Type to search for generic questions and select one or more"
    )

    # Filter Generic Questions by the selected confidence level first.
    filtered_historical = ranking_df[ranking_df["Confidence_Level"].isin(selected_confidence)]

    # If any generic question(s) are selected, filter the DataFrame accordingly.
    if selected_historical_questions:
        filtered_generic = filtered_historical[filtered_historical["Historical_Question"].isin(selected_historical_questions)]


    # generic_question_filter = st.sidebar.text_input("Filter by Generic Question")

    # # Filter Generic Questions 
    # filtered_generic = ranking_df[ranking_df["Confidence_Level"].isin(selected_confidence)]
    # if generic_question_filter:
    #     filtered_generic = filtered_generic[
    #         filtered_generic["Generic_Question"].str.contains(generic_question_filter, case=False)
    #     ]
        
    # Get a sorted list of unique generic questions from your ranking DataFrame.
    generic_question_options = sorted(ranking_df["Generic_Question"].unique().tolist())

    # Use st.multiselect (or st.selectbox) to create a searchable dropdown in the sidebar.
    selected_generic_questions = st.sidebar.multiselect(
        "Filter by Generic Question", 
        options=generic_question_options,
        help="Type to search for generic questions and select one or more"
    )

    # Filter Generic Questions by the selected confidence level first.
    filtered_generic = ranking_df[ranking_df["Confidence_Level"].isin(selected_confidence)]

    # If any generic question(s) are selected, filter the DataFrame accordingly.
    if selected_generic_questions:
        filtered_generic = filtered_generic[filtered_generic["Generic_Question"].isin(selected_generic_questions)]
    
    filtered_df = ranking_df[ranking_df["Confidence_Level"].isin(selected_confidence)]
    if selected_historical_questions:

        filtered_df = filtered_historical

    if selected_generic_questions:
        filtered_df = filtered_generic
        
if selected_section == "Generic Survey Template":
    st.sidebar.header("Filters")
    # generic_question_filterr = st.sidebar.text_input("Filter by Generic Question")
    # # Filter Generic Questions 
    # filtered_generic_question = template_df
    # if generic_question_filterr:
    #     filtered_generic_question = filtered_generic_question[
    #         filtered_generic_question["generic_question"].str.contains(generic_question_filterr, case=False)
    #     ]
    
      # Get a sorted list of unique generic questions from your ranking DataFrame.
    generic_question_option = sorted(template_df["generic_question"].unique().tolist())

    # Use st.multiselect (or st.selectbox) to create a searchable dropdown in the sidebar.
    selected_generic_questions = st.sidebar.multiselect(
        "Filter by Generic Question", 
        options=generic_question_option,
        help="Type to search for generic questions and select one or more"
    )

    # Filter Generic Questions by the selected confidence level first.
    filtered_generic_question = template_df

    # If any generic question(s) are selected, filter the DataFrame accordingly.
    if selected_generic_questions:
        filtered_generic_question = filtered_generic_question[filtered_generic_question["generic_question"].isin(selected_generic_questions)]

# ----------------------------------------
# Dashboard Title & Overview
# ----------------------------------------
st.title("Generic Survey Dashboard")
# st.markdown("""
# This dashboard provides an overview of generic survey questions along with similarity and ranking information.
# """)

if st.button("Refresh"):
    load_generic_template.clear()
    load_updated_generic_template.clear()
    load_matched_questions.clear()
    load_ranking_data.clear()
    st.experimental_rerun()

tabs = st.tabs(["Rank Table","Visualizations","Generic Survey Template","Generic Survey Enrichment"])



with tabs[0]:
      # ----------------------------------------
    # Ranking Section using Tabs
    # ----------------------------------------
    tabz = st.tabs(["Top 100 Matches","Middle Matches","Bottom 100 Matches"])

    n = len(filtered_df)

    # Top Matches
    with tabz[0]:
        st.markdown("### Top 100 Matches")
        if n >= 10:
            top_matches = filtered_df.head(100)
            st.dataframe(top_matches, use_container_width=True)
        else:
            st.info("Not enough data for top matches. Showing all available rows.")
            st.dataframe(filtered_df, use_container_width=True)

    # Middle Matches:
    with tabz[1]:
        st.markdown("### Middle Matches")
        if n > 20:
            middle_matches = filtered_df.iloc[100:-100]
            st.dataframe(middle_matches, use_container_width=True)
        else:
            st.info("Not enough data for middle matches.")

    # Bottom Matches: 
    with tabz[2]:
        st.markdown("### Bottom 100 Matches")
        if n >= 10:
            bottom_matches = filtered_df.tail(100)
            st.dataframe(bottom_matches, use_container_width=True)
        else:
            st.info("Not enough data for bottom matches.")

    
    st.markdown("---")

    st.markdown("### Full Ranking Table")
    st.dataframe(filtered_df, use_container_width=True)

      
with tabs[1]:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Confidence Level Comparisons")
        # Bar Chart: Average Similarity Score by Confidence Level
        conf_avg = matched_questions_df.groupby('confidence_level')['similarity_score'].mean().reset_index()
        fig_avg = px.bar(conf_avg, x='confidence_level', y='similarity_score', 
                     title="Average Similarity Score by Confidence Level", color='confidence_level')
        st.plotly_chart(fig_avg, use_container_width=True)
    with col2:
         # Group by confidence level and count the number of matches per category
        conf_count = matched_questions_df.groupby('confidence_level').size().reset_index(name='Count')

        # Create a pie chart 
        fig_pie = px.pie(
            conf_count,
            values='Count',
            names='confidence_level',
            title="Proportion of Matched Questions by Confidence Level",
            color='confidence_level',
            color_discrete_map={'High':'green', 'Medium':'orange', 'Low':'red'}
        )

        st.plotly_chart(fig_pie, use_container_width=True)
    
    # heat map: Similarity Heatmap
    st.subheader("Similarity Matrix  Heatmap")
    from sklearn.metrics.pairwise import cosine_similarity

    embeddings_list = clusters_df["sbert_embedding"].apply(ast.literal_eval).tolist()
    embeddings = np.array(embeddings_list)
    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(embeddings)
    plt.figure(figsize=(12, 5))
    sns.heatmap(similarity_matrix, cmap="coolwarm", annot=False)
    plt.title("Question Similarity Heatmap")
    st.pyplot(plt.gcf())

with tabs[2]:
    
    st.markdown("### Generic Survey Template")
    st.dataframe(filtered_generic_question, use_container_width=True)
        
with tabs[3]:
    # enrichment / refinement
    
    input_questions = st.text_area(
        "Paste/Type Questions (comma separated)",
        "What is your Age?, Rate the level of noise in your area?"
    )

   
    if st.button("Generate New Generic Question"):
      
        questions_list = [q.strip() for q in input_questions.split(",") if q.strip()]
        
        if not questions_list:
            st.error("Please enter at least one valid question.")
        else:
            with st.spinner("Generating new questions using AI..."):
                new_questions = generate_new_questions(questions_list)
            
            # Check the output and display results.
            if new_questions is not None:
                st.success("New questions generated successfully!")
                new_questions_df = pd.DataFrame(new_questions)
                st.dataframe(new_questions_df, use_container_width=True)
            else:
                st.error("Failed to generate new questions. Please check the logs for errors.")
    
    
    # ----------------------------------------
    # update the template
    # ----------------------------------------
   
    if "new_questions_df" in locals() and new_questions_df is not None and not new_questions_df.empty:
        st.markdown("##### Choose Generic Questions")
        # For demonstration, assume new_questions_df exists
        if 'new_questions_df' not in st.session_state and 'new_questions' in locals():
            st.session_state.new_questions_df = new_questions_df  # cache for later use
        
        for idx, row in st.session_state.new_questions_df.iterrows():
            # Create two columns: one for displaying question data, one for the update button.
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Question {idx}:** {row.get('generic_question')}")
                # st.write("**Options:**", row.get("option_1"), row.get("option_2"), row.get("option_3"), row.get("option_4"), row.get("option_5"), row.get("option_6"), row.get("option_7"))
            with col2:
                st.button(
                "Add To Template", 
                key=f"update_{idx}",
                on_click=update_callback,
                args=(idx, row.to_dict())
                 )
          

    # ----------------------------------------
    # Display Generic Survey Template
    # ----------------------------------------
    st.markdown("### Current Generic Survey Template")
    st.dataframe(filtered_generic_question, use_container_width=True)

    
    
st.markdown("---")

# with tabs[2]:
#     # # Bar Chart: Distribution of Ranks
#     # rank_count = matched_questions_df.groupby('Rank').size().reset_index(name='Count')
#     # fig_rank = px.bar(rank_count, x='Rank', y='Count', 
#     #                   title="Distribution of Ranks", color='Rank')
#     # st.plotly_chart(fig_rank, use_container_width=True)

         
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("Generic Survey Questions")
#     st.dataframe(filtered_generic, use_container_width=True)


    
    
 
    
    
    
# import numpy as np
# n = 500  # assume 500 questions


# st.subheader("Similarity Matrix Heatmap")

# # Sidebar: Let the user choose how many questions to display
# max_display = st.sidebar.slider(
#     "Number of Questions to Display (Rows & Columns)",
#     min_value=10,
#     max_value=min(100, n),  # limit maximum to 100 for readability
#     value=50,
#     step=5
# )

# # Subset the similarity matrix based on the user's selection
# subset_matrix = similarity_matrix_df.iloc[:max_display, :max_display]

# # Plot the heatmap for the subset
# fig = px.imshow(
#     subset_matrix,
#     text_auto=True,
#     color_continuous_scale='RdBu',
#     title=f"Question Similarity Matrix (First {max_display} Questions)"
# )

# st.plotly_chart(fig, use_container_width=True)