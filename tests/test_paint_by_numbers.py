"""Unit tests for Paint by Numbers engine, preset templates, and custom image processor."""

import io
import pytest
from PIL import Image, ImageDraw
from app.games.paint_by_numbers.engine import PaintByNumbersEngine
from app.games.paint_by_numbers.image_processor import ImageProcessor
from app.games.paint_by_numbers.templates_data import (
    get_preset_template,
    list_preset_templates,
)


def test_preset_templates_and_strict_painting() -> None:
    presets = list_preset_templates()
    assert len(presets) >= 3
    with pytest.raises(KeyError):
        get_preset_template("non_existent")

    engine = PaintByNumbersEngine(template_id="sunny_house", strict_mode=True)
    state = engine.get_state()
    assert state["progress_percent"] == 0
    assert state["is_finished"] is False

    first_reg = state["regions"][0]
    wrong_color = 2 if first_reg["number"] == 1 else 1

    # Strict mode rejects wrong number
    res_wrong = engine.paint_region(first_reg["id"], wrong_color)
    assert res_wrong["accepted"] is False
    assert engine.completed_count == 0

    # Paint all regions with their matching target color number
    for reg in state["regions"]:
        res_ok = engine.paint_region(reg["id"], reg["number"])
        assert res_ok["accepted"] is True
        assert res_ok["matches_target"] is True

    assert engine.is_finished is True
    assert engine.progress_percent == 100
    assert engine.get_hint() is None


def test_paint_invalid_region_and_color_errors() -> None:
    engine = PaintByNumbersEngine(template_id="space_rocket", strict_mode=False)
    with pytest.raises(ValueError):
        engine.paint_region("unknown_reg", 1)
    with pytest.raises(ValueError):
        engine.paint_region("space_bg", 99)

    hint = engine.get_hint(color_number=1)
    assert hint is not None and hint["number"] == 1


def test_image_processor_custom_upload_and_granularity() -> None:
    # Create synthetic colorful test image in memory
    img = Image.new("RGB", (120, 90), color=(255, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 60, 45], fill=(0, 255, 0))
    draw.rectangle([60, 0, 120, 45], fill=(0, 0, 255))
    draw.rectangle([0, 45, 60, 90], fill=(255, 255, 0))
    draw.rectangle([60, 45, 120, 90], fill=(255, 0, 255))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    raw_bytes = buf.getvalue()

    processed = ImageProcessor.process_uploaded_image(
        image_bytes=raw_bytes,
        num_colors=4,
        grid_cols=12,
        grid_rows=8,
        title="TestFoto.png",
    )
    assert 2 <= len(processed["palette"]) <= 4
    assert len(processed["regions"]) >= 2

    # Ensure engine can load and complete the custom uploaded template
    engine = PaintByNumbersEngine(template_data=processed)
    for reg in engine.regions:
        engine.paint_region(reg["id"], reg["number"])
    assert engine.is_finished is True

    with pytest.raises(ValueError):
        ImageProcessor.process_uploaded_image(b"")
    with pytest.raises(ValueError):
        ImageProcessor.process_uploaded_image(b"not-an-image")
