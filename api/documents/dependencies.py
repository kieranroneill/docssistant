from pathlib import Path

from fastapi import Request


def get_documents_path(request: Request) -> Path:
    return request.app.state.documents_path
