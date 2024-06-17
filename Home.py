import streamlit as st
import streamlit.components.v1 as components
from streamlit import session_state as ss
from modules.nav import MenuButtons
from pages.account import get_roles
import random
import pickle
import jwt
from jwt.exceptions import DecodeError
import yaml
from jwt import DecodeError, ExpiredSignatureError
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Đọc file cấu hình YAML
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Lấy khóa từ file cấu hình
secret_key = config['cookie']['key']

# Tạo payload
payload = {
    'user_id': 123,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=config['cookie']['expiry_days']) 
}

# Tạo token
token = jwt.encode(payload, secret_key, algorithm='HS256')

print("Generated Token:", token)

# Giải mã token
try:
    decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    print("Payload:", decoded_payload)
except ExpiredSignatureError:
    print("Token has expired.")
except DecodeError:
    print("Token is invalid.")
except Exception as e:
    print(f"An error occurred: {e}")

# If the user reloads or refreshes the page while still logged in,
# go to the account page to restore the login status. Note reloading
# the page changes the session id and previous state values are lost.
# What we are doing is only to relogin the user.
if 'authentication_status' not in ss:
    st.switch_page('./pages/account.py')

MenuButtons(get_roles())

st.markdown(
  """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bungee+Spice&display=swap" rel="stylesheet">
  """, 
  unsafe_allow_html=True)

custom_css = """
    <style>
    .custom-header {
        font-family: "Bungee Spice", sans-serif;
        font-size: 60px;
        color: #FFD700;
        text-align: center;
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<p class='custom-header'>TORO - MUSIC FOR LIFE</p>", unsafe_allow_html=True)


# SLIDESHOWS -------------------------------------------------------------------------------------------------
components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing: border-box;}
body {font-family: Verdana, sans-serif;}
.mySlides {display: none;}
img {vertical-align: middle;}

/* Slideshow container */
.slideshow-container {
  max-width: 1000px;
  position: relative;
  margin: auto;
}

/* Caption text */
.text {
  color: #f2f2f2;
  font-size: 20px;
  padding: 8px 12px;
  position: absolute;
  bottom: 8px;
  width: 100%;
  text-align: center;
}

/* Number text (1/3 etc) */
.numbertext {
  color: #f2f2f2;
  font-size: 12px;
  padding: 8px 12px;
  position: absolute;
  top: 0;
}

/* The dots/bullets/indicators */
.dot {
  height: 15px;
  width: 15px;
  margin: 0 2px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  transition: background-color 0.6s ease;
}

.active {
  background-color: #717171;
}

/* Fading animation */
.fade {
  animation-name: fade;
  animation-duration: 1.5s;
}

@keyframes fade {
  from {opacity: .4} 
  to {opacity: 1}
}

/* On smaller screens, decrease text size */
@media only screen and (max-width: 300px) {
  .text {font-size: 11px}
}
</style>
</head>
<body>

<div class="slideshow-container">

<div class="mySlides fade">
  <img src="https://content.api.news/v3/images/bin/a050d5efbb8316137626df7fc235bae8" style="width:100%">
</div>

<div class="mySlides fade">
  <img src="https://i2.wp.com/hollieblog.com/wp-content/uploads/2020/05/conan-album-image.png?fit=1024%2C512&ssl=1" style="width:100%">
</div>

<div class="mySlides fade">
  <img src="https://assets.rebelmouse.io/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZSI6Imh0dHBzOi8vYXNzZXRzLnJibC5tcy8yNjEyNjkzNC9vcmlnaW4uanBnIiwiZXhwaXJlc19hdCI6MTc1MTgzNjE2MX0.iNUhgOuDNCoAC2h4CcxCUyA8y_m9e8y5ky5MSTYBhDY/img.jpg?width=1200&height=600&coordinates=0%2C0%2C0%2C68" style="width:100%">
</div>

<div class="mySlides fade">
  <img src="https://lhslance.org/wp-content/uploads/2019/05/Untitled-presentation-1-e1557157053760.jpg" style="width:90%">
</div>

<div class="mySlides fade">
  <img src="https://www.usatoday.com/gcdn/presto/2021/10/07/USAT/79244000-18b6-441c-b8e9-0144618e8c81-US_Vogue_NOV21_Cover.jpg?crop=2324,1308,x0,y489&width=2324&height=1308&format=pjpg&auto=webp" style="width:100%">
</div>

<div class="mySlides fade">
  <img src="https://media.pitchfork.com/photos/6058ad261f9ee7d62be45061/16:9/w_1280,c_limit/Justin%20Bieber:%20Justice.jpeg" style="width:100%">
</div>

<div class="mySlides fade">
  <img src="https://static.standard.co.uk/2020/11/13/18/Harryvog2020.jpg?width=1200" style="width:85%">
</div>

<div class="mySlides fade">
  <img src="https://media-s3-us-east-1.ceros.com/uproxx/images/2023/08/30/a528c1ab63c22c73eb575a82a8c5693c/ashnikko-r3-don-9661.jpg?imageOpt=1&fit=bounds&width=1575&crop=3000,1501,x0,y0" style="width:100%">
</div>

</div>
<br>

<div style="text-align:center">
  <span class="dot"></span> 
  <span class="dot"></span> 
  <span class="dot"></span>
  <span class="dot"></span> 
  <span class="dot"></span> 
  <span class="dot"></span> 
  <span class="dot"></span> 
  <span class="dot"></span> 
</div>

<script>
let slideIndex = 0;
showSlides();

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlides, 2000);
}
</script>

</body>
</html> 

    """,
    height=700,
)

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

music = pickle.load(open('df.pkl','rb'))

def get_song_album_cover_url(song_name, artist_name):
  search_query = f"track:{song_name} artist:{artist_name}"
  results = sp.search(q=search_query, type="track")

  if results and results["tracks"]["items"]:
      track = results["tracks"]["items"][0]
      album_cover_url = track["album"]["images"][0]["url"]
      print(album_cover_url)
      return album_cover_url
  else:
      return "https://i.postimg.cc/0QNxYz4V/social.png"
    
def explore():
  random_songs = music.sample(n=20)
  
  music_names = []
  music_posters = []

  for _, row in random_songs.iterrows():
    artist = row.artist
    song_name = row.song
    music_names.append(song_name)
    music_posters.append(get_song_album_cover_url(song_name, artist))

  return music_names, music_posters

# NEW RL PL -------------------------------------------------------------------------------------------------
st.markdown(
    """
    <h1 style='color: #FF5733;'>New Release Playlist</h1>
    """, 
    unsafe_allow_html=True
)

def display_song_row():
    song_names, song_posters = explore()
  
    cols = st.columns(10)
    for i in range(10):
        with cols[i]:
            st.image(song_posters[i], use_column_width=True)
            st.write(song_names[i])

display_song_row()

# FEATURED MUSIC -------------------------------------------------------------------------------------------------
st.markdown(
    """
    <h1 style='color: #FF5733;'>Featured music</h1>
    """, 
    unsafe_allow_html=True
)

def display_music():
    song_names, song_posters = explore()

    for i in range(0, 20, 5):
        cols = st.columns([0.5, 0.5, 0.5, 0.5, 0.5])  
        for j in range(5):
            with cols[j]:
                st.image(song_posters[i + j], width=130) 
                st.write(song_names[i + j])

display_music()

# TOP 10 -------------------------------------------------------------------------------------------------
st.markdown(
    """
    <h1 style='color: #FF5733;'>Top 10 This Week</h1>
    """, 
    unsafe_allow_html=True
)

def fetch_random_songs():
    random_songs = music.sample(n=10)
  
    music_names = []
    music_posters = []

    for _, row in random_songs.iterrows():
        artist = row.artist
        song_name = row.song
        music_names.append(song_name)
        music_posters.append(get_song_album_cover_url(song_name, artist))

    return music_names, music_posters

def display_song_row():
    song_names, song_posters = fetch_random_songs()
  
    cols = st.columns(10)
    for i in range(10):
        with cols[i]:
            st.image(song_posters[i], use_column_width=True)
            st.write(song_names[i])

display_song_row()

# HOT SONGS -------------------------------------------------------------------------------------------------
st.markdown(
    """
    <h1 style='color: #FF5733;'>Hot Songs</h1>
    """, 
    unsafe_allow_html=True
)

def display_song_rows():
    song_names, song_posters = explore()
    cols = st.columns(4)
    
    for i in range(0, 12, 4):
        cols = st.columns([1, 1, 1, 1])  
        for j in range(4):
            with cols[j]:
                st.image(song_posters[i + j], width=200)
                st.write(song_names[i + j])

display_song_rows()

# MORE TO LISTEN -------------------------------------------------------------------------------------------------
st.markdown(
    """
    <h1 style='color: #FF5733;'>More To Listen</h1>
    """, 
    unsafe_allow_html=True
)

if ss.authentication_status:
    st.write('Please click the Recommender on the left navigation bar.')
else:
    st.write('Please login on Account page, then click the Recommender on the left navigation bar.')
