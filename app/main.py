"""Main FastAPI application entry point for ErsteKinderApp."""

from typing import Any
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import APP_TITLE, APP_VERSION, STATIC_DIR, TEMPLATES_DIR
from app.core.registry import get_game_registry
from app.core.settings import settings_router
from app.games.color_sort.router import router as color_sort_router
from app.games.connect_four.router import router as connect_four_router
from app.games.jump_and_run.router import router as jump_and_run_router
from app.games.paint_by_numbers.router import router as paint_by_numbers_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI web application."""
    application = FastAPI(title=APP_TITLE, version=APP_VERSION)
    application.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    application.include_router(settings_router)
    application.include_router(connect_four_router)
    application.include_router(color_sort_router)
    application.include_router(paint_by_numbers_router)
    application.include_router(jump_and_run_router)

    @application.get("/", response_class=HTMLResponse)
    def start_page(request: Request) -> HTMLResponse:
        """Render the start page with all available minigames."""
        registry = get_game_registry()
        games = [g.to_dict() for g in registry.list_all()]
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "page_title": APP_TITLE,
                "games": games,
                "game_id": None,
            },
        )

    @application.get("/api/games")
    def list_games_api() -> dict[str, Any]:
        """Return JSON list of all registered minigames."""
        registry = get_game_registry()
        return {"games": [g.to_dict() for g in registry.list_all()]}

    @application.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok", "version": APP_VERSION}

    return application


app = create_app()
