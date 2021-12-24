import pandas as pd
import streamlit as st
import pickle
import requests
from streamlit_lottie import st_lottie 


# st.markdown("![Alt Text](https://media.giphy.com/media/fh64X5Bd8RNWU/giphy.gif)")

movies_dict = pickle.load(open("movies_dict.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies = pd.DataFrame(movies_dict)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

url = "https://assets10.lottiefiles.com/private_files/lf30_is6flrfu.json"
res_json = load_lottieurl(url)
st_lottie(res_json)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path



st.title("Movie Recommendation System :popcorn:")

selected_movies_name = st.selectbox(
    "Select the name of last movie you watched  👇", movies['title'].values)

num = st.slider('Number of Movies to Recommend...', 1, 10, 5)

def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movies_index]

    movie_list = sorted([i for i in enumerate(distance)], reverse=True, key=lambda x: x[1])[1:num+1]

    recommended_movies = []
    mv_poster = []
    for i in movie_list:
        # for fetching poser from api
        movie_id = movies.iloc[i[0]].movie_id
        mv_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,mv_poster


if st.button('Recommend'):
    names,poster = recommend(selected_movies_name)
    list1 = st.columns(num)
    for i,item  in enumerate(list1):
        with item:
            st.text(names[i])
            st.image(poster[i])
