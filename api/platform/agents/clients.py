import os
from abc import ABC, abstractmethod

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.graph.state import CompiledStateGraph

from api.platform.datetime.utilities import now, to_iso_string

from .dtos import ChatResult, Message, Usage


class AbstractAgentClient(ABC):
    ##
    # public methods
    ##
    @abstractmethod
    async def chat(self, query: str, messages: list[Message]) -> ChatResult:
        pass


class AgentClient(AbstractAgentClient):
    _agent: CompiledStateGraph
    _model: ChatOllama

    def __init__(self):
        base_url = os.environ["OLLAMA_BASE_URL"]

        if base_url is None:
            raise ValueError("OLLAMA_BASE_URL environment variable is not set")

        model_name = os.environ["OLLAMA_MODEL"]

        if model_name is None:
            raise ValueError("OLLAMA_MODEL environment variable is not set")

        model = ChatOllama(
            base_url=base_url,
            model=model_name,
            temperature=0,
        )

        self._model = model
        self._agent = create_agent(
            model=model,
            system_prompt="""
            You are a helpful assistant.
            """,
        )

    async def chat(self, query: str, messages: list[Message]) -> ChatResult:
        result = await self._agent.ainvoke(
            {
                "messages": messages.copy().append(Message(content=query, role="user")),
            }
        )
        last = result["messages"][-1]
        content = last.content or ""
        metadata = last.metadata or {}
        model = metadata.get("model") or metadata.get("model_name") or self._model.model
        usage = last.usage_metadata or {}

        return ChatResult(
            content=content,
            created_at=metadata.get("created_at", to_iso_string(now())),
            model=model,
            role="assistant",
            usage=Usage(
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
            ),
        )
