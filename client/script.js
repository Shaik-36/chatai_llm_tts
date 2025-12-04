// ================= Configuration of Client =======================
const WS_URL = 'ws://localhost:8000/ws';

let ws = null;
let currentAudio = null;

// ====================== DOM Elements ========================
const chat = document.getElementById('chat');
const input = document.getElementById('input');
const send = document.getElementById('send');
const dot = document.getElementById('dot');
const statusEl = document.getElementById('status');

// ======================= Init Function ======================
function init() {
  console.log("Client  Started")
  attachEventListeners();
  connectWebSocket();
}

// ======================= Start Point ======================
document.addEventListener('DOMContentLoaded', init);

// ================= Event Liseners and Handlers ===================
function attachEventListeners() {
  send.addEventListener('click', handleSendClick);
  input.addEventListener('keypress', handleInputKeypress);
}

function handleSendClick() {
  sendMessage();
}

function handleInputKeypress(e) {
  if (e.key === 'Enter') {
    sendMessage();
  }
}

// ======================= WebSocket Connection ======================
function connectWebSocket() {
  if (ws) {
    ws.close();
  }

  setStatus('Connecting...');
  ws = new WebSocket(WS_URL);

  ws.onopen = handleWsOpen;
  ws.onmessage = handleWsMessage;
  ws.onerror = handleWsError;
  ws.onclose = handleWsClose;
}

function handleWsOpen() {
  setStatus('Connected');
  dot.classList.add('connected');
  setInputEnabled(true);
  setSendEnabled(true);
}

function handleWsMessage(event) {
  const msg = JSON.parse(event.data);

  removeLoadingMessage();
  setSendEnabled(true);

  if (msg.type === 'audio') {
    // Stop any currently playing audio before playing the new one
    stopAudio();
    addMessage('AI Bot', msg.llm_text, 'assistant');
    console.log(msg.llm_text);
    playAudio(msg.audio_data);
  }
}

function handleWsError() {
  setStatus('Error');
  dot.className = 'status-dot';
}

function handleWsClose() {
  setStatus('Disconnected');
  setInputEnabled(false);
  setSendEnabled(false);
}

// ======================= Chat and Status Update Functions ======================
function setStatus(text) {
  statusEl.textContent = text;
}

function setInputEnabled(enabled) {
  input.disabled = !enabled;
}

function setSendEnabled(enabled) {
  send.disabled = !enabled;
}

function addMessage(sender, text, type) {
  const div = document.createElement('div');
  div.className = `msg ${type}`;
  div.textContent = `${sender}: ${text}`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function addLoadingMessage() {
  addMessage('AI Bot', 'Processing...', 'assistant');
}

function removeLoadingMessage() {
  const msgs = chat.querySelectorAll('.msg');
  if (msgs.length > 0) {
    const last = msgs[msgs.length - 1];
    // Optionally check for specific text if you only want to remove "Processing..." messages
    last.remove();
  }
}

// ======================= Messages Handling Functions ======================
function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  // Stop old audio when user sends a new message
  stopAudio();

  addMessage('You', text, 'user');
  input.value = '';

  setSendEnabled(false);
  addLoadingMessage();

  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ text }));
  } else {
    setStatus('Reconnecting...');
    connectWebSocket();
    // Optionally buffer message / re-send after reconnect logic here
  }
}

// ======================= Audio Handling Functions ======================
function stopAudio() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
  }
}

function playAudio(base64) {
  // Always stop any currently playing audio first
  stopAudio();

  const audio = new Audio(`data:audio/mp3;base64,${base64}`);
  currentAudio = audio;

  audio.play().catch((err) => {
    console.error('Audio playback error:', err);
    currentAudio = null;
  });

  audio.onended = () => {
    // Clear only if this is still the active audio
    if (currentAudio === audio) {
      currentAudio = null;
    }
  };
}
