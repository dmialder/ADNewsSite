const canvas = document.getElementById('bg-candles');
const ctx = canvas.getContext('2d');
const scrollRoot = document.querySelector('.snap-container');
const smoothing = 0.008; // Чем меньше — тем быстрее реагирует масштаб по y

let candles = [];
let candleWidth = 25;
let gap = 4;
let scrollOffset = 0;
let speed = 0.005;
let currentIndex = 0;
let currentScaleMin = null;
let currentScaleMax = null;
let targetScaleMin = null;
let targetScaleMax = null;
let visibleCandles = [];
let visibleCount = 0;

function resizeCanvas() {
  if (!scrollRoot) return;
  canvas.width = scrollRoot.clientWidth;
  canvas.height = scrollRoot.scrollHeight;
  canvas.style.height = `${scrollRoot.scrollHeight}px`;
  rebuildVisible();
}

window.addEventListener('resize', resizeCanvas);

// === Подгрузка свечей из JSON ===
async function loadCandles() {
  try {
    const response = await fetch('/static/js/sp500_data.json');
    const data = await response.json();
    candles = data;
    rebuildVisible();
  } catch (err) {
    console.error("Не удалось загрузить свечи:", err);
  }
}

function rebuildVisible() {
  if (!candles.length || !canvas.width) return;

  visibleCount = Math.ceil(canvas.width / (candleWidth + gap)) + 2;
  visibleCandles = [];

  for (let i = 0; i < visibleCount; i++) {
    const dataIndex = (currentIndex + i) % candles.length;
    visibleCandles.push(candles[dataIndex]);
  }

  updateScaleTarget();
}

function updateScaleTarget() {
  if (!visibleCandles.length) return;

  targetScaleMax = Math.max(...visibleCandles.map(c => c.high));
  targetScaleMin = Math.min(...visibleCandles.map(c => c.low));

  if (currentScaleMax === null || currentScaleMin === null) {
    currentScaleMax = targetScaleMax;
    currentScaleMin = targetScaleMin;
  }
}

function drawCandles() {
  if (!scrollRoot) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (!visibleCandles.length || targetScaleMax === null || targetScaleMin === null) return;

  currentScaleMax = currentScaleMax * (1 - smoothing) + targetScaleMax * smoothing;
  currentScaleMin = currentScaleMin * (1 - smoothing) + targetScaleMin * smoothing;

  const scale = canvas.height / (currentScaleMax - currentScaleMin);
  const baseY = canvas.height;

  for (let i = 0; i < visibleCount; i++) {
    const c = visibleCandles[i];
    const x = i * (candleWidth + gap) - scrollOffset;

    const openY = baseY - (c.open - currentScaleMin) * scale;
    const closeY = baseY - (c.close - currentScaleMin) * scale;
    const highY = baseY - (c.high - currentScaleMin) * scale;
    const lowY = baseY - (c.low - currentScaleMin) * scale;

    const strokeColor = 'rgba(0, 0, 0, 1)';
    const fillColor = 'rgba(255, 255, 255, 1)';

    // тень
    ctx.beginPath();
    ctx.moveTo(x + candleWidth / 2, highY);
    ctx.lineTo(x + candleWidth / 2, lowY);
    ctx.strokeStyle = strokeColor;
    ctx.stroke();

    // тело
    ctx.fillStyle = fillColor;
    ctx.fillRect(x, Math.min(openY, closeY), candleWidth, Math.abs(openY - closeY));
    ctx.strokeRect(x, Math.min(openY, closeY), candleWidth, Math.abs(openY - closeY));
  }
}

function animate() {
  scrollOffset += speed;

  const threshold = candleWidth + gap;
  if (scrollOffset >= threshold) {
    scrollOffset -= threshold;
    currentIndex = (currentIndex + 1) % candles.length;
    if (visibleCandles.length) {
      const nextIndex = (currentIndex + visibleCount - 1) % candles.length;
      visibleCandles.shift();
      visibleCandles.push(candles[nextIndex]);
      updateScaleTarget();
    }
  }

  drawCandles();
  requestAnimationFrame(animate);
}

// === Старт ===
resizeCanvas();
loadCandles().then(() => {
  animate();
});
