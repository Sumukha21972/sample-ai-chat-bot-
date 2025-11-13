async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    if (userInput.value.trim() === "") return;

    chatBox.innerHTML += `<div><strong>You:</strong> ${userInput.value}</div>`;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput.value })
        });

        const data = await response.json();
        chatBox.innerHTML += `<div><strong>Bot:</strong> ${data.response || "No response."}</div>`;
    } catch (error) {
        chatBox.innerHTML += `<div><strong>Error:</strong> Unable to fetch response.</div>`;
    }

    userInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Handle enter key for sending messages
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
