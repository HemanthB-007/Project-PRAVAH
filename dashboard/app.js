/* ============================================================
   PRAVAH — Flood Intelligence Platform  |  app.js
   ============================================================ */

"use strict";

// ── State ────────────────────────────────────────────────────
const state = {
  currentRisk: "LOW",
  floodProbability: 0,
  isSimulating: false,
  lastUpdated: new Date(),
};

// ── Rain Canvas ──────────────────────────────────────────────
(function initRainCanvas() {
  const canvas = document.getElementById("rain-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener("resize", resize);

  const drops = Array.from({ length: 120 }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    len: Math.random() * 18 + 8,
    speed: Math.random() * 2.5 + 1.5,
    opacity: Math.random() * 0.35 + 0.05,
  }));

  let rainIntensity = 0.3; // 0 = none, 1 = heavy

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = `rgba(100, 160, 220, 1)`;
    ctx.lineWidth = 0.8;

    drops.forEach(d => {
      ctx.globalAlpha = d.opacity * rainIntensity;
      ctx.beginPath();
      ctx.moveTo(d.x, d.y);
      ctx.lineTo(d.x - d.len * 0.15, d.y + d.len);
      ctx.stroke();

      d.y += d.speed * (1 + rainIntensity);
      if (d.y > canvas.height + d.len) {
        d.y = -d.len;
        d.x = Math.random() * canvas.width;
      }
    });

    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }

  draw();

  // Expose so predictFlood can update intensity
  window.setRainIntensity = (v) => { rainIntensity = Math.min(1, Math.max(0, v)); };
})();

// ── Chart ────────────────────────────────────────────────────
const chartCtx = document.getElementById("rainChart").getContext("2d");
const rainChart = new Chart(chartCtx, {
  type: "line",
  data: {
    labels: ["Day −6", "Day −5", "Day −4", "Day −3", "Day −2", "Day −1", "Now"],
    datasets: [{
      label: "Rainfall (mm)",
      data: [20, 30, 40, 50, 60, 70, 80],
      borderColor: "#3b9eff",
      backgroundColor: "rgba(59, 158, 255, 0.06)",
      fill: true,
      tension: 0.45,
      pointBackgroundColor: "#3b9eff",
      pointBorderColor: "rgba(59, 158, 255, 0.25)",
      pointBorderWidth: 4,
      pointRadius: 4,
      pointHoverRadius: 7,
    }],
  },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "rgba(11, 24, 41, 0.95)",
        borderColor: "rgba(0, 212, 255, 0.3)",
        borderWidth: 1,
        titleColor: "#3b9eff",
        bodyColor: "#5b84a8",
        titleFont: { family: "'JetBrains Mono', monospace", size: 11 },
        bodyFont:  { family: "'Syne', sans-serif", size: 12 },
        padding: 12,
      },
    },
    scales: {
      x: {
        grid: { color: "rgba(59, 158, 255, 0.06)" },
        ticks: {
          color: "#2a4a6a",
          font: { family: "'JetBrains Mono', monospace", size: 9 },
        },
        border: { color: "rgba(59, 158, 255, 0.08)" },
      },
      y: {
        grid: { color: "rgba(59, 158, 255, 0.06)" },
        ticks: {
          color: "#2a4a6a",
          font: { family: "'JetBrains Mono', monospace", size: 9 },
          callback: v => v + " mm",
        },
        border: { color: "rgba(59, 158, 255, 0.08)" },
      },
    },
    animation: { duration: 400, easing: "easeInOutQuart" },
  },
});

// ── Gauge ────────────────────────────────────────────────────
const gaugeFill = document.getElementById("gauge-fill");
const CIRCUMFERENCE = 408; // 2π × r = 2π × 65 ≈ 408

function updateGauge(probability) {
  const offset = CIRCUMFERENCE * (1 - probability);
  gaugeFill.style.strokeDashoffset = offset;

  let color;
  if (probability > 0.65)      color = "var(--alert-high)";
  else if (probability > 0.35) color = "var(--alert-mid)";
  else                          color = "var(--alert-low)";

  gaugeFill.style.stroke = color;

  const pct = Math.round(probability * 100);
  document.getElementById("gauge-percent").textContent = pct + "%";
}

// ── Slider Track Fill ────────────────────────────────────────
const slider = document.getElementById("rainSlider");
const trackFill = document.getElementById("slider-track-fill");

function updateSliderTrack() {
  const pct = (slider.value - slider.min) / (slider.max - slider.min) * 100;
  trackFill.style.width = pct + "%";
  document.getElementById("rainValueDisplay").textContent = parseFloat(slider.value).toFixed(0);
}

slider.addEventListener("input", () => {
  updateSliderTrack();
  predictFlood();
});

// ── Predict Flood ────────────────────────────────────────────
async function predictFlood() {
  const rainfall = parseFloat(slider.value);
  updateSliderTrack();

  // Update rain canvas intensity (0–200mm → 0–1)
  if (window.setRainIntensity) window.setRainIntensity(rainfall / 200);

  // Chart data
  rainChart.data.datasets[0].data = [
    +(rainfall * 0.25).toFixed(1),
    +(rainfall * 0.40).toFixed(1),
    +(rainfall * 0.60).toFixed(1),
    +(rainfall * 0.80).toFixed(1),
    +(rainfall * 0.95).toFixed(1),
    +(rainfall * 1.10).toFixed(1),
    +rainfall.toFixed(1),
  ];
  rainChart.update();

  const r3 = rainfall * 0.8;
  const r7 = rainfall * 1.2;

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/predict?rainfall_mm=${rainfall}&rainfall_3day_avg=${r3}&rainfall_7day_avg=${r7}`,
      { method: "POST" }
    );
    if (!res.ok) throw new Error("API Offline");
    const data = await res.json();

    applyRiskState(data.risk_level, data.flood_probability);

    // Post to map iframe
    const mapFrame = document.getElementById("mapFrame");
    if (mapFrame?.contentWindow) {
      mapFrame.contentWindow.postMessage({
        zones: data.zone_predictions,
        overall_prob: data.flood_probability,
      }, "*");
    }

    updateLastUpdated();
  } catch {
    // Fallback: compute locally from rainfall value
    let prob, risk;
    if (rainfall >= 120) {
      prob = 0.75 + Math.min(0.25, (rainfall - 120) / 320);
      risk = "HIGH";
    } else if (rainfall >= 60) {
      prob = 0.35 + ((rainfall - 60) / 60) * 0.40;
      risk = "MODERATE";
    } else {
      prob = Math.max(0.02, rainfall / 200 * 0.35);
      risk = "LOW";
    }
    applyRiskState(risk, prob);
  }
}

// ── Apply Risk State ─────────────────────────────────────────
function applyRiskState(riskLevel, probability) {
  state.currentRisk = riskLevel;
  state.floodProbability = probability;

  updateGauge(probability);

  const badge  = document.getElementById("risk-badge");
  const riskCard = document.querySelector(".card--risk");

  // Color configs
  const cfg = {
    HIGH:     { badge: "rgba(255, 51, 85, 0.15)", border: "rgba(255, 51, 85, 0.4)", color: "var(--alert-high)", label: "HIGH RISK", icon: "🚨", title: "CRITICAL FLOOD WARNING", action: "Initiate emergency protocols. Low-lying wards are at severe inundation risk. Deploy SDRF teams and advise immediate evacuation of vulnerable zones.", steps: ["Issue public emergency alerts via all channels", "Evacuate wards in topological depressions", "Deploy SDRF teams to high-risk zones", "Open emergency shelters — capacity check required"], dot: "#ff3355" },
    MODERATE: { badge: "rgba(255, 179, 0, 0.15)", border: "rgba(255, 179, 0, 0.35)", color: "var(--alert-mid)", label: "MODERATE RISK", icon: "⚠️", title: "ELEVATED FLOOD RISK", action: "Severe waterlogging expected in low-lying areas. Dispatch clearing teams to primary drainage networks and closely monitor lake capacities.", steps: ["Alert municipal drainage & clearing crews", "Monitor lake and reservoir water levels", "Prepare evacuation routes as precaution", "Issue public advisory for low-lying residents"], dot: "#ffb300" },
    LOW:      { badge: "rgba(34, 197, 94, 0.10)", border: "rgba(34, 197, 94, 0.22)", color: "var(--alert-low)", label: "LOW RISK", icon: "✅", title: "NORMAL CONDITIONS", action: "Standard operating procedures. No severe infrastructure threats detected at current rainfall levels.", steps: ["Continue routine drainage maintenance", "Monitor weather forecasts", "Maintain operational readiness", "Log current sensor readings"], dot: "#22c55e" },
  };

  const c = cfg[riskLevel] ?? cfg.LOW;

  badge.textContent  = c.label;
  badge.style.background = c.badge;
  badge.style.borderColor = c.border;
  badge.style.color      = c.color;

  riskCard.className = `card card--risk${riskLevel === "HIGH" ? " alert-high" : ""}`;

  // Protocol panel
  const protoStatus = document.getElementById("protocol-status");
  const protoIcon   = document.getElementById("protocol-icon");
  const protoTitle  = document.getElementById("protocol-title");
  const protoAction = document.getElementById("protocol-action");
  const stepsList   = document.getElementById("protocol-steps");
  const ribbonDot   = document.getElementById("ribbon-dot");

  protoStatus.style.background   = c.badge;
  protoStatus.style.borderColor  = c.border;
  protoIcon.textContent          = c.icon;
  protoTitle.textContent         = c.title;
  protoTitle.style.color         = c.color;
  protoAction.textContent        = c.action;

  stepsList.innerHTML = c.steps.map((s, i) =>
    `<div class="protocol-step" style="border-left-color:${c.color}">
      <span class="step-num">0${i + 1}</span>
      <span class="step-text">${s}</span>
    </div>`
  ).join("");

  ribbonDot.style.background    = c.dot;
  ribbonDot.style.boxShadow     = `0 0 8px ${c.dot}`;

  const rainDisplay = parseFloat(slider.value).toFixed(0) + " mm";
  document.getElementById("ribbon-risk").textContent        = c.label;
  document.getElementById("ribbon-risk").style.color        = c.color;
  document.getElementById("ribbon-prob").textContent        = (probability * 100).toFixed(1) + "%";
  document.getElementById("ribbon-rain").textContent        = rainDisplay;
  const ribbonRainRibbon = document.getElementById("ribbon-rain-ribbon");
  if (ribbonRainRibbon) ribbonRainRibbon.textContent        = rainDisplay;
}

// ── Live Weather ─────────────────────────────────────────────
async function fetchLiveWeather() {
  const btn = document.getElementById("btn-weather");
  btn.disabled = true;
  btn.querySelector(".ctrl-btn-desc").textContent = "Fetching data…";

  try {
    const res  = await fetch("https://api.open-meteo.com/v1/forecast?latitude=13.0827&longitude=80.2707&daily=precipitation_sum&past_days=7&timezone=Asia%2FKolkata");
    const data = await res.json();
    const today = data.daily.precipitation_sum[7] ?? 0;

    slider.value = today;
    updateSliderTrack();
    await predictFlood();

    btn.querySelector(".ctrl-btn-desc").textContent = `Loaded — ${today} mm today`;
  } catch {
    btn.querySelector(".ctrl-btn-desc").textContent = "Failed to fetch — retrying…";
  } finally {
    btn.disabled = false;
  }
}

// ── Cyclone Michaung Simulation ───────────────────────────────
async function simulateMichaung() {
  if (state.isSimulating) return;
  state.isSimulating = true;

  const simData = [
    { day: "Dec 1, 2023", rain: 15,  label: "Pre-storm" },
    { day: "Dec 2, 2023", rain: 45,  label: "Approach" },
    { day: "Dec 3, 2023", rain: 120, label: "Landfall" },
    { day: "Dec 4, 2023", rain: 340, label: "Peak Flooding" },
  ];

  const progress = document.getElementById("sim-progress");
  const dayLabel = document.getElementById("sim-day-label");
  const btn      = document.getElementById("btn-simulate");

  progress.style.display = "block";
  dayLabel.style.display = "block";
  btn.disabled = true;

  for (let i = 0; i < simData.length; i++) {
    const d = simData[i];
    slider.value = d.rain;
    updateSliderTrack();

    dayLabel.textContent = `▶ ${d.day} — ${d.label} (${d.rain} mm)`;
    progress.querySelector(".sim-progress-bar").style.width = `${((i + 1) / simData.length) * 100}%`;

    await predictFlood();
    await new Promise(r => setTimeout(r, 2500));
  }

  dayLabel.textContent = "✓ Simulation complete";
  btn.disabled = false;
  state.isSimulating = false;
}

// ── PDF Export ───────────────────────────────────────────────
function generatePDFReport() {
  const el  = document.body;
  const opt = {
    margin: 0.5,
    filename: `PRAVAH_Risk_Report_${new Date().toISOString().slice(0, 10)}.pdf`,
    image: { type: "jpeg", quality: 0.97 },
    html2canvas: { scale: 2, useCORS: true },
    jsPDF: { unit: "in", format: "letter", orientation: "landscape" },
  };
  html2pdf().set(opt).from(el).save();
}

// ── Clock & Last Updated ─────────────────────────────────────
function updateClock() {
  const now = new Date();
  const t   = now.toLocaleTimeString("en-IN", { hour12: false });
  const d   = now.toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
  document.getElementById("live-clock").textContent  = t;
  document.getElementById("live-date").textContent   = d;
}

function updateLastUpdated() {
  state.lastUpdated = new Date();
  document.getElementById("last-updated").textContent = state.lastUpdated.toLocaleTimeString("en-IN", { hour12: false });
}

setInterval(updateClock, 1000);
updateClock();

// ── Boot ─────────────────────────────────────────────────────
window.addEventListener("load", () => {
  updateSliderTrack();
  predictFlood();
  console.log("PRAVAH v2.0 — Flood Intelligence Platform initialized ✅");
});

// Expose to HTML onclick
window.fetchLiveWeather    = fetchLiveWeather;
window.simulateMichaung    = simulateMichaung;
window.generatePDFReport   = generatePDFReport;
