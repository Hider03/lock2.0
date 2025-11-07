let conversationId = null;
let eventSource = null;

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', function () {
  // Extract conversation ID from URL path
  const path = window.location.pathname;
  const match = path.match(/\/pub\/chat\/([^\/]+)$/);
  if (match) {
    conversationId = match[1];
    console.log('Conversation ID:', conversationId);

    // Start SSE connection
    startSSEConnection();
  }

  const chatInput = document.getElementById('chatInput');
  const sendButton = document.getElementById('sendButton');

  sendButton.addEventListener('click', sendMessage);

  chatInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
});

const urlParams = new URLSearchParams(window.location.search);
const guestId = urlParams.get('guest');

// Start SSE connection with guest query param if present
function startSSEConnection() {
  if (eventSource) eventSource.close();

  let sseUrl = `/pub/chat/${conversationId}/stream`;
  if (guestId) sseUrl += `?guest=${guestId}`;

  eventSource = new EventSource(sseUrl);

  eventSource.onmessage = function (event) {
    try {
      const msg = JSON.parse(event.data);
      console.log('Received SSE message:', msg);
      addMessageToUI(msg);
    } catch (err) {
      console.error('Error parsing SSE message:', err);
    }
  };

  eventSource.onerror = function () {
    console.error('SSE connection error, reconnecting in 5s...');
    eventSource.close();
    setTimeout(startSSEConnection, 5000);
  };
}
function addMessageToUI(message) {
  const container = document.getElementById('messages');

  console.log('Adding message to UI:', message);
  const div = document.createElement('div');
  div.className = `message ${message.sender_type}`;
  div.id = `msg-${message.id}`;

  div.innerHTML = `
    <span class="timestamp">${message.timestamp}</span>
    <span class="sender">${message.sender_name}:</span>
    <span class="text">${message.content}</span>
  `;

  container.appendChild(div);
  scrollToBottom();
}

function scrollToBottom() {
  const container = document.getElementById('messages');
  container.scrollTop = container.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;

  try {
    const res = await fetch(`/pub/chat/${conversationId}/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: text })
    });

    if (res.ok) {
      input.value = '';
      input.focus();
    } else {
      console.error('Failed to send message');
    }
  } catch (err) {
    console.error('Error sending message:', err);
  }
}

// Clean up SSE on page unload
window.addEventListener('beforeunload', () => {
  if (eventSource) eventSource.close();
});
