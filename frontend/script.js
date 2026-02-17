async function sendMessage() {
    const input = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const userMessage = input.value;
    chatBox.innerHTML += `<div><strong>You:</strong> ${userMessage}</div>`;
    input.value = '';

    const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    });
    const data = await response.json();
    chatBox.innerHTML += `<div><strong>Bot:</strong> ${data.reply}</div>`;
    speakText(data.reply);
}

function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}

function startVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function(event) {
        document.getElementById('user-input').value = event.results[0][0].transcript;
        sendMessage();
    };
}
