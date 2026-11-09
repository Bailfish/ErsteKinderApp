"""Integration tests for all FastAPI HTML views and JSON API routes."""

import io
from fastapi.testclient import TestClient
from PIL import Image


def test_start_page_and_game_html_pages(client: TestClient) -> None:
    for path in (
        "/",
        "/games/connect-four",
        "/games/color-sort",
        "/games/paint-by-numbers",
        "/games/jump-and-run",
    ):
        res = client.get(path)
        assert res.status_code == 200
        assert "KinderSpielWelt" in res.text

    assert client.get("/health").json()["status"] == "ok"
    assert len(client.get("/api/games").json()["games"]) == 4


def test_settings_gear_api_routes(client: TestClient) -> None:
    res = client.get("/api/settings/connect_four")
    assert res.status_code == 200
    assert res.json()["game_id"] == "connect_four"

    upd = client.put(
        "/api/settings/connect_four",
        json={"control_scheme": "keyboard", "primary_key": "Enter"},
    )
    assert upd.status_code == 200
    assert upd.json()["control_scheme"] == "keyboard"

    rst = client.post("/api/settings/connect_four/reset")
    assert rst.status_code == 200
    assert rst.json()["control_scheme"] == "hybrid"

    assert client.get("/api/settings/invalid").status_code == 404
    assert client.put("/api/settings/invalid", json={}).status_code == 404
    assert client.post("/api/settings/invalid/reset").status_code == 404


def test_connect_four_api_flow(client: TestClient) -> None:
    created = client.post(
        "/api/connect-four/new", json={"mode": "ai", "difficulty": "easy"}
    ).json()
    gid = created["game_id"]

    state = client.get(f"/api/connect-four/state/{gid}")
    assert state.status_code == 200

    move = client.post("/api/connect-four/move", json={"game_id": gid, "column": 3})
    assert move.status_code == 200
    assert move.json()["move_count"] == 2  # Player + AI reply

    assert client.get("/api/connect-four/state/missing").status_code == 404
    assert (
        client.post(
            "/api/connect-four/move", json={"game_id": "missing", "column": 0}
        ).status_code
        == 404
    )


def test_color_sort_api_flow(client: TestClient) -> None:
    created = client.post(
        "/api/color-sort/new", json={"difficulty": "easy", "seed": 7}
    ).json()
    gid = created["game_id"]

    assert client.get(f"/api/color-sort/state/{gid}").status_code == 200

    pour = client.post(
        "/api/color-sort/pour",
        json={"game_id": gid, "from_tube": 0, "to_tube": 3},
    )
    assert pour.status_code == 200

    # Invalid pour onto same tube
    bad_pour = client.post(
        "/api/color-sort/pour",
        json={"game_id": gid, "from_tube": 0, "to_tube": 0},
    )
    assert bad_pour.status_code == 400

    undo = client.post("/api/color-sort/undo", json={"game_id": gid})
    assert undo.status_code == 200
    assert undo.json()["undone"] is True


def test_paint_by_numbers_api_and_upload(client: TestClient) -> None:
    tpls = client.get("/api/paint-by-numbers/templates")
    assert tpls.status_code == 200

    created = client.post(
        "/api/paint-by-numbers/new",
        json={"template_id": "sunny_house", "strict_mode": True},
    ).json()
    gid = created["game_id"]

    hint = client.get(f"/api/paint-by-numbers/hint/{gid}?color_number=1")
    assert hint.status_code == 200

    paint = client.post(
        "/api/paint-by-numbers/paint",
        json={"game_id": gid, "region_id": "sky", "color_number": 1},
    )
    assert paint.status_code == 200
    assert paint.json()["paint_result"]["accepted"] is True

    # Test custom image upload endpoint with granularity
    img = Image.new("RGB", (60, 45), color=(120, 200, 80))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    upload = client.post(
        "/api/paint-by-numbers/upload",
        data={"num_colors": "5", "grid_cols": "10", "grid_rows": "8", "strict_mode": "true"},
        files={"file": ("kid_drawing.png", buf.getvalue(), "image/png")},
    )
    assert upload.status_code == 200
    assert len(upload.json()["regions"]) >= 1


def test_jump_and_run_api_flow(client: TestClient) -> None:
    created = client.post(
        "/api/jump-and-run/new", json={"difficulty": "easy", "seed": 42}
    ).json()
    gid = created["game_id"]

    step = client.post(
        "/api/jump-and-run/step",
        json={"game_id": gid, "dt": 0.05, "action": "jump"},
    )
    assert step.status_code == 200
    assert step.json()["player"]["y"] > 0

    score = client.post(
        "/api/jump-and-run/score", json={"difficulty": "easy", "score": 150}
    )
    assert score.status_code == 200
    assert score.json()["highscore"] >= 150
