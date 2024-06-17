import streamlit as st
from streamlit import session_state as ss
from modules.nav import MenuButtons
from pages.account import get_roles
import yaml
import bcrypt

if 'authentication_status' not in ss:
    st.experimental_rerun()

MenuButtons(get_roles())

# Read the config.yaml file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def update_user(username, name, email):
    if username in config['credentials']['usernames']:
        config['credentials']['usernames'][username]['name'] = name
        config['credentials']['usernames'][username]['email'] = email
        
        # Save changes to config.yaml
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)
        
        st.success(f"User {username} updated successfully")
    else:
        st.error("User not found")

def delete_user(username):
    if username in config['credentials']['usernames']:
        del config['credentials']['usernames'][username]
        
        # Save changes to config.yaml
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)
        
        st.success(f"User {username} deleted successfully")
    else:
        st.error("User not found")

def main():
    st.markdown(
        """
        <h1 style='color: #FF5733;'>User Management</h1>
        """,
        unsafe_allow_html=True
    )

    # Display user list in a table
    users_data = [{"Username": username, "Name": user['name'], "Email": user['email']} for username, user in config['credentials']['usernames'].items()]
    st.table(users_data)

    # Display edit/delete options for each user
    for username, user in list(config['credentials']['usernames'].items()):  # Iterate over a copy of the dictionary items
        with st.expander(f"Edit/Delete {username}"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name:", user['name'], key=f"name_{username}")
            with col2:
                email = st.text_input("Email:", user['email'], key=f"email_{username}")
            col3, col4 = st.columns([1, 1])
            with col3:
                if st.button("Update ✏️", key=f"update_{username}"):
                    update_user(username, name, email)
            with col4:
                if st.button("Delete 🗑️", key=f"delete_{username}"):
                    delete_user(username)

if __name__ == "__main__":
    main()
