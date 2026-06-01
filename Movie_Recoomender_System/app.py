import streamlit as st 
import pickle as pkl
import pandas as pd
import requests as r
movies_dict=pkl.load(open('movies_dict1.pkl','rb'))
m=pd.DataFrame(movies_dict)
similarity=pkl.load(open('similarity.pkl','rb'))
def fetch_posters(mid):
    response=r.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(mid),verify=False)
    data=response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
def recommend(movie):
    movie_index=m[m["title"]==movie].index[0]
    similarity_scores=similarity[movie_index]
    similar_movies=sorted(list(enumerate(similarity_scores)),reverse=True,key=lambda x:x[1])[1:6]
    l=[]
    posters=[]
    for i in similar_movies:
        posters.append(fetch_posters(m.iloc[i[0]].movie_id))
        l.append(m.iloc[i[0]].title)
    return l,posters
def get_trailer(movie_name):

    query = movie_name.replace(" ", "+")

    return f"https://www.youtube.com/results?search_query={query}+official+trailer"
st.set_page_config(
    page_title="Movie Recommender",
    layout="wide"
)
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #000000 0%,
        #0f0f0f 30%,
        #141414 60%,
        #1a1a1a 100%
    );
    color: white;
}

/* Top glow effect */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #050505;
}

/* Movie cards */
.movie-card {
    background: rgba(30,30,30,0.85);
    backdrop-filter: blur(8px);

    padding: 12px;
    border-radius: 18px;

    box-shadow:
        0 0 10px rgba(255,0,80,0.15),
        0 0 30px rgba(0,0,0,0.6);

    transition: all 0.3s ease;
}

/* Hover ambient glow */
.movie-card:hover {

    transform: scale(1.05);

    box-shadow:
        0 0 20px rgba(255,0,80,0.45),
        0 0 40px rgba(255,0,80,0.25),
        0 0 60px rgba(255,0,80,0.15);
}

/* Movie title */
.movie-title {
    color: white;
    text-align: center;
    margin-top: 10px;
    font-size: 16px;
    font-weight: 600;
}

/* Buttons */
.stButton > button,
.stLinkButton > a {

    background: linear-gradient(
        90deg,
        #e50914,
        #ff2e63
    );

    color: white !important;

    border-radius: 12px;

    border: none;

    font-weight: bold;

    transition: 0.3s;
}

/* Button hover */
.stButton > button:hover,
.stLinkButton > a:hover {

    box-shadow:
        0 0 15px rgba(255,0,80,0.5);

    transform: scale(1.03);
}

/* Selectbox */
div[data-baseweb="select"] > div {

    background-color: #1a1a1a !important;

    border-radius: 12px;

    border: 1px solid #333;

    color: white !important;
}

/* Hide streamlit footer/menu */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

</style>
""", unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align: center;'>🎬 Movie Recommender</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: grey;'>Discover movies according to your taste</p>",
    unsafe_allow_html=True
)

st.divider()
col1, col2, col3 = st.columns([1,2,1])
with col2:
    selected_movie = st.selectbox("Which movie have you watched?",m["title"])

if st.button("Recommend"):
    with st.spinner('Finding your movies...'):
        recommended_movies, pid = recommend(selected_movie)
        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.markdown(f"""
                <style>
                .card:hover img {{
                    transform: scale(1.05);
                    transition: transform 0.3s;
                }}
                </style>

                <div class="card">
                    <img src="{pid[i]}" width="100%">
                    <p style='color:white;'>{recommended_movies[i]}</p>
                </div>
                """, unsafe_allow_html=True)
                trailer = get_trailer(recommended_movies[i])
                st.link_button(
                    "🎥 Trailer",
                    trailer,
                    use_container_width=True
                )


    st.markdown("<hr><p style='text-align:center;color:grey;'>Built by Sayandeep Guin</p>", unsafe_allow_html=True)




