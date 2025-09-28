const canvas = document.getElementById('bg-candles');
const ctx = canvas.getContext('2d');
const smoothing = 0.008; // Чем меньше — тем быстрее реагирует масштаб по y

let candles = [];
let candleWidth = 200;
let gap = 4;
let scrollOffset = 0;
let speed = 0.05;
let currentIndex = 0;
let currentScaleMin = null;
let currentScaleMax = null;

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);

// === Подгрузка свечей из JSON ===
async function loadCandles() {
  try {
    const response = await fetch('/static/js/sp500_data.json');
    const data = await response.json();
    candles = data;
  } catch (err) {
    console.error("Не удалось загрузить свечи:", err);
  }
}

function drawCandles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (!candles.length) return;

  const visibleCount = Math.ceil(canvas.width / (candleWidth + gap)) + 2;
  let visibleCandles = [];

  for (let i = 0; i < visibleCount; i++) {
    const dataIndex = (currentIndex + i) % candles.length;
    visibleCandles.push(candles[dataIndex]);
  }

  const max = Math.max(...visibleCandles.map(c => c.high));
  const min = Math.min(...visibleCandles.map(c => c.low));

  if (currentScaleMax === null || currentScaleMin === null) {
    currentScaleMax = max;
    currentScaleMin = min;
  } else {
    currentScaleMax = currentScaleMax * (1 - smoothing) + max * smoothing;
    currentScaleMin = currentScaleMin * (1 - smoothing) + min * smoothing;
  }

  const scale = canvas.height / (currentScaleMax - currentScaleMin);

  for (let i = 0; i < visibleCount; i++) {
    const dataIndex = (currentIndex + i) % candles.length;
    const c = candles[dataIndex];
    const x = i * (candleWidth + gap) - scrollOffset;

    const openY = canvas.height - (c.open - currentScaleMin) * scale;
    const closeY = canvas.height - (c.close - min) * scale;
    const highY = canvas.height - (c.high - min) * scale;
    const lowY = canvas.height - (c.low - min) * scale;

    const color = c.close >= c.open ? 'rgba(16, 66, 78, 0.6)' : 'rgba(0, 40, 50, 0.6)';

    // тень
    ctx.beginPath();
    ctx.moveTo(x + candleWidth / 2, highY);
    ctx.lineTo(x + candleWidth / 2, lowY);
    ctx.strokeStyle = color;
    ctx.stroke();

    // тело
    ctx.fillStyle = color;
    ctx.fillRect(x, Math.min(openY, closeY), candleWidth, Math.abs(openY - closeY));
  }
}

function animate() {
  scrollOffset += speed;

  const threshold = candleWidth + gap;
  if (scrollOffset >= threshold) {
    scrollOffset -= threshold;
    currentIndex = (currentIndex + 1) % candles.length;
  }

  drawCandles();
  requestAnimationFrame(animate);
}

// === Старт ===
resizeCanvas();
loadCandles().then(() => {
  animate();
});
