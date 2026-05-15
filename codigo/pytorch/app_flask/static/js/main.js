// raptors-cnn — Flask app frontend logic

const el = (id) => document.getElementById(id);
const show = (id) => el(id).classList.remove("hidden");
const hide = (id) => el(id).classList.add("hidden");

// Estado de la última predicción
let lastPrediction = null;

// Paleta circular para top-3 bars
const SPECIES_COLORS = [
  "#1A6E68", "#D7644C", "#2E5984", "#8B5A2B", "#5C4DA8",
  "#3F8E5A", "#C26B41", "#4A6FA5", "#7B4C77", "#3E7D7D",
];

// ─── Eventos de upload ──────────────────────────────
el("btn-pick-image").addEventListener("click", () => el("file-input").click());
el("btn-pick-video").addEventListener("click", () => el("video-input").click());

el("file-input").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    el("preview-image").src = ev.target.result;
    show("preview-section");
    hide("result-section");
  };
  reader.readAsDataURL(file);
});

el("btn-cancel-preview").addEventListener("click", () => {
  el("file-input").value = "";
  hide("preview-section");
});

el("btn-identify").addEventListener("click", async () => {
  const file = el("file-input").files[0];
  if (!file) return;
  hide("preview-section");
  show("loading-section");

  const fd = new FormData();
  fd.append("image", file);
  try {
    const r = await fetch("/identify", { method: "POST", body: fd });
    const data = await r.json();
    hide("loading-section");
    if (data.error) {
      alert("Error: " + data.error);
      show("preview-section");
      return;
    }
    lastPrediction = data;
    renderResult(data);
    show("result-section");
    el("result-section").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    hide("loading-section");
    alert("Error de red: " + err);
  }
});

// ─── Render del resultado ──────────────────────────
function renderResult(data) {
  const best = data.best;

  // Banner principal
  el("r-common").textContent = best.common_es || best.common_en;
  el("r-scientific").textContent = best.scientific_name;
  el("r-confidence").textContent = `${best.confidence_pct.toFixed(1)} %`;

  // Color del banner por especie (paleta circular)
  const colorIdx = (best.code.charCodeAt(0) + best.code.charCodeAt(1 || 0)) % SPECIES_COLORS.length;
  const color = SPECIES_COLORS[colorIdx];
  el("result-banner").style.background = `linear-gradient(135deg, ${color} 0%, ${darken(color)} 100%)`;

  // Alerta baja confianza
  if (data.low_confidence) {
    show("alert-low-conf");
  } else {
    hide("alert-low-conf");
  }

  // Info de la especie
  el("r-iucn").textContent       = best.iucn_status || "—";
  el("r-habitat").textContent    = best.habitat || best.distribution || "—";
  el("r-length").textContent     = best.length_cm || "—";
  el("r-wingspan").textContent   = best.wingspan_cm || "—";
  el("r-diagnostic").textContent = best.diagnostic || "—";
  el("r-best-months").textContent= best.best_months || "—";
  el("r-did-you-know").textContent = best.did_you_know || "—";

  // Seña
  el("r-sign-header").textContent = `${best.code} — ${best.common_en}`;
  el("r-sign-sub").textContent    = best.scientific_name;
  el("r-sign-desc").textContent   = "Seña en International Sign — pendiente de validación con la comunidad sorda.";
  el("r-sign-card").style.background = `linear-gradient(135deg, ${color} 0%, ${darken(color)} 100%)`;

  // Top-3 bars
  const ul = el("r-top3");
  ul.innerHTML = "";
  const medals = ["🥇", "🥈", "🥉"];
  data.top_k.forEach((p, i) => {
    const li = document.createElement("li");
    const c = SPECIES_COLORS[(p.code.charCodeAt(0) + (p.code.charCodeAt(1) || 0)) % SPECIES_COLORS.length];
    li.innerHTML = `
      <span class="top3-medal">${medals[i] || "🏅"}</span>
      <span class="top3-name">${p.common_es || p.common_en}</span>
      <div class="top3-bar-wrap"><div class="top3-bar" style="width:${p.confidence_pct}%;background:${c};"></div></div>
      <span class="top3-pct">${p.confidence_pct.toFixed(1)}%</span>
    `;
    ul.appendChild(li);
  });

  // Llenar dropdown del selector
  const sel = el("select-true-species");
  sel.innerHTML = '<option value="">— elegir —</option>';
  SPECIES.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s.sci;
    opt.textContent = s.sci.replace(/_/g, " ");
    sel.appendChild(opt);
  });

  // Reset feedback / observación
  hide("correct-species-selector");
  el("feedback-status").textContent = "";
  el("obs-status").textContent = "";
}

function darken(hex) {
  // simple darken por 12%
  const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
  const f = 0.78;
  return `#${[r,g,b].map(x => Math.max(0, Math.floor(x*f)).toString(16).padStart(2,"0")).join("")}`;
}

// ─── Active learning: ¿fue correcta? ──────────────────
el("btn-correct").addEventListener("click", async () => {
  if (!lastPrediction) return;
  await postFeedback("correct");
  el("feedback-status").textContent = "✓ Confirmación guardada. ¡Gracias!";
});

el("btn-incorrect").addEventListener("click", () => {
  show("correct-species-selector");
});

el("btn-submit-correction").addEventListener("click", async () => {
  const trueSci = el("select-true-species").value;
  if (!trueSci) {
    el("feedback-status").textContent = "Elige la especie correcta antes de enviar.";
    return;
  }
  await postFeedback("incorrect", trueSci);
  el("feedback-status").textContent = `📝 Corrección guardada (era ${lastPrediction.best.code}, ahora ${trueSci.replace(/_/g," ")}).`;
});

async function postFeedback(decision, trueSci = "") {
  return fetch("/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      upload_id: lastPrediction.upload_id,
      decision,
      predicted_code: lastPrediction.best.code,
      predicted_species: lastPrediction.best.scientific_underscored,
      true_species: trueSci,
    }),
  });
}

// ─── Guardar observación ───────────────────────────
el("btn-save-obs").addEventListener("click", async () => {
  if (!lastPrediction) return;
  const lat = el("obs-lat").value;
  const lon = el("obs-lon").value;
  const notes = el("obs-notes").value;
  const r = await fetch("/save_observation", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      species_scientific: lastPrediction.best.scientific_underscored,
      species_common: lastPrediction.best.common_en,
      species_code: lastPrediction.best.code,
      confidence: lastPrediction.best.confidence_pct / 100,
      image_filename: lastPrediction.upload_filename,
      latitude: lat,
      longitude: lon,
      notes,
    }),
  });
  const data = await r.json();
  if (data.ok) {
    el("obs-status").textContent = `📍 Observación ${data.observation_id} guardada.`;
  }
});

el("btn-new-id").addEventListener("click", () => {
  el("file-input").value = "";
  hide("result-section");
  window.scrollTo({ top: 0, behavior: "smooth" });
});
