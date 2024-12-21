import streamlit as st
from llm.prompts import INTRODUCTION_MESSAGE
from utils import (
    QUERY_SUGGESTIONS,
    generate_response,
)

ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
CHAT_INPUT_PROMPT = "Postavite pitanje vezano za ..."

def display_chat_history():
    """Display all chat messages stored in the session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input(qdrant_client, config):
    """Handle user input and generate responses."""
    # Provide suggestions if it's the first time interacting
    if not st.session_state.get("suggestions_used", False):
        st.write("### 💡 Suggested Queries")
        for suggestion in QUERY_SUGGESTIONS.split("\n"):
            if suggestion.strip():
                if st.button(suggestion.strip(), key=suggestion.strip()):
                    st.session_state.messages.append({"role": ROLE_USER, "content": suggestion.strip()})
                    generate_and_display_response(suggestion.strip(), qdrant_client, config)
                    st.session_state.suggestions_used = True
                    st.experimental_rerun()

    # Handle manual user input
    if prompt := st.chat_input(CHAT_INPUT_PROMPT):
        generate_and_display_response(prompt, qdrant_client, config)
        st.session_state.suggestions_used = True

def generate_and_display_response(prompt, qdrant_client, config):
    """Generate a response using the LLM and display it."""
    # Append user message to session state.
    st.session_state.messages.append({"role": ROLE_USER, "content": prompt})

    # Display user message in chat container.
    with st.chat_message(ROLE_USER):
        st.markdown(prompt)

    # Generate and display assistant's response.
    with st.chat_message(ROLE_ASSISTANT):
        try:
            stream = generate_response(query=prompt, qdrant_client=qdrant_client, config=config)
            response = st.write_stream(stream)
        except Exception as e:
            response = f"An error occurred: {str(e)}"

    # Append assistant's response to session state.
    st.session_state.messages.append({"role": ROLE_ASSISTANT, "content": response})
