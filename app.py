import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3cc2cb0c2e2ba75cadfbb9c67a6f4f59&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return None  # No poster path available
    except Exception as e:
        st.error(f"Error fetching poster for movie ID {movie_id}: {e}")
        return None

movies = pickle.load(open("C:/Users/venky rampeesa/Desktop/Recommendor system/movies_list.pkl", 'rb'))
similarity = pickle.load(open("C:/Users/venky rampeesa/Desktop/Recommendor system/similarity.pkl", 'rb'))

movies_list = movies['title'].values

st.header("Recommendation Engine")

import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="C:/Users/venky rampeesa/Desktop/Recommendor system/frontend/frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
]

imageUrls = [url for url in imageUrls if url is not None]  # Filter out any None URLs

imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

if st.button("Show Recommend"):
    movie_names, movie_posters = recommend(selectvalue)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(movie_names):
            with col:
                st.text(movie_names[i])
                if movie_posters[i]:
                    st.image(movie_posters[i])
                else:
                    st.write("Poster not available")
def fetch_multiple_posters(movie_ids):
    posters = []
    for movie_id in movie_ids:
        poster = fetch_poster(movie_id)
        if poster:
            posters.append(poster)
    return posters

