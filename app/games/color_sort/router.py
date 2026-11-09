"""FastAPI router for the Color Sort (Farbsortierspiel) minigame."""

from typing import Any
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.core.config import TEMPLATES_DIR
from app.core.settings import settings_manager
from app.games.color_sort.engine import ColorSortEngine

router = APIRouter(tags=["color_sort"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

_GAMES: dict[str, ColorSortEngine] = {}


class NewColorSortRequest(BaseModel):
    difficulty: str = Field(default="easy")
    seed: int | None = None


class PourRequest(BaseModel):
    game_id: str
    from_tube: int = Field(..., ge=0)
    to_tube: int = Field(..., ge=0)


class UndoRequest(BaseModel):
    game_id: str


@router.get("/games/color-sort", response_class=HTMLResponse)
def color_sort_page(request: Request) -> HTMLResponse:
    """Render the Color Sort minigame HTML page."""
    settings = settings_manager.get_settings("color_sort")
    return templates.TemplateResponse(
        request,
        "games/color_sort.html",
        {
            "game_id": "color_sort",
            "page_title": "Farbsortierspiel",
            "settings": settings.model_dump(),
        },
    )


@router.post("/api/color-sort/new")
def create_color_sort_game(payload: NewColorSortRequest) -> dict[str, Any]:
    """Create a new solvable Color Sort puzzle."""
    engine = ColorSortEngine(difficulty=payload.difficulty, seed=payload.seed)
    _GAMES[engine.game_id] = engine
    return engine.get_state()


@router.get("/api/color-sort/state/{game_id}")
def get_color_sort_state(game_id: str) -> dict[str, Any]:
    """Get current state of a Color Sort game."""
    engine = _GAMES.get(game_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Color Sort game not found.")
    return engine.get_state()


@router.post("/api/color-sort/pour")
def pour_color_sort(payload: PourRequest) -> dict[str, Any]:
    """Pour liquid from `from_tube` into `to_tube`."""
    engine = _GAMES.get(payload.game_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Color Sort game not found.")
    try:
        moved = engine.pour(payload.from_tube, payload.to_tube)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    state = engine.get_state()
    state["moved_units"] = moved
    return state


@router.post("/api/color-sort/undo")
def undo_color_sort(payload: UndoRequest) -> dict[str, Any]:
    """Undo the last pour action."""
    engine = _GAMES.get(payload.game_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Color Sort game not found.")
    undone = engine.undo()
    state = engine.get_state()
    state["undone"] = undone
    return state
