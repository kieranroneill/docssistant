from fastapi import Request

from .clients import AgentClient


def get_agent(request: Request) -> AgentClient:
    return request.app.state.agent
