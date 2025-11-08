// Chatbot functionality
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// Add user message to chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = isUser ? '👤' : '🤖';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = content;
    
    if (isUser) {
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = 'typing-indicator-msg';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';
    
    const typing = document.createElement('div');
    typing.className = 'typing-indicator active';
    typing.innerHTML = '<span></span><span></span><span></span>';
    
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(typing);
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function hideTyping() {
    const typingMsg = document.getElementById('typing-indicator-msg');
    if (typingMsg) {
        typingMsg.remove();
    }
}

// Send message to chatbot
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message
    addMessage(message, true);
    userInput.value = '';
    
    // Disable input
    sendBtn.disabled = true;
    userInput.disabled = true;
    
    // Show typing
    showTyping();
    
    try {
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Hide typing
        hideTyping();
        
        if (data.success) {
            addMessage(data.response);
        } else {
            addMessage('Sorry, I encountered an error. Please try again! 😅');
        }
    } catch (error) {
        hideTyping();
        addMessage('Sorry, I could not connect to the server. Please check your internet connection! 🌐');
        console.error('Chatbot error:', error);
    }
    
    // Re-enable input
    sendBtn.disabled = false;
    userInput.disabled = false;
    userInput.focus();
}

// Quick question click
function askQuestion(question) {
    userInput.value = question;
    sendMessage();
}

// Initialize
console.log('✅ Chatbot loaded successfully');
