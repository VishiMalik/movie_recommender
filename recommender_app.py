import streamlit as st
import pandas as pd

# Load data
ratings = pd.read_csv('u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
movies = pd.read_csv('u.item', sep='|', encoding='latin-1', usecols=[0, 1], names=['movie_id', 'title'])

# Merge datasets
data = pd.merge(ratings, movies, on='movie_id')
filtered_data = data.copy()

# Create user-movie matrix
filtered_matrix = filtered_data.pivot_table(index='user_id', columns='title', values='rating')

# Streamlit UI
st.title("🎬 Movie Recommender")

movie = st.selectbox("Select a movie", filtered_matrix.columns.tolist())

if st.button("Show Recommendations"):
    movie_ratings = filtered_matrix[movie]

    # Calculate correlation
    similar_movies = filtered_matrix.corrwith(movie_ratings)
    corr_df = similar_movies.to_frame(name='Correlation').dropna()

    # Add number of ratings
    rating_counts = filtered_data.groupby('title')['rating'].count()
    corr_df = corr_df.join(rating_counts.rename("Rating Count"))

    # Filter and sort
    recommendations = corr_df[corr_df['Rating Count'] > 50].sort_values('Correlation', ascending=False)

    # Display top 10
    st.subheader("Top Similar Movies:")
    for title, row in recommendations.head(10).iterrows():
        st.write(f"{title} (Similarity: {row['Correlation']:.2f})")
