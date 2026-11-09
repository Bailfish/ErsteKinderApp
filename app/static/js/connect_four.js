/**
 * Connect Four (4 Gewinnt) Frontend Controller
 */
(function () {
    let gameState = null;
    let selectedCol = 3;

    const boardEl = document.getElementById("c4-board");
    const colBtnsEl = document.getElementById("c4-column-buttons");
    const statusEl = document.getElementById("c4-status");
    const modeSelect = document.getElementById("c4-mode");
    const diffSelect = document.getElementById("c4-difficulty");
    const diffLabel = document.getElementById("c4-diff-label");
    const newBtn = document.getElementById("c4-new-btn");

    modeSelect?.addEventListener("change", () => {
        diffLabel.style.display = modeSelect.value === "ai" ? "inline-block" : "none";
        startNewGame();
    });
    diffSelect?.addEventListener("change", startNewGame);
    newBtn?.addEventListener("click", startNewGame);

    window.addEventListener("gamesettings:updated", (e) => {
        if (e.detail?.difficulty) {
            diffSelect.value = e.detail.difficulty;
        }
    });

    async function startNewGame() {
        const res = await fetch("/api/connect-four/new", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                mode: modeSelect.value,
                difficulty: diffSelect.value,
            }),
        });
        gameState = await res.json();
        renderBoard();
    }

    async function makeMove(col) {
        if (!gameState || gameState.is_game_over) return;
        const res = await fetch("/api/connect-four/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ game_id: gameState.game_id, column: col }),
        });
        if (res.ok) {
            gameState = await res.json();
            renderBoard();
        }
    }

    function renderBoard() {
        colBtnsEl.innerHTML = "";
        for (let c = 0; c < 7; c++) {
            const btn = document.createElement("button");
            btn.className = "c4-col-btn";
            btn.textContent = c === selectedCol ? "⬇️" : `${c + 1}`;
            btn.disabled = gameState.is_game_over || !gameState.valid_columns.includes(c);
            btn.addEventListener("click", () => {
                if (window.GameSettings?.control_scheme === "keyboard") return;
                makeMove(c);
            });
            colBtnsEl.appendChild(btn);
        }

        boardEl.innerHTML = "";
        const winSet = new Set((gameState.winning_cells || []).map(([r, c]) => `${r},${c}`));
        for (let r = 0; r < gameState.rows; r++) {
            for (let c = 0; c < gameState.cols; c++) {
                const cell = document.createElement("div");
                const val = gameState.board[r][c];
                cell.className = `c4-cell disc-${val}` + (winSet.has(`${r},${c}`) ? " win-cell" : "");
                cell.addEventListener("click", () => {
                    if (window.GameSettings?.control_scheme === "keyboard") return;
                    makeMove(c);
                });
                boardEl.appendChild(cell);
            }
        }

        if (gameState.winner === 1) {
            statusEl.textContent = "🎉 Hurra! Spieler 1 (Rot 🔴) hat gewonnen!";
        } else if (gameState.winner === 2) {
            statusEl.textContent = gameState.mode === "ai"
                ? "🤖 Der Computer (Gelb 🟡) hat gewonnen! Versuch es gleich nochmal!"
                : "🎉 Hurra! Spieler 2 (Gelb 🟡) hat gewonnen!";
        } else if (gameState.is_draw) {
            statusEl.textContent = "🤝 Unentschieden! Alle Felder sind voll.";
        } else {
            statusEl.textContent = gameState.current_player === 1
                ? "Spieler 1 (Rot 🔴) ist am Zug!"
                : "Spieler 2 (Gelb 🟡) ist am Zug!";
        }
    }

    window.addEventListener("keydown", (e) => {
        if (window.GameSettings?.control_scheme === "mouse_touch") return;
        if (!gameState || gameState.is_game_over) return;
        if (e.code === "ArrowLeft") {
            selectedCol = (selectedCol + 6) % 7;
            renderBoard();
        } else if (e.code === "ArrowRight") {
            selectedCol = (selectedCol + 1) % 7;
            renderBoard();
        } else if (e.code === (window.GameSettings?.primary_key || "Space") || e.code === "Enter") {
            e.preventDefault();
            makeMove(selectedCol);
        } else if (e.key >= "1" && e.key <= "7") {
            makeMove(parseInt(e.key, 10) - 1);
        }
    });

    startNewGame();
})();
