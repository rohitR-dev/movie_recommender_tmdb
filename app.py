import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f132690ed8c60cd365f2910d44d247bc&language=en-US')
        data = response.json()
        return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception as e:
        return None  # Return None if there's an error

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)

    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            if poster:
                st.image(poster)
            else:
                st.write("Poster not available")
