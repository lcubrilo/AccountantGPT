import json
import os
from typing import Dict, Generator, List

import streamlit as st
import yaml
from langfuse.decorators import langfuse_context, observe
from langfuse.openai import openai
from loguru import logger
from openai.types.chat import ChatCompletion
from pydantic import BaseModel
from qdrant_client import QdrantClient

from database.utils import embed_text, get_context, search
from llm.prompts import DEFAULT_CONTEXT
from llm.utils import formate_messages_chat
from router.query_router import formate_messages_router
from router.router_prompt import DEFAULT_ROUTER_RESPONSE

LOGO_URL = "assets/AccountantGPT-Logomark.png"
LOGO_TEXT_LIGHT_URL = "assets/AccountantGPT-Light-Horizontal.png"
LOGO_TEXT_DARK_URL = "assets/AccountantGPT-Dark-Horizontal.png"
TEXT_URL = "assets/AccountantGPT-Dark-Typography.png"

WARNING_MESSAGE = """
_Please note that AccountantGPT may make **mistakes**. For critical legal information, always **verify** with a qualified legal professional. AccountantGPT is here to assist, not replace professional legal advice._
"""

QUERY_SUGGESTIONS = """
Na koliko dana godisnjeg imam pravo?\n
Da li smem da koristim porodiljsko bolovanje zene umesto nje?\n
Koji porez placam ako sam preduzetnik?\n
Da li mogu da trazim da se izbrisu moji podaci sa sajta ako ih nisam odobrio?\n
U kom roku mogu da trazim zamenu proizvoda kojim nisam zadovoljan?\n
Kome pripadaju pokloni koje smo muz i ja dobili na vencanju?
"""

AUTHORS = """
[Luka Čubrilo](https://www.linkedin.com/in/luka-cubrilo/)
"""


class RouterConfig(BaseModel):
    model: str
    temperature: float


class ChatConfig(BaseModel):
    model: str
    temperature: float
    max_conversation: int


class EmbeddingsConfig(BaseModel):
    model: str
    dimensions: int


class OpenAIConfig(BaseModel):
    embeddings: EmbeddingsConfig
    chat: ChatConfig
    router: RouterConfig


class Config(BaseModel):
    openai: OpenAIConfig


def load_config(yaml_file_path: str = "./config.yaml") -> Config:
    with open(yaml_file_path, "r") as file:
        yaml_content = yaml.safe_load(file)
    return Config(**yaml_content)


@st.cache_resource
def initialize_clients() -> QdrantClient:
    """
    Initializes and returns the clients for OpenAI and Qdrant services.

    Returns:
    - Tuple[OpenAI, QdrantClient]: A tuple containing the initialized OpenAI and Qdrant clients.

    Raises:
    - EnvironmentError: If required environment variables are missing.
    """
    try:
        # Retrieve Qdrant client configuration from environment variables
        qdrant_url = os.environ["QDRANT_CLUSTER_URL"]
        qdrant_api_key = os.environ["QDRANT_API_KEY"]
        qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

        return qdrant_client
    except KeyError as e:
        error_msg = f"Missing environment variable: {str(e)}"
        logger.error(error_msg)
        raise EnvironmentError(error_msg)


@observe(as_type="generation")
def call_llm(
    model: str,
    temperature: float,
    messages: List[Dict],
    json_response: bool = False,
    stream: bool = False,
) -> ChatCompletion:
    """
    Get an answer from the OpenAI chat model.
    """
    logger.info("Sending to Langfuse/OpenAI:")
    logger.info(f"Model: {model}")
    logger.info(f"Temperature: {temperature}")
    logger.info(f"Messages: {json.dumps(messages, indent=2)}")
    logger.info(f"JSON Response: {json_response}")
    try:
        response = openai.chat.completions.create(
            model=model,
            response_format={"type": "json_object"} if json_response else None,
            temperature=temperature,
            messages=messages,
            stream=stream,
        )
        logger.info("Langfuse/OpenAI response received.")
        return response
    except Exception as e:
        logger.error(f"Langfuse/OpenAI error: {e}")
        raise



@observe()
def generate_response(
    query: str, qdrant_client: QdrantClient, config: Config
) -> Generator[str, None, None]:
    """
    Generates a response for a given user query using a combination of semantic search and a chat model.

    Args:
    - query (str): The user's query string.
    - qdrant_client (QdrantClient): Client to interact with Qdrant's API.
    - config (Config): Configuration settings for API interaction and response handling.

    Yields:
    - str: Parts of the generated response from the chat model.
    """
    try:
        # Limit the stored messages to the maximum conversation length defined in the configuration
        st.session_state.messages = st.session_state.messages[
            -config.openai.chat.max_conversation :
        ]

        # Determine the relevant collections to route the query to
        messages = formate_messages_router(query)
        response = call_llm(
            model=config.openai.router.model,
            temperature=config.openai.router.temperature,
            messages=messages,
            json_response=True,
        )
        try:
            collections = json.loads(response.choices[0].message.content)["response"]
            logger.info(f"Query routed to collections: {collections}")
            langfuse_context.update_current_trace(tags=collections)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Error parsing Langfuse response: {str(e)}")
            logger.error(f"Raw response: {response}")
            yield "Sorry, there was an issue processing your query."
            return

        # Embed the user query using the specified model in the configuration
        embedding_response = embed_text(
            text=query,
            model=config.openai.embeddings.model,
        )
        embedding = embedding_response.data[0].embedding

        # Determine the context for the chat model based on the routed collections
        context = determine_context(collections, embedding, qdrant_client)

        # Generate the response stream from the chat model
        messages = formate_messages_chat(
            context=context, query=query, conversation=st.session_state.messages
        )
        stream = call_llm(
            model=config.openai.chat.model,
            temperature=config.openai.chat.temperature,
            messages=messages,
            stream=True,
        )

        # Yield each part of the response as it becomes available
        for chunk in stream:
            part = chunk.choices[0].delta.content
            if part is not None:
                yield part

        langfuse_context.flush()

    except Exception as e:
        logger.error(f"An error occurred while generating the response: {str(e)}")
        yield "Sorry, an error occurred while processing your request."


def determine_context(
    collections: List[str], embedding: List[float], qdrant_client: QdrantClient
) -> str:
    """Determines the context for generating responses based on search results from collections."""
    try:
        if collections[0] == DEFAULT_ROUTER_RESPONSE:
            return DEFAULT_CONTEXT
        else:
            search_results = []
            for collection_name in collections:
                search_results.extend(
                    search(
                        client=qdrant_client,
                        collection=collection_name,
                        query_vector=embedding,
                        limit=10,
                        with_vectors=True,
                    )
                )
            # Upgrade this with tokes length checking
            top_k = 15 if len(collections) > 1 else 10
            return get_context(search_results=search_results, top_k=top_k)
    except Exception as e:
        logger.error(f"Error determining context: {str(e)}")
        return DEFAULT_CONTEXT  # Fallback to default context
