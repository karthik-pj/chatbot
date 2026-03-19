document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = text;
        
        msgDiv.appendChild(bubble);
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function addTypingIndicator() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message assistant typing';
        msgDiv.id = 'typing-indicator';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble typing-indicator';
        bubble.innerHTML = '<span></span><span></span><span></span>';
        
        msgDiv.appendChild(bubble);
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;

        // Add user message
        addMessage(msg, true);
        chatInput.value = '';
        sendBtn.disabled = true;

        // Add loading state
        addTypingIndicator();

        try {
            const response = await fetch('/chat/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: msg })
            });

            const data = await response.json();
            
            removeTypingIndicator();
            if (response.ok) {
                addMessage(data.response);
            } else {
                addMessage("Sorry, I encountered an error communicating with the server.");
            }
        } catch (error) {
            removeTypingIndicator();
            addMessage("Network error occurred.");
            console.error('Error:', error);
        } finally {
            sendBtn.disabled = false;
            chatInput.focus();
        }
    });
});
