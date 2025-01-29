import pandas as pd
import requests
import streamlit as st
import pickle
import os

api_key = os.getenv("API_KEY")

with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

def get_recommendation(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movies_indices = [i[0] for i in sim_scores]

    return movies['title'].iloc[movies_indices]

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path


# Streamlit UI
st.title("Movie Recommendations")

# Select a movie
selected_movie = st.selectbox("Select a movie:", movies['title'].values)

# Display movie details
if selected_movie:
    movie_data = movies[movies['title'] == selected_movie].values[0]
    poster_url = fetch_poster(movie_data[0])
    movie_description = movie_data[-2]

    # Display movie poster and description
    with st.container():
        cols = st.columns([1, 2])  # Left (1 part) | Right (2 parts)

        with cols[0]:
            st.image(poster_url, width=200)

        with cols[1]:
            st.text_area("Movie Description:", movie_description, height=270, disabled=True)

    st.write("")
    
    st.write("")

    # Display similar movies (Recommendation System)
    st.write(f"Movies similar to {selected_movie}:")
    recommendations = get_recommendation(selected_movie)

    # Display movie posters
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]
                movie_id = movies.loc[movies['title'] == movie_title, 'movie_id'].values[0]
                poster_url = fetch_poster(movie_id)
            
            with col:
                st.image(poster_url, width=130)
                st.write(movie_title)