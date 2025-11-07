async function loadChats() {
    // Check if user is logged in
    const res = await fetch("/userinfo", { method: "GET", credentials: "include" });
    if (!res.ok) {
        window.location.href = "/login";
        return;
    }

    // Fetch user's conversations
    const chatsRes = await fetch("/api/priv/mychats", { method: "GET", credentials: "include" });
    const chats = await chatsRes.json();
    const chatsList = document.getElementById("chatsList");
    chatsList.innerHTML = ""; // clear loading text

    if (!chats || chats.length === 0) {
        chatsList.textContent = "You have no conversations yet.";
        return;
    }

    for (const conv of chats) {
        const card = document.createElement("div");
        card.className = "chat-card";

        // Display last message or placeholder
        const lastMsg = conv.messages && conv.messages.length > 0
            ? conv.messages[conv.messages.length - 1].message_content
            : "(No messages yet)";

        card.innerHTML = `
      <h3>
        <a href="/priv/chat/${conv.id}" class="chat-link">
          Conversation with ${conv.finder_contact || "Guest"}
        </a>
      </h3>
      <p class="chat-info">
        <strong>Last message:</strong> ${lastMsg}
      </p>
      <p class="chat-actions">
        <a href="/priv/chat/${conv.id}" class="chat-link">Open Chat</a>
        |
        <a href="/pub/chat/${conv.id}" class="chat-link" target="_blank">Public Link</a>
      </p>
    `;

        chatsList.appendChild(card);
    }
}

// Run on page load
document.addEventListener("DOMContentLoaded", loadChats);
