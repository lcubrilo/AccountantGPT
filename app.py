import streamlit as st
from dotenv import find_dotenv, load_dotenv
from streamlit_theme import st_theme
from llm.prompts import INTRODUCTION_MESSAGE
from utils import (
    AUTHORS,
    LOGO_TEXT_DARK_URL,
    LOGO_TEXT_LIGHT_URL,
    LOGO_URL,
    QUERY_SUGGESTIONS,
    WARNING_MESSAGE,
    generate_response,
    initialize_clients,
    load_config,
)

from login import login_screen
from chat import display_chat_history, handle_user_input
from utils import initialize_clients, load_config
from PIL import Image
import time

# Load environment variables
load_dotenv(find_dotenv())

def show_splash_screen():
    """Display a splash screen with a loading animation."""
    splash_image = Image.open("assets/AccountantGPT-Dark-Horizontal.png")
    st.image(splash_image, use_column_width=True)
    time.sleep(2)  # Simulate loading time

def setup_sidebar():
    """Set up the sidebar with useful information."""
    with st.sidebar:
        st.subheader("⚠️ Warning")
        st.markdown(WARNING_MESSAGE)
        st.subheader("✍️ Authors")
        st.markdown(AUTHORS)

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="AccountantGPT", page_icon=":robot:")
    show_splash_screen()

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": INTRODUCTION_MESSAGE}
        ]
    # Handle login or chat
    if not st.session_state["logged_in"]:
        login_screen()
    else:
        # Set up app content
        st.sidebar.title("AccountantGPT Sidebar")
        qdrant_client, config = initialize_clients(), load_config()

        st.title(f"Welcome, {st.session_state['username']}!")
        setup_sidebar()

        # Chat functionality
        display_chat_history()
        handle_user_input(qdrant_client, config)

        # Log out button
        if st.sidebar.button("Log Out"):
            st.session_state["logged_in"] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
