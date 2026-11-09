"""FastAPI router for the Jump and Run (Hüpf & Flitz) minigame."""

from typing import Any
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.core.config import TEMPLATES_DIR
from app.core.settings import settings_manager
from app.games.jump_and_run.engine import JumpAndRunEngine

router = APIRouter(tags=["jump_and_run"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

_GAMES: dict[str, JumpAndRunEngine] = {}
_HIGHSCORES: dict[str, int] = {"easy": 0, "medium": 0, "hard": 0}


class NewJumpRunRequest(BaseModel):
    difficulty: str = Field(default="easy")
    seed: int | None = None


class StepJumpRunRequest(BaseModel):
    game_id: str
    dt: float = Field(default=0.05, ge=0.0, le=0.5)
    action: str | None = Field(default=None)


class ScoreSubmitRequest(BaseModel):
    difficulty: str = Field(default="easy")
    score: int = Field(..., ge=0)


@router.get("/games/jump-and-run", response_class=HTMLResponse)
def jump_and_run_page(request: Request) -> HTMLResponse:
    """Render the Jump and Run minigame HTML page."""
    settings = settings_manager.get_settings("jump_and_run")
    return templates.TemplateResponse(
        request,
        "games/jump_and_run.html",
        {
            "game_id": "jump_and_run",
            "page_title": "Hüpf & Flitz – Jump & Run",
            "settings": settings.model_dump(),
            "highscores": _HIGHSCORES,
        },
    )


@router.post("/api/jump-and-run/new")
def create_jump_and_run_game(payload: NewJumpRunRequest) -> dict[str, Any]:
    """Create a new Jump and Run session."""
    engine = JumpAndRunEngine(difficulty=payload.difficulty, seed=payload.seed)
    _GAMES[engine.game_id] = engine
    state = engine.get_state()
    state["highscore"] = _HIGHSCORES.get(engine.difficulty, 0)
    return state


@router.post("/api/jump-and-run/step")
def step_jump_and_run_game(payload: StepJumpRunRequest) -> dict[str, Any]:
    """Advance the server-side Jump and Run simulation by `dt` seconds."""
    engine = _GAMES.get(payload.game_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Jump and Run game not found.")
    state = engine.step(dt=payload.dt, action=payload.action)
    if state["score"] > _HIGHSCORES.get(engine.difficulty, 0):
        _HIGHSCORES[engine.difficulty] = state["score"]
    state["highscore"] = _HIGHSCORES.get(engine.difficulty, 0)
    return state


@router.post("/api/jump-and-run/score")
def submit_jump_and_run_score(payload: ScoreSubmitRequest) -> dict[str, Any]:
    """Record a highscore achieved in the Jump and Run game."""
    diff = payload.difficulty if payload.difficulty in _HIGHSCORES else "easy"
    if payload.score > _HIGHSCORES[diff]:
        _HIGHSCORES[diff] = payload.score
    return {"difficulty": diff, "highscore": _HIGHSCORES[diff], "highscores": _HIGHSCORES}
