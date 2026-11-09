/**
 * Color Sort (Farbsortierspiel) Frontend Controller
 */
(function () {
    let gameState = null;
    let selectedTube = null;

    const stageEl = document.getElementById("cs-tubes-container");
    const statusEl = document.getElementById("cs-status");
    const diffSelect = document.getElementById("cs-difficulty");
    const undoBtn = document.getElementById("cs-undo-btn");
    const newBtn = document.getElementById("cs-new-btn");

    diffSelect?.addEventListener("change", startNewGame);
    newBtn?.addEventListener("click", startNewGame);
    undoBtn?.addEventListener("click", undoMove);

    window.addEventListener("gamesettings:updated", (e) => {
        if (e.detail?.difficulty && e.detail.difficulty !== diffSelect.value) {
            diffSelect.value = e.detail.difficulty;
            startNewGame();
        }
    });

    async function startNewGame() {
        selectedTube = null;
        const res = await fetch("/api/color-sort/new", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ difficulty: diffSelect.value }),
        });
        gameState = await res.json();
        renderTubes();
    }

    async function handleTubeSelect(index) {
        if (!gameState || gameState.is_solved) return;
        if (selectedTube === null) {
            if (gameState.tubes[index].length > 0) {
                selectedTube = index;
                renderTubes();
            }
            return;
        }
        if (selectedTube === index) {
            selectedTube = null;
            renderTubes();
            return;
        }

        const res = await fetch("/api/color-sort/pour", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                game_id: gameState.game_id,
                from_tube: selectedTube,
                to_tube: index,
            }),
        });
        selectedTube = null;
        if (res.ok) {
            gameState = await res.json();
        } else {
            statusEl.textContent = "⚠️ Da passt die Farbe leider nicht drauf! Gleiche Farbe oder leeres Glas wählen.";
            setTimeout(() => renderTubes(), 1200);
            return;
        }
        renderTubes();
    }

    async function undoMove() {
        if (!gameState) return;
        const res = await fetch("/api/color-sort/undo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ game_id: gameState.game_id }),
        });
        if (res.ok) {
            gameState = await res.json();
            selectedTube = null;
            renderTubes();
        }
    }

    function renderTubes() {
        stageEl.innerHTML = "";
        undoBtn.disabled = !gameState.can_undo;

        gameState.tubes.forEach((layers, idx) => {
            const wrap = document.createElement("div");
            wrap.className = "tube-wrapper" + (selectedTube === idx ? " selected" : "");
            wrap.addEventListener("click", () => {
                if (window.GameSettings?.control_scheme === "keyboard") return;
                handleTubeSelect(idx);
            });

            const glass = document.createElement("div");
            glass.className = "tube-glass";
            layers.forEach((colorId) => {
                const layer = document.createElement("div");
                layer.className = "tube-layer";
                layer.style.background = gameState.palette[colorId]?.hex || "#ccc";
                glass.appendChild(layer);
            });

            const label = document.createElement("span");
            label.style.marginTop = "8px";
            label.style.fontWeight = "800";
            label.textContent = gameState.completed_tubes[idx] ? `✅ Glas ${idx + 1}` : `Glas ${idx + 1}`;

            wrap.appendChild(glass);
            wrap.appendChild(label);
            stageEl.appendChild(wrap);
        });

        if (gameState.is_solved) {
            statusEl.innerHTML = `🎉 <strong>Super gemacht!</strong> Alle Farben sind in ${gameState.move_count} Zügen perfekt sortiert!`;
        } else {
            statusEl.innerHTML = `Wähle ein Reagenzglas zum Ausgießen! (Züge: <strong>${gameState.move_count}</strong>)`;
        }
    }

    window.addEventListener("keydown", (e) => {
        if (window.GameSettings?.control_scheme === "mouse_touch") return;
        if (e.key >= "1" && e.key <= "9") {
            const idx = parseInt(e.key, 10) - 1;
            if (gameState && idx < gameState.tubes.length) handleTubeSelect(idx);
        } else if (e.code === "KeyZ" || e.code === "Backspace") {
            undoMove();
        }
    });

    startNewGame();
})();
