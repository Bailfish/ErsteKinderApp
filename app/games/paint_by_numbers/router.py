"""FastAPI router for Paint by Numbers (Ausmalspiel) including custom image upload."""

from typing import Any
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.core.config import TEMPLATES_DIR
from app.core.settings import settings_manager
from app.games.paint_by_numbers.engine import PaintByNumbersEngine
from app.games.paint_by_numbers.image_processor import ImageProcessor
from app.games.paint_by_numbers.templates_data import (
    get_preset_template,
    list_preset_templates,
)

router = APIRouter(tags=["paint_by_numbers"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

_GAMES: dict[str, PaintByNumbersEngine] = {}


class NewPaintGameRequest(BaseModel):
    template_id: str = Field(default="sunny_house")
    strict_mode: bool = Field(default=True)


class PaintRegionRequest(BaseModel):
    game_id: str
    region_id: str
    color_number: int = Field(..., ge=1)


@router.get("/games/paint-by-numbers", response_class=HTMLResponse)
def paint_by_numbers_page(request: Request) -> HTMLResponse:
    """Render the Paint by Numbers minigame HTML page."""
    settings = settings_manager.get_settings("paint_by_numbers")
    return templates.TemplateResponse(
        request,
        "games/paint_by_numbers.html",
        {
            "game_id": "paint_by_numbers",
            "page_title": "Malen nach Zahlen",
            "settings": settings.model_dump(),
            "presets": list_preset_templates(),
        },
    )


@router.get("/api/paint-by-numbers/templates")
def get_available_templates() -> dict[str, Any]:
    """List all built-in example pictures."""
    return {"templates": list_preset_templates()}


@router.post("/api/paint-by-numbers/new")
def create_preset_paint_game(payload: NewPaintGameRequest) -> dict[str, Any]:
    """Start a new Paint by Numbers session from a preset example image."""
    try:
        tpl = get_preset_template(payload.template_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    engine = PaintByNumbersEngine(
        template_data=tpl,
        template_id=payload.template_id,
        strict_mode=payload.strict_mode,
    )
    _GAMES[engine.game_id] = engine
    return engine.get_state()


@router.post("/api/paint-by-numbers/upload")
async def upload_custom_paint_image(
    file: UploadFile = File(...),
    num_colors: int = Form(default=6),
    grid_cols: int = Form(default=18),
    grid_rows: int = Form(default=14),
    strict_mode: bool = Form(default=True),
) -> dict[str, Any]:
    """Upload a custom image and convert it into a Paint-by-Numbers game with adjustable granularity."""
    raw_bytes = await file.read()
    try:
        custom_template = ImageProcessor.process_uploaded_image(
            image_bytes=raw_bytes,
            num_colors=num_colors,
            grid_cols=grid_cols,
            grid_rows=grid_rows,
            title=file.filename or "Mein Bild",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    engine = PaintByNumbersEngine(
        template_data=custom_template,
        template_id="custom_upload",
        strict_mode=strict_mode,
    )
    _GAMES[engine.game_id] = engine
    return engine.get_state()


@router.post("/api/paint-by-numbers/paint")
def paint_region_endpoint(payload: PaintRegionRequest) -> dict[str, Any]:
    """Paint a numbered region with the selected color number."""
    engine = _GAMES.get(payload.game_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Paint game not found.")
    try:
        result = engine.paint_region(payload.region_id, payload.color_number)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    state = engine.get_state()
    state["paint_result"] = result
    return state


@router.get("/api/paint-by-numbers/hint/{game_id}")
def get_paint_hint(game_id: str, color_number: int | None = None) -> dict[str, Any]:
    """Return a hint for an unpainted region."""
    engine = _GAMES.get(game_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Paint game not found.")
    return {"hint": engine.get_hint(color_number=color_number)}
