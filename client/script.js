const WS_URL = 'ws://localhost:8000/ws';

const chat = document.getElementById('chat');
const input = document.getElementById('input');
const send = document.getElementById('send');
const dot = document.getElementById('dot');
const status = document.getElementById('status');

let ws = null;
let currentAudio = null;


function init() {
    send.addEventListener('click', sendMsg);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMsg();
    });
    connect();
}


function connect() {
    if (ws) ws.close();
    status.textContent = 'Connecting...';
    ws = new WebSocket(WS_URL);
    
    ws.onopen = () => {
        status.textContent = 'Connected';
        dot.classList.add('connected');
        input.disabled = false;
        send.disabled = false;
    };
    
    ws.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        removeLoading();
        send.disabled = false
        if (msg.type === 'audio') {
            stopAudio();
            addMsg('AI Bot', msg.llm_text, 'assistant');
            playAudio(msg.audio_data);
        }
    };
    
    ws.onerror = () => {
        status.textContent = 'Error';
        dot.className = 'status-dot';
    };
    
    ws.onclose = () => {
        status.textContent = 'Disconnected';
        input.disabled = true;
        send.disabled = true;
    };
}


function sendMsg() {
    const text = input.value.trim();
    if (!text) return;
    
    stopAudio();
    addMsg('You', text, 'user');
    input.value = '';
    
    send.disabled = true;
    addMsg('AI Bot', 'Processing...', 'assistant');
    
    ws.send(JSON.stringify({ text }));
}


function stopAudio() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }
}


function playAudio(base64) {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    const blob = new Blob([bytes], { type: 'audio/mp3' });
    currentAudio = new Audio(URL.createObjectURL(blob));
    currentAudio.play();
    currentAudio.onended = () => { currentAudio = null; };
}


function addMsg(sender, text, type) {
    const div = document.createElement('div');
    div.className = `msg ${type}`;
    div.textContent = `${sender}: ${text}`;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}


function removeLoading() {
    const msgs = chat.querySelectorAll('.msg');
    if (msgs.length > 0) msgs[msgs.length - 1].remove();
}


document.addEventListener('DOMContentLoaded', init);
