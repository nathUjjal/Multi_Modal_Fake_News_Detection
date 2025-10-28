const attachBtn = document.getElementById('attachBtn');
const fileInput = document.getElementById('fileInput');
const micBtn = document.getElementById('micBtn');
const voiceBtn = document.getElementById('voiceBtn');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');

let recognition;
let processingTimeout;
let isProcessing = false;

/* ---------------- FILE UPLOAD ---------------- */
attachBtn.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', (e) => {
  const files = Array.from(e.target.files);
  if (files.length > 0) {
    attachBtn.style.color = '#00a67e'; // turn green
    alert(`Attached ${files.length} file(s):\n` + files.map(f => f.name).join('\n'));
  }
});

/* ---------------- VOICE INPUT ---------------- */
if ('webkitSpeechRecognition' in window) {
  recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  micBtn.addEventListener('click', () => {
    recognition.start();
    micBtn.style.color = '#00a67e';
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    userInput.value = transcript;
    micBtn.style.color = '#cfcfcf';
  };

  recognition.onerror = () => {
    micBtn.style.color = '#cfcfcf';
    alert('Voice input not available.');
  };
} else {
  micBtn.addEventListener('click', () => {
    alert('Speech recognition not supported in this browser.');
  });
}

/* ---------------- VOICE OUTPUT ---------------- */
voiceBtn.addEventListener('click', () => {
  const text = userInput.value.trim();
  if (!text) return alert('Type a message first!');
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = 'en-US';
  speechSynthesis.speak(utter);
});

/* ---------------- SEND / STOP BUTTON ---------------- */
sendBtn.addEventListener('click', () => {
  if (!isProcessing) sendMessage();
  else stopProcessing();
});

userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    if (!isProcessing) sendMessage();
  }
});

function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  isProcessing = true;
  userInput.value = '';

  // Change send to stop
  sendBtn.innerHTML = '<i class="fa-solid fa-stop"></i>';
  sendBtn.classList.add('stop-btn');

  // Simulate processing
  processingTimeout = setTimeout(() => {
    finishProcessing(`Message processed: "${message}"`);
  }, 3000);
}

function stopProcessing() {
  clearTimeout(processingTimeout);
  finishProcessing('Processing stopped.');
}

function finishProcessing(message) {
  isProcessing = false;
  sendBtn.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
  sendBtn.classList.remove('stop-btn');
  alert(message);
}
