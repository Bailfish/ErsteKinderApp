/**
 * Global Gear Settings Modal Controller (⚙️)
 * Manages control scheme, key bindings, difficulty, and sound across all minigames.
 */
(function () {
    const gameId = document.body.dataset.gameId;
    if (!gameId) return;

    const gearBtn = document.getElementById("settings-gear-btn");
    const modal = document.getElementById("settings-modal");
    const closeBtn = document.getElementById("settings-close-btn");
    const form = document.getElementById("settings-form");
    const resetBtn = document.getElementById("settings-reset-btn");

    window.GameSettings = window.INITIAL_GAME_SETTINGS || {
        game_id: gameId,
        control_scheme: "hybrid",
        primary_key: "Space",
        secondary_key: "ArrowDown",
        difficulty: "easy",
        sound_enabled: true,
        show_hints: true,
    };

    function syncFormFromSettings(s) {
        document.getElementById("setting-control-scheme").value = s.control_scheme || "hybrid";
        document.getElementById("setting-primary-key").value = s.primary_key || "Space";
        document.getElementById("setting-secondary-key").value = s.secondary_key || "ArrowDown";
        document.getElementById("setting-difficulty").value = s.difficulty || "easy";
        document.getElementById("setting-sound").checked = Boolean(s.sound_enabled);
        document.getElementById("setting-hints").checked = Boolean(s.show_hints);
    }

    gearBtn?.addEventListener("click", () => {
        syncFormFromSettings(window.GameSettings);
        modal.classList.remove("hidden");
    });

    closeBtn?.addEventListener("click", () => modal.classList.add("hidden"));
    modal?.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.add("hidden");
    });

    form?.addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            control_scheme: document.getElementById("setting-control-scheme").value,
            primary_key: document.getElementById("setting-primary-key").value,
            secondary_key: document.getElementById("setting-secondary-key").value,
            difficulty: document.getElementById("setting-difficulty").value,
            sound_enabled: document.getElementById("setting-sound").checked,
            show_hints: document.getElementById("setting-hints").checked,
        };
        const res = await fetch(`/api/settings/${gameId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        if (res.ok) {
            window.GameSettings = await res.json();
            window.dispatchEvent(new CustomEvent("gamesettings:updated", { detail: window.GameSettings }));
            modal.classList.add("hidden");
        }
    });

    resetBtn?.addEventListener("click", async () => {
        const res = await fetch(`/api/settings/${gameId}/reset`, { method: "POST" });
        if (res.ok) {
            window.GameSettings = await res.json();
            syncFormFromSettings(window.GameSettings);
            window.dispatchEvent(new CustomEvent("gamesettings:updated", { detail: window.GameSettings }));
        }
    });
})();
