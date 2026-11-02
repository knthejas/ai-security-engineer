from fastapi import FastAPI

from ai_security_engineer.api.router import api_router
from ai_security_engineer.core.config import settings


def create_app() -> FastAPI:
    """Create the HTTP application."""
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(api_router)
    return app


app = create_app()
