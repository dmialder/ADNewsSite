const canvas = document.getElementById('bg-candles');
const ctx = canvas.getContext('2d');

let candles = [];
let candleWidth = 30;
let gap = 4;
let scrollOffset = 0;
let speed = 0.1;  // скорость прокрутки (меньше — плавнее)
let lastClose = 100 + Math.random() * 20;

function generateCandle(prevClose) {
  const open = prevClose;
  const close = open + (Math.random() - 0.5) * 10;
  const high = Math.max(open, close) + Math.random() * 5;
  const low = Math.min(open, close) - Math.random() * 5;
  return { open, close, high, low };
}

function initCandles() {
  const totalCandles = Math.ceil(window.innerWidth / (candleWidth + gap)) + 10;
  candles = [];
  let price = lastClose;
  for (let i = 0; i < totalCandles; i++) {
    const c = generateCandle(price);
    candles.push(c);
    price = c.close;
  }
  lastClose = price;
}

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  initCandles();
}
window.addEventListener('resize', resizeCanvas);

function drawCandles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const max = Math.max(...candles.map(c => c.high));
  const min = Math.min(...candles.map(c => c.low));
  const scale = canvas.height / (max - min);

  for (let i = 0; i < candles.length; i++) {
    const x = i * (candleWidth + gap) - scrollOffset;
    if (x > canvas.width) continue;

    const c = candles[i];
    const openY = canvas.height - (c.open - min) * scale;
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
    candles.shift();
    const newCandle = generateCandle(candles[candles.length - 1].close);
    candles.push(newCandle);
  }

  drawCandles();
  requestAnimationFrame(animate);
}

resizeCanvas();
animate();
