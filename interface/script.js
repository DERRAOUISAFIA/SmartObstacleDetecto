// --- Fonction log (si tu as la section historique) ---
function logAction(message) {
  const logList = document.getElementById("log-list");
  if (!logList) return;

  const item = document.createElement("li");
  item.textContent = new Date().toLocaleTimeString() + " - " + message;
  logList.prepend(item);
}

// --- START bouton ---
document.getElementById("startBtn").addEventListener("click", () => {
  const status = document.getElementById("status");
  const mode = document.getElementById("mode").value;
  const camSource = document.querySelector('input[name="cam"]:checked').value;

  status.innerHTML =
    '<span class="status-dot" style="background-color: orange;"></span> 🧠 Lancement de la détection (' +
    mode +
    ")...";

  logAction("Tentative de démarrage en mode : " + mode);

  fetch("http://localhost:5000/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mode: mode }),
    body: JSON.stringify({ mode: mode, cam: camSource }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.text();
    })
    .then((txt) => {
      status.innerHTML =
        '<span class="status-dot" style="background-color: limegreen;"></span> ✅ ' +
        txt;

      logAction("Détection lancée (" + mode + ")");
    })
    .catch((err) => {
      status.innerHTML =
        '<span class="status-dot" style="background-color: red;"></span> ❌ Erreur lors du lancement';
      console.error("Erreur JS :", err);

      logAction("Erreur lors du lancement");
    });
});

// --- STOP bouton ---
document.getElementById("stopBtn").addEventListener("click", () => {
  const status = document.getElementById("status");

  status.innerHTML =
    '<span class="status-dot" style="background-color: orange;"></span> ⏳ Arrêt de la détection...';

  logAction("Tentative d'arrêt...");

  fetch("http://localhost:5000/stop")
    .then((res) => res.text())
    .then((txt) => {
      status.innerHTML =
        '<span class="status-dot" style="background-color: red;"></span> 🛑 ' +
        txt;

      logAction("Détection arrêtée");
    })
    .catch((err) => {
      status.innerHTML =
        '<span class="status-dot" style="background-color: red;"></span> ❌ Erreur lors de l\'arrêt';
      console.error("Erreur JS :", err);

      logAction("Erreur lors de l'arrêt");
    });
});

// --- Horloge ---
function updateClock() {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");
  document.getElementById(
    "clock"
  ).textContent = `${hours}:${minutes}:${seconds}`;
}

setInterval(updateClock, 1000);
updateClock();
