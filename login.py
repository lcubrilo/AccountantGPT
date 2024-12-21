import streamlit as st

# Dummy user database for now
USER_DATABASE = {
    "testuser": "password123",
    "admin": "adminpass",
}

def login_screen():
    """Display the login screen."""
    st.title("Login to AccountantGPT")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Log In")

    if login_button:
        if username in USER_DATABASE and USER_DATABASE[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")
