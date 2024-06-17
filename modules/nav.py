import streamlit as st
from streamlit import session_state as ss

st.sidebar.image("images/toro_logo.png", use_column_width=True)

def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

def LoginNav():
    st.sidebar.page_link("pages/account.py", label="Account", icon='🔐')

def AdminNav():
    st.sidebar.page_link("pages/admin.py", label="Admin Dashboard", icon='🛠️')

def RecommenderNav():
    st.sidebar.page_link("pages/recommender.py", label="Recommender", icon='🎵')

def SearchNav():
    st.sidebar.page_link("pages/search.py", label="Search", icon='🔍')



def MenuButtons(user_roles=None):
    if user_roles is None:
        user_roles = {}

    if 'authentication_status' not in ss:
        ss.authentication_status = False

    # Always show the home and login navigators.
    HomeNav()
    LoginNav()

    # Show the other page navigators depending on the users's role.
    if ss.authentication_status:
        if 'username' in ss and ss.username in user_roles:
            role = user_roles[ss.username]
            if role == 'admin':
                AdminNav()

        RecommenderNav()
        SearchNav()
