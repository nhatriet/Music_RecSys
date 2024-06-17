import pandas as pd
import streamlit as st
from modules.nav import MenuButtons
from pages.account import get_roles
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yaml
from yaml.loader import SafeLoader
from modules.nav import MenuButtons
import json
import os

if 'authentication_status' not in st.session_state:
    st.switch_page('./pages/search.py')

MenuButtons(get_roles())

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@st.cache_data
def load_music():
    url = "https://raw.githubusercontent.com/nhatriet/Dataset_Spotify/main/spotify_millsongdata.csv"
    return pd.read_csv(url, sep=",", on_bad_lines='skip', engine='python')

music = load_music()

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def load_saved_songs():
    saved_songs_file = 'saved_songs.json'
    if os.path.exists(saved_songs_file):
        with open(saved_songs_file, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_songs_to_file(saved_songs_data):
    saved_songs_file = 'saved_songs.json'
    with open(saved_songs_file, 'w') as file:
        json.dump(saved_songs_data, file)

def search_and_save():
    st.markdown(
        """
        <h1 style='color: #FF5733;'>Search and Save Songs</h1>
        """,
        unsafe_allow_html=True
    )

    if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
        st.error("You need to log in to save songs.")
        return

    user_id = st.session_state['authentication_status']  # Assuming this contains the unique user identifier

    name = st.text_input("Enter song name")
    
    if name:
        filtered = music[music['song'].str.lower().str.contains(name.lower(), na=False)]
    else:
        filtered = music

    st.write(f"{len(filtered)} songs found")
    st.write(filtered)
    selected_songs = st.multiselect("Select songs to save", filtered['song'].tolist())

    saved_songs_file = 'saved_songs.json'

     # Load saved songs from file
    saved_songs_data = load_saved_songs()

    if user_id not in saved_songs_data:
        saved_songs_data[user_id] = []

    if st.button("Save selected songs"):
        saved_songs_data[user_id].extend(selected_songs)
        saved_songs_data[user_id] = list(set(saved_songs_data[user_id]))  # Remove duplicates
        save_songs_to_file(saved_songs_data)
        st.success(f"Saved {len(selected_songs)} songs!")
        st.session_state['saved_songs'] = saved_songs_data  # Update session state

    # Load configuration from config.yaml
    #with open('config.yaml', 'r') as file:
    #    config = yaml.safe_load(file)

    # Lấy khóa từ file cấu hình
    #secret_key = config['cookie']['key']

    # Load saved songs from session state
    #if 'saved_songs' not in st.session_state:
    #    st.session_state.saved_songs = {}

    #if user_id not in st.session_state.saved_songs:
    #    st.session_state.saved_songs[user_id] = []

    #if st.button("Save selected songs"):
    #    st.session_state.saved_songs[user_id].extend(selected_songs)
    #    st.session_state.saved_songs[user_id] = list(set(st.session_state.saved_songs[user_id]))  # Remove duplicates
    #   st.success(f"Saved {len(selected_songs)} songs!")

    saved_songs = st.session_state.saved_songs.get(user_id, [])
    num_columns = 5  

    st.markdown(
        """
        <h1 style='color: #FF5733;'>Saved Songs</h1>
        """,
        unsafe_allow_html=True
    )
    for i in range(0, len(saved_songs), num_columns):
        col_items = saved_songs[i:i+num_columns]
        col = st.columns(num_columns)
        for idx, item in enumerate(col_items):
            with col[idx]:
                song_data = music[music['song'] == item].iloc[0]
                artist_name = song_data['artist']
                album_cover_url = get_song_album_cover_url(item, artist_name)
                st.text(item)
                st.image(album_cover_url, width=100)

if 'saved_songs' not in st.session_state:
    st.session_state['saved_songs'] = load_saved_songs()
    
search_and_save()
