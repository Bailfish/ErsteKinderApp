"""FastAPI router for Connect Four (4 Gewinnt) view and API endpoints."""

from typing import Any
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.core.config import TEMPLATES_DIR
from app.core.settings import settings_manager
from app.games.connect_four.ai import ConnectFourAI
from app.games.connect_four.engine import ConnectFourEngine, Difficulty, GameMode

router = APIRouter(tags=["connect_four"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

_GAMES: dict[str, ConnectFourEngine] = {}


class NewConnectFourRequest(BaseModel):
    mode: GameMode = Field(default=GameMode.AI)
    difficulty: Difficulty = Field(default=Difficulty.EASY)


class ConnectFourMoveRequest(BaseModel):
    game_id: str
    column: int = Field(..., ge=0, le=6)


@router.get("/games/connect-four", response_class=HTMLResponse)
def connect_four_page(request: Request) -> HTMLResponse:
    """Render the Connect Four minigame HTML page."""
    settings = settings_manager.get_settings("connect_four")
    return templates.TemplateResponse(
        request,
        "games/connect_four.html",
        {
            "game_id": "connect_four",
            "page_title": "4 Gewinnt",
            "settings": settings.model_dump(),
        },
    )


@router.post("/api/connect-four/new")
def create_connect_four_game(payload: NewConnectFourRequest) -> dict[str, Any]:
    """Start a new Connect Four game session."""
    engine = ConnectFourEngine(mode=payload.mode, difficulty=payload.difficulty)
    _GAMES[engine.game_id] = engine
    return engine.get_state()


@router.get("/api/connect-four/state/{game_id}")
def get_connect_four_state(game_id: str) -> dict[str, Any]:
    """Retrieve the state of an existing Connect Four game."""
    engine = _GAMES.get(game_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Connect Four game not found.")
    return engine.get_state()


@router.post("/api/connect-four/move")
def play_connect_four_move(payload: ConnectFourMoveRequest) -> dict[str, Any]:
    """Drop a disc in the chosen column and automatically run AI reply if in AI mode."""
    engine = _GAMES.get(payload.game_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Connect Four game not found.")

    try:
        player_move = engine.drop_disc(payload.column)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    ai_move = None
    if engine.mode == GameMode.AI and not engine.is_game_over:
        ai_col = ConnectFourAI.choose_move(engine, difficulty=engine.difficulty)
        ai_move = engine.drop_disc(ai_col)

    state = engine.get_state()
    state["last_player_move"] = player_move
    state["last_ai_move"] = ai_move
    return state
