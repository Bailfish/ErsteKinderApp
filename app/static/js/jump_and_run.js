/**
 * Jump and Run (Hüpf & Flitz) Frontend Controller
 */
(function () {
    const canvas = document.getElementById("jr-canvas");
    const ctx = canvas.getContext("2d");
    const scoreEl = document.getElementById("jr-score");
    const dodgedEl = document.getElementById("jr-dodged");
    const highscoreEl = document.getElementById("jr-highscore");
    const diffSelect = document.getElementById("jr-difficulty");
    const startBtn = document.getElementById("jr-start-btn");
    const jumpBtn = document.getElementById("jr-jump-btn");
    const duckBtn = document.getElementById("jr-duck-btn");
    const hintEl = document.getElementById("jr-control-hint");

    let gameState = null;
    let pendingAction = null;
    let loopTimer = null;

    startBtn?.addEventListener("click", startNewRun);
    diffSelect?.addEventListener("change", startNewRun);

    jumpBtn?.addEventListener("click", () => {
        if (window.GameSettings?.control_scheme === "keyboard") return;
        pendingAction = "jump";
    });
    duckBtn?.addEventListener("mousedown", () => {
        if (window.GameSettings?.control_scheme === "keyboard") return;
        pendingAction = "duck";
    });
    duckBtn?.addEventListener("mouseup", () => {
        pendingAction = "stand";
    });
    canvas?.addEventListener("click", () => {
        if (window.GameSettings?.control_scheme === "keyboard") return;
        pendingAction = "jump";
    });

    window.addEventListener("gamesettings:updated", (e) => {
        const s = e.detail;
        hintEl.textContent = `Steuerung: ${s.primary_key} = Springen | ${s.secondary_key} = Ducken (${s.control_scheme})`;
    });

    window.addEventListener("keydown", (e) => {
        if (window.GameSettings?.control_scheme === "mouse_touch") return;
        const jumpKey = window.GameSettings?.primary_key || "Space";
        const duckKey = window.GameSettings?.secondary_key || "ArrowDown";
        if (e.code === jumpKey || e.code === "Space" || e.code === "ArrowUp") {
            e.preventDefault();
            pendingAction = "jump";
        } else if (e.code === duckKey || e.code === "ArrowDown") {
            e.preventDefault();
            pendingAction = "duck";
        }
    });

    window.addEventListener("keyup", (e) => {
        const duckKey = window.GameSettings?.secondary_key || "ArrowDown";
        if (e.code === duckKey || e.code === "ArrowDown") {
            pendingAction = "stand";
        }
    });

    async function startNewRun() {
        if (loopTimer) clearInterval(loopTimer);
        const res = await fetch("/api/jump-and-run/new", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ difficulty: diffSelect.value }),
        });
        gameState = await res.json();
        renderScene();
        loopTimer = setInterval(stepGame, 50);
    }

    async function stepGame() {
        if (!gameState || gameState.game_over) {
            if (loopTimer) clearInterval(loopTimer);
            return;
        }
        const actionToSend = pendingAction;
        pendingAction = null;
        const res = await fetch("/api/jump-and-run/step", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                game_id: gameState.game_id,
                dt: 0.05,
                action: actionToSend,
            }),
        });
        if (res.ok) {
            gameState = await res.json();
            renderScene();
        }
    }

    function renderScene() {
        if (!gameState) return;
        const groundY = 270;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Player
        const p = gameState.player;
        const py = groundY - p.y - p.height;
        ctx.fillStyle = "#ff595e";
        ctx.beginPath();
        ctx.roundRect(p.x, py, p.width, p.height, 10);
        ctx.fill();
        ctx.fillStyle = "#fff";
        ctx.fillRect(p.x + p.width - 14, py + 10, 8, 8);

        // Obstacles
        gameState.obstacles.forEach((obs) => {
            const oy = groundY - obs.y - obs.height;
            ctx.fillStyle = obs.kind === "air" ? "#6a4c93" : "#d97706";
            ctx.beginPath();
            ctx.roundRect(obs.x, oy, obs.width, obs.height, 8);
            ctx.fill();
        });

        scoreEl.textContent = gameState.score;
        dodgedEl.textContent = gameState.obstacles_dodged;
        highscoreEl.textContent = gameState.highscore || 0;

        if (gameState.game_over) {
            ctx.fillStyle = "rgba(15, 23, 42, 0.65)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#fff";
            ctx.font = "bold 28px Nunito, sans-serif";
            ctx.textAlign = "center";
            ctx.fillText(`💥 Autsch! Punkte: ${gameState.score} – Klicke auf 'Lauf starten'!`, canvas.width / 2, 175);
        }
    }

    startNewRun();
})();
