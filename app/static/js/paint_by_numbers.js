/**
 * Paint by Numbers (Ausmalspiel) Frontend Controller
 */
(function () {
    let gameState = null;
    let activeColorNumber = 1;

    const svgEl = document.getElementById("pbn-svg");
    const paletteEl = document.getElementById("pbn-palette");
    const statusEl = document.getElementById("pbn-status");
    const templateSelect = document.getElementById("pbn-template-select");
    const loadPresetBtn = document.getElementById("pbn-load-preset-btn");
    const hintBtn = document.getElementById("pbn-hint-btn");
    const uploadForm = document.getElementById("pbn-upload-form");
    const granSlider = document.getElementById("pbn-granularity");
    const granVal = document.getElementById("pbn-granularity-val");
    const detailSelect = document.getElementById("pbn-detail");

    granSlider?.addEventListener("input", () => {
        granVal.textContent = granSlider.value;
    });

    loadPresetBtn?.addEventListener("click", () => loadPreset(templateSelect.value));
    templateSelect?.addEventListener("change", () => loadPreset(templateSelect.value));
    hintBtn?.addEventListener("click", showHint);

    uploadForm?.addEventListener("submit", async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById("pbn-file-input");
        if (!fileInput.files.length) return;

        const [cols, rows] = detailSelect.value.split("x").map(Number);
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);
        formData.append("num_colors", granSlider.value);
        formData.append("grid_cols", cols);
        formData.append("grid_rows", rows);
        formData.append("strict_mode", "true");

        statusEl.textContent = "⏳ Dein Bild wird in ein Ausmalbild mit Zahlen umgewandelt...";
        const res = await fetch("/api/paint-by-numbers/upload", {
            method: "POST",
            body: formData,
        });
        if (res.ok) {
            gameState = await res.json();
            activeColorNumber = gameState.palette[0]?.number || 1;
            renderWorkspace();
        } else {
            statusEl.textContent = "❌ Das Bild konnte leider nicht geladen werden.";
        }
    });

    async function loadPreset(templateId) {
        const res = await fetch("/api/paint-by-numbers/new", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ template_id: templateId, strict_mode: true }),
        });
        if (res.ok) {
            gameState = await res.json();
            activeColorNumber = gameState.palette[0]?.number || 1;
            renderWorkspace();
        }
    }

    async function paintRegion(regionId) {
        if (!gameState) return;
        const res = await fetch("/api/paint-by-numbers/paint", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                game_id: gameState.game_id,
                region_id: regionId,
                color_number: activeColorNumber,
            }),
        });
        if (res.ok) {
            gameState = await res.json();
            renderWorkspace(gameState.paint_result?.message);
        }
    }

    async function showHint() {
        if (!gameState) return;
        const res = await fetch(`/api/paint-by-numbers/hint/${gameState.game_id}?color_number=${activeColorNumber}`);
        if (res.ok) {
            const { hint } = await res.json();
            if (hint) {
                statusEl.innerHTML = `💡 Tipp: Suche nach einem Feld mit der Zahl <strong>${hint.number}</strong>!`;
            }
        }
    }

    function renderWorkspace(customMsg) {
        paletteEl.innerHTML = "";
        gameState.palette.forEach((item) => {
            const btn = document.createElement("button");
            btn.className = "palette-swatch" + (item.number === activeColorNumber ? " active" : "");
            btn.style.backgroundColor = item.hex;
            btn.textContent = `${item.number} – ${item.name}`;
            btn.addEventListener("click", () => {
                activeColorNumber = item.number;
                renderWorkspace();
            });
            paletteEl.appendChild(btn);
        });

        svgEl.setAttribute("viewBox", gameState.view_box || "0 0 600 450");
        svgEl.innerHTML = "";

        gameState.regions.forEach((reg) => {
            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path.setAttribute("d", reg.path_d);
            path.setAttribute("class", "pbn-region");
            path.setAttribute("fill", reg.painted_hex || "#f8fafc");
            path.addEventListener("click", () => paintRegion(reg.id));
            svgEl.appendChild(path);

            if (!reg.is_completed) {
                const txt = document.createElementNS("http://www.w3.org/2000/svg", "text");
                txt.setAttribute("x", reg.label_x);
                txt.setAttribute("y", reg.label_y);
                txt.setAttribute("class", "pbn-label");
                txt.textContent = reg.number;
                svgEl.appendChild(txt);
            }
        });

        if (gameState.is_finished) {
            statusEl.innerHTML = "🎉 <strong>Kunstwerk fertig! (100%)</strong> Dein Bild sieht fantastisch aus!";
        } else {
            const msg = customMsg || `Farbe ${activeColorNumber} ausgewählt – tippe auf ein Feld mit der Zahl ${activeColorNumber}!`;
            statusEl.innerHTML = `Fortschritt: <strong>${gameState.progress_percent}%</strong> (${gameState.completed_count}/${gameState.total_count}) – ${msg}`;
        }
    }

    window.addEventListener("keydown", (e) => {
        if (!gameState) return;
        const num = parseInt(e.key, 10);
        if (num >= 1 && num <= gameState.palette.length) {
            activeColorNumber = num;
            renderWorkspace();
        }
    });

    loadPreset(templateSelect?.value || "sunny_house");
})();
