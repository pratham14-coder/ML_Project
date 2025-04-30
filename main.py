import streamlit as st
import requests

# API Key 
api_key = 'e6825812'

# Streamlit interface
st.title("Movie Search and Recommendation")

movie_title = st.text_input("Enter a movie name", "Batman")
rating_range = st.slider("Select Rating Range", 0, 10, (5, 9))

# Fetch movie data
url = f"http://www.omdbapi.com/?s={movie_title}&apikey={api_key}"
response = requests.get(url)
data = response.json()

if data["Response"] == "True":
    movies = data["Search"]
    movie_list = []
    
    for movie in movies:
        title = movie["Title"]
        year = movie["Year"]
        imdb_id = movie["imdbID"]
        poster = movie["Poster"]
        
        # Fetch IMDb rating for each movie
        movie_detail_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
        movie_detail_response = requests.get(movie_detail_url)
        movie_detail_data = movie_detail_response.json()
        rating = float(movie_detail_data["imdbRating"])
        
        if rating_range[0] <= rating <= rating_range[1]:
            movie_list.append({
                "Title": title,
                "Year": year,
                "Rating": rating,
                "Poster": poster
            })
    
    if movie_list:
        for movie in movie_list:
            st.subheader(f"{movie['Title']} ({movie['Year']})")
            st.image(movie['Poster'])
            st.write(f"Rating: {movie['Rating']}")
    else:
        st.write("No movies found within the selected rating range.")
else:
    st.write("Error fetching data. Please try again.")

