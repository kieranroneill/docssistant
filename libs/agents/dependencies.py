from fastapi import Request

from .clients import ChatAgent, EmbeddingsAgent


def get_chat_agent(request: Request) -> ChatAgent:
    return request.app.state.chat_agent


def get_embeddings_agent(request: Request) -> EmbeddingsAgent:
    return request.app.state.embeddings_agent
