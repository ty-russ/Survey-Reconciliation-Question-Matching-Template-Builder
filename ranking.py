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


# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="ETC Generic Survey Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------
# Data Loading Functions (Replace with your actual data loading)
# ----------------------------------------
@st.cache_data
def load_matched_questions():  
    matched_df = pd.read_csv("./output/matched_questions.csv")
    return pd.DataFrame(matched_df)
    

@st.cache_data
def load_similarity_matrix():
    similarity_scoresdf = pd.read_csv("./output/similarity_scores.csv")
        
    # df = pd.DataFrame(data, columns=generic_questions, index=historical_questions)
    return similarity_scoresdf

@st.cache_data
def load_ranking_data():
    rankingdf = pd.read_csv("./output/ranking.csv")
    return pd.DataFrame(rankingdf)

@st.cache_data
def load_cluster_questions():    
    clusters_df = pd.read_csv("./output/clustered_questions.csv")
    return pd.DataFrame(clusters_df)
    
# ----------------------------------------
# Load Data
# ----------------------------------------
matched_questions_df = load_matched_questions()
similarity_matrix_df = load_similarity_matrix()
ranking_df = load_ranking_data()
clusters_df = load_cluster_questions()

# ----------------------------------------
# Sidebar Filters
# ----------------------------------------
st.sidebar.header("Filters")
selected_confidence = st.sidebar.multiselect(
    "Select Confidence Level",
    options=ranking_df["Confidence_Level"].unique(),
    default=ranking_df["Confidence_Level"].unique()
)

historical_question_filter = st.sidebar.text_input("Filter by Historical Question")

# Filter Historical Questions DataFrame
filtered_historical = ranking_df[ranking_df["Confidence_Level"].isin(selected_confidence)]
if historical_question_filter:
    filtered_historical = filtered_historical[
        filtered_historical["Historical_Question"].str.contains(historical_question_filter, case=False)
    ]



generic_question_filter = st.sidebar.text_input("Filter by Generic Question")

# Filter Generic Questions DataFrame
filtered_generic = ranking_df[ranking_df["Confidence_Level"].isin(selected_confidence)]
if generic_question_filter:
    filtered_generic = filtered_generic[
        filtered_generic["Generic_Question"].str.contains(generic_question_filter, case=False)
    ]




filtered_df = ranking_df[ranking_df["Confidence_Level"].isin(selected_confidence)]
if historical_question_filter:
    # Convert historical question IDs to string to support partial matching
    filtered_df = filtered_historical

if generic_question_filter:
    filtered_df = filtered_generic



# ----------------------------------------
# Dashboard Title & Overview
# ----------------------------------------
st.title("ETC Institute Towards Generic Survey Dashboard")
# st.markdown("""
# This dashboard provides an overview of generic survey questions along with similarity and ranking information.
# """)

# ----------------------------------------
# Main Layout: Two Columns
# ----------------------------------------
tabs = st.tabs(["Rank Table","Confidence Level Comparisons","Similarity Heatmap"])

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

        # Create a pie chart using Plotly Express
        fig_pie = px.pie(
            conf_count,
            values='Count',
            names='confidence_level',
            title="Proportion of Matched Questions by Confidence Level",
            color='confidence_level',
            color_discrete_map={'High':'green', 'Medium':'orange', 'Low':'red'}
        )

        st.plotly_chart(fig_pie, use_container_width=True)
    

with tabs[0]:
    
    st.markdown("### Ranking Table")
    st.dataframe(filtered_df, use_container_width=True)
    
    
    # st.markdown("---")

    # ----------------------------------------
    # Ranking Section using Tabs
    # ----------------------------------------
    # st.subheader("Historical to Generic Question Rankings")
    # tabz = st.tabs(["Top 10 Ranked Matches","Top 20 Ranked Matches","Top 50 Ranked Matches","Top 100 Ranked Matches"])

    # with tabz[0]:
    #     st.markdown("### Top 10 Ranked Matches (Rank <=10)")
    #     top_matches = filtered_df[filtered_df["Rank"] <= 10]
    #     st.dataframe(top_matches, use_container_width=True)

    # with tabz[1]:
    #     st.markdown("### Top 20 Ranked Matches (Rank <=20)")
    #     top_matches = filtered_df[filtered_df["Rank"] <= 20]
    #     st.dataframe(top_matches, use_container_width=True)

    # with tabz[2]:
    #     st.markdown("### Top 50 Ranked Matches (Rank <=50)")
    #     top_matches = filtered_df[filtered_df["Rank"] <= 50]
    #     st.dataframe(top_matches, use_container_width=True)

    # with tabz[3]:
    #     st.markdown("### Top 100 Ranked Matches (Rank <=100)")
    #     top_matches = filtered_df[filtered_df["Rank"] <= 100]
    #     st.dataframe(top_matches, use_container_width=True)   


with tabs[2]:
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
    st.pyplot(plt.gcf())  # Use st.pyplot() to render the figure in Streamlit
    


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

# with col2:
#     st.subheader("Similarity Matrix Col Heatmap")
#     from sklearn.metrics.pairwise import cosine_similarity
    
#     embeddings_list = clusters_df["sbert_embedding"].apply(ast.literal_eval).tolist()
#     embeddings = np.array(embeddings_list)
#     # Compute cosine similarity matrix
#     similarity_matrix = cosine_similarity(embeddings)

#     plt.figure(figsize=(12, 5))
#     sns.heatmap(similarity_matrix, cmap="coolwarm", annot=False)
#     plt.title("Question Similarity Heatmap")
#     st.pyplot(plt.gcf())  # Use st.pyplot() to render the figure in Streamlit

    
    
 
    
    
    
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